# coding: utf-8


from kinder.webservice.spyne_ws.declaration_info.descriptors import (
    SummaryPosition)


class SummaryWithOutAgePosition(SummaryPosition):
    """Показатели по сводной очереди в ДОО без учета возраста"""

    value_field_name = "_summary_with_out_age"

    def _get_context(self):

        ctx = super(SummaryWithOutAgePosition, self)._get_context()
        ctx.update({"age1": None, "age2": None})

        return ctx
