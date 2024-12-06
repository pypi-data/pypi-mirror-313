import gettext
import re
from abc import abstractmethod
from collections.abc import Iterable, Iterator
from contextlib import contextmanager, suppress
from contextvars import ContextVar
from decimal import Decimal
from operator import itemgetter
from pathlib import Path
from typing import ClassVar, ContextManager, Protocol, runtime_checkable

from babel import Locale, UnknownLocaleError
from babel.support import Translations
from injection import singleton

from hundred import DIRECTORY as HUNDRED_DIR


@runtime_checkable
class I18NService(Protocol):
    __slots__ = ()

    @abstractmethod
    def get_translations(self) -> gettext.NullTranslations:
        raise NotImplementedError

    @abstractmethod
    def locale_scope(self, *locales: Locale) -> ContextManager[None]:
        raise NotImplementedError


type LocaleScope = Iterable[Locale]


@singleton(on=I18NService, inject=False, mode="fallback")
class BabelService(I18NService):
    __slots__ = ("__default_locale", "__directories", "__domain")

    __directory: ClassVar[Path] = HUNDRED_DIR / "lang"
    __scope: ClassVar[ContextVar[LocaleScope | None]] = ContextVar(
        "locale_scope",
        default=None,
    )

    def __init__(
        self,
        default_locale: Locale = Locale("en"),
        directories: Iterable[Path] = (),
        domain: str = Translations.DEFAULT_DOMAIN,  # type: ignore[has-type]
    ) -> None:
        self.__default_locale = default_locale
        self.__directories = frozenset((*directories, self.__directory))
        self.__domain = domain

    @contextmanager
    def locale_scope(self, *locales: Locale) -> Iterator[None]:
        if self.__default_locale not in locales:
            locales = *locales, self.__default_locale

        token = self.__scope.set(locales)
        yield
        self.__scope.reset(token)

    def get_translations(self) -> gettext.NullTranslations:
        locales = self.__get_scope()
        return self.load(*locales)

    def load(self, *locales: Locale) -> gettext.NullTranslations:
        loader = self.__loader(*locales)

        try:
            translations = next(loader)
        except StopIteration:
            return gettext.NullTranslations()

        for loaded in loader:
            translations.add_fallback(loaded)

        return translations

    def __loader(self, *locales: Locale) -> Iterator[Translations]:
        for directory in self.__directories:
            with suppress(FileNotFoundError):
                yield gettext.translation(
                    self.__domain,
                    directory,
                    tuple(str(locale) for locale in locales),
                    Translations,
                )

    def __get_scope(self) -> LocaleScope:
        return self.__scope.get() or (self.__default_locale,)


class AcceptLanguageHeaderParser:
    __slots__ = ()

    __pattern = re.compile(
        r"\s*(?P<language>[a-z]{2})(?:-(?P<territory>[A-Z]{2}))"
        r"?(?:\s*;q=(?P<q>[0-9]\.[0-9]))?(?:\s*,|$)"
    )

    def __call__(self, accept_language: str) -> tuple[Locale, ...]:
        header = dict(self.__parser(accept_language))
        return tuple(
            locale
            for locale, q in sorted(
                header.items(),
                key=itemgetter(1),
                reverse=True,
            )
        )

    @classmethod
    def __parser(cls, accept_language: str) -> Iterator[tuple[Locale, Decimal]]:
        for match in re.finditer(cls.__pattern, accept_language):
            language, territory, q = match.group("language", "territory", "q")

            try:
                locale = Locale(language, territory)
            except UnknownLocaleError:
                continue

            if q is None:
                q = Decimal(1)
            else:
                q = Decimal(q)

            yield locale, q


parse_accept_language_header = AcceptLanguageHeaderParser()

del AcceptLanguageHeaderParser
