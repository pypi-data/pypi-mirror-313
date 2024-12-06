import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery

from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.dict.models import UnitKind
from kinder.core.group.enum import GroupStatusEnum
from kinder.core.group.models import Pupil
from kinder.core.unit.models import Unit
from kinder.reports.impersonal_children_list.providers import (
    ImpersonalReportProvider)


class AttachmentRequestReportProvider(ImpersonalReportProvider):
    """Провайдер данных для сервиса AttachmentRequest."""

    def pupils_data(self):
        """Данные по зачисленным детям"""

        _current_date = datetime.date.today()

        # Максимальный приоритет льготы по заявке ребенка
        privilege_best_priority = DeclarationPrivilege.objects.filter(
            declaration_id=OuterRef('declaration_id')
        ).order_by('privilege__order_type__code')

        # Подзапрос на поиск МО для организации
        subquery_alloc_date_begin = (
            Unit.objects.filter(
                Q(lft__lte=OuterRef('grup__unit__lft'))
                & Q(rght__gte=OuterRef('grup__unit__rght'))
                & Q(tree_id=OuterRef('grup__unit__tree_id'))
                & Q(kind_id=UnitKind.MO)))

        # Базовый запрос:
        # Зачисления в группы заданных организаций;
        # День и месяц начала комплектования заполнены в МО;
        # Дата зачисления по приказу в ДОО заполнена и <= Текущей даты.
        base_pupils_query = (
            Pupil.objects.annotate(
                alloc_date_bgn_month=Subquery(
                    subquery_alloc_date_begin.values(
                        'alloc_date_bgn_month')[:1]),
                alloc_date_bgn_day=Subquery(
                    subquery_alloc_date_begin.values('alloc_date_bgn_day')[:1])
            ).filter(
                Q(grup__unit__in=self.units)
                & Q(alloc_date_bgn_month__isnull=False)
                & Q(alloc_date_bgn_day__isnull=False)
                & Q(date_in_order_to_doo__isnull=False)
                & Q(date_in_order_to_doo__lte=_current_date)))

        # Данные фактических зачислений
        pupils_fact_ids = (
            base_pupils_query.filter(
                Q(grup__status=GroupStatusEnum.FACT)
            ).values(
                'id', 'children_id'
            ).order_by('children_id', 'id').distinct('children_id'))

        fact_children_ids = [x['children_id'] for x in pupils_fact_ids]

        pupils_fact_ids = [x['id'] for x in pupils_fact_ids]

        # Данные планновых зачислений
        pupils_plan_ids = (
            base_pupils_query.filter(
                Q(grup__status=GroupStatusEnum.PLAN)
            ).exclude(
                children_id__in=fact_children_ids
            ).values('id').order_by('children_id', 'id').distinct('children_id'))

        pupils_data = Pupil.objects.annotate(
            privilege_best_priority=Subquery(
                privilege_best_priority.values(
                    'privilege__order_type__code')[:1]),
            alloc_date_bgn_month=Subquery(
                subquery_alloc_date_begin.values('alloc_date_bgn_month')[:1]),
            alloc_date_bgn_day=Subquery(
                subquery_alloc_date_begin.values('alloc_date_bgn_day')[:1])
        ).filter(
            Q(Q(id__in=pupils_fact_ids) | Q(id__in=pupils_plan_ids))
        ).values(
            'declaration__client_id',  # Идентификатор
            'declaration__date',
            'privilege_best_priority',
            'grup__status',  # Статус группы
            'grup__age_cat__name',  # Возрастная категория группы
            'grup__type__name',  # Направленность группы
            'grup__work_type__name',  # Режим пребывания
            'grup__program__syllabus__name',  # Образовательная программа
            'grup__spec__name',  # Язык обучения
            'date_in_order_to_doo',
            'alloc_date_bgn_month',
            'alloc_date_bgn_day'
        ).order_by('declaration_id')

        # Выполняет проверку, что Дата зачисления по приказу в ДОО
        # >= Даты начала комплектования.
        for pupil_data in pupils_data.iterator():

            # Дата начала планового комплектования.
            alloc_date_bgn = datetime.date(
                _current_date.year,
                pupil_data['alloc_date_bgn_month'],
                pupil_data['alloc_date_bgn_day'])

            # Если дата тек. комплектования меньше даты начала планового
            # комлектования, то фиксируется дата планового
            # комплектования за прошлый год.
            if _current_date < alloc_date_bgn:
                alloc_date_bgn -= relativedelta(years=1)

            if pupil_data['date_in_order_to_doo'] >= alloc_date_bgn:
                yield pupil_data
