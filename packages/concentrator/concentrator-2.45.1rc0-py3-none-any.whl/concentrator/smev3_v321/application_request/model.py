from dataclasses import dataclass


@dataclass
class ApplicationManagerData:
    """Класс данных выполнения менеджера обработки заявления."""

    order_id: int
    org_code: int
    tech_code: int
    comment: str
