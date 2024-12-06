from cq import DTO
from pydantic import Field, computed_field


class PaginatedList[T](DTO):
    count: int = Field(gt=0)
    per_page: int = Field(gt=0)
    current_page: int = Field(gt=0)
    items: tuple[T, ...]

    def __bool__(self) -> bool:
        return bool(self.items)

    def __len__(self) -> int:
        return len(self.items)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total_pages(self) -> int:
        total = self.count // self.per_page
        rest = self.count % self.per_page

        if rest > 0:
            return total + 1

        return total

    @computed_field  # type: ignore[prop-decorator]
    @property
    def next_page(self) -> int | None:
        page = self.current_page + 1

        if page <= self.total_pages:
            return page

        return None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def previous_page(self) -> int | None:
        page = self.current_page - 1

        if page > 0:
            return page

        return None
