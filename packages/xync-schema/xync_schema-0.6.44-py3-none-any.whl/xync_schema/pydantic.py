from pydantic import BaseModel


class FiatUpd(BaseModel):
    detail: str | None = None
    name: str | None = None
    amount: float | None = None
    target: int | None = None


class FiatNew(FiatUpd):
    cur_id: int
    pm_id: int
    detail: str
    amount: float = 0
