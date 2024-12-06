from datetime import timedelta
from uuid import UUID

from injection import injectable
from pydantic import SecretStr

from hundred.ctx.auth.aliases import AccessTokenLifespan, TrustedAccessTokenLifespan
from hundred.ctx.auth.domain import Session, SessionStatus, User
from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.factories import SessionFactory
from hundred.ctx.auth.ports import SessionRepository
from hundred.exceptions import Conflict
from hundred.gettext import gettext as _
from hundred.services.authenticator import StatelessAuthenticator
from hundred.services.datetime import DateTimeService
from hundred.services.token import TokenService


@injectable(mode="fallback")
class SessionService:
    __slots__ = (
        "__access_token_lifespan",
        "__authenticator",
        "__datetime_service",
        "__session_factory",
        "__session_repository",
        "__token_service",
        "__trusted_access_token_lifespan",
    )

    def __init__(
        self,
        *,
        access_token_lifespan: AccessTokenLifespan = timedelta(minutes=30),
        authenticator: StatelessAuthenticator,
        datetime_service: DateTimeService,
        session_factory: SessionFactory,
        session_repository: SessionRepository,
        token_service: TokenService,
        trusted_access_token_lifespan: TrustedAccessTokenLifespan = timedelta(
            minutes=10,
        ),
    ) -> None:
        self.__access_token_lifespan = access_token_lifespan
        self.__authenticator = authenticator
        self.__datetime_service = datetime_service
        self.__session_factory = session_factory
        self.__session_repository = session_repository
        self.__token_service = token_service
        self.__trusted_access_token_lifespan = trusted_access_token_lifespan

    @property
    def __fake_access_token(self) -> str:
        return self.__generate_token(
            user_id=UUID("00000000-0000-0000-0000-000000000000"),
            is_trusted=False,
            session_status=SessionStatus.UNVERIFIED,
        )

    async def ensure_session_can_be_created(self, application_id: UUID) -> None:
        session = await self.__session_repository.get(application_id)

        if session is None:
            return

        if session.is_unverified:
            await self.logout(application_id)
            return

        raise Conflict(_("already_logged_on_this_device"))

    async def logout(self, application_id: UUID) -> None:
        await self.__session_repository.delete(application_id)

    async def new_session(
        self,
        application_id: UUID,
        user: User,
        status: SessionStatus = SessionStatus.UNVERIFIED,
    ) -> Authenticated:
        session_token = self.__token_service.generate(256)
        session = self.__session_factory.build(application_id, user, session_token)
        session.status = status
        await self.__session_repository.save(session)

        access_token = self.new_access_token(session=session)
        return Authenticated(
            access_token=SecretStr(access_token),
            session_token=SecretStr(session_token),
        )

    async def new_temporary_session(
        self,
        application_id: UUID,
        user: User,
    ) -> Authenticated:
        session = self.__session_factory.build(application_id, user)
        await self.__session_repository.save(session)

        access_token = self.new_access_token(session=session)
        return Authenticated(access_token=SecretStr(access_token))

    async def new_fake_temporary_session(self) -> Authenticated:
        return Authenticated(access_token=SecretStr(self.__fake_access_token))

    def new_access_token(self, session: Session, is_trusted: bool = False) -> str:
        return self.__generate_token(session.user.id, is_trusted, session.status)

    def __generate_token(
        self,
        user_id: UUID,
        is_trusted: bool,
        session_status: SessionStatus,
    ) -> str:
        lifespan = (
            self.__trusted_access_token_lifespan
            if is_trusted
            else self.__access_token_lifespan
        )
        expiration = self.__datetime_service.utcnow() + lifespan
        return self.__authenticator.generate_token(
            data={
                "sub": {
                    "user_id": str(user_id),
                },
                "is_trusted": is_trusted,
                "session_status": session_status,
            },
            expiration=expiration,
        )
