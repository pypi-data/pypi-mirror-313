from typing import Any

from concentrator.smev3.applicationrequest.rules import DictRule


class DelegateConfRightsRule(DictRule):
    """Правило соответствия Документа о нахождении в РФ"""

    @classmethod
    def system_value(cls, concentrator_value: list[Any]) -> bool:
        """Приводим список к bool, так как в системе не сохраняем данные Документа о нахождении в РФ,
        которые приходят в запросе, а только информацию о его наличии"""

        return bool(concentrator_value)
