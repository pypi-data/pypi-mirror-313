import uuid

from django.conf import settings
from educommon.report import AbstractDataProvider
from educommon.report import AbstractReportBuilder
from educommon.report.reporter import SimpleReporter
from educommon.report.reporter import get_path
from educommon.report.reporter import get_url

from kinder.core.declaration.models import Declaration


def if_date_str(date):
    return date.strftime(settings.DATE_FORMAT) if date else u''


class BasePassingSmevReporter(SimpleReporter):
    u"""Базовый класс для отчетов - Миня СМЭВ."""

    def set_file_and_url(self):
        base_name = str(uuid.uuid4())[0:16] + self.extension
        self.out_file_path = get_path(base_name)
        self.out_file_url = get_url(base_name)
        return (self.out_file_path, self.out_file_url)


class BasePassingSmevProvider(AbstractDataProvider):
    u"""Базовый провайдер для отчетов - Минуя СМЭВ."""

    def init(self, declaration_ids, report_name, **params):
        self.declaration_ids = declaration_ids
        self.report_name = report_name


class BasePassingSmevBuilder(AbstractReportBuilder):

    u"""Базовый построитель для отчетов - Минуя СМЭВ."""

    def __init__(self, provider, adapter, report, params):
        self.provider = provider
        self.report = report

    def _init_sections(self):
        get_section = self.report.get_section
        self.header_section = get_section('header')
        self.item_section = get_section('item')

    def after_build(self):
        # Полная область печати
        self.report.workbook.xlwt_writer.wtsheet.fit_num_pages = 1


class FirstTypePassingSmevProvider(BasePassingSmevProvider):
    u"""Провайдер для первого типа отчета - Минуя СМЭВ."""

    def get_declarations(self):
        delegate_lookup = (
            'declarationprivilege__privilegeconfirmationattributes__delegate'
        )
        return Declaration.objects.filter(
            pk__in=self.declaration_ids
        ).values_list(
            '{}__fullname'.format(delegate_lookup),
            '{}__date_of_birth'.format(delegate_lookup),
            '{}__reg_address_full'.format(delegate_lookup),
            '{}__snils'.format(delegate_lookup),
            'children__fullname',
            'children__date_of_birth',
        )


class FirstTypePassingSmevBuilder(BasePassingSmevBuilder):
    u"""Построитель для первого типа отчета - Минуя СМЭВ."""

    def build(self):
        self._init_sections()
        self.header_section.flush({'name': self.provider.report_name})

        for idx, (
            delegate_fullname,
            delegate_date_of_birth,
            delegate_address,
            delegate_snils,
            fullname,
            date_of_birth
        ) in enumerate(self.provider.get_declarations(), 1):
            self.item_section.flush({
                'idx': idx,
                'delegate_fullname': delegate_fullname,
                'delegate_date_of_birth': if_date_str(delegate_date_of_birth),
                'delegate_address': delegate_address,
                'delegate_snils': delegate_snils,
                'children_info': u', '.join((
                    fullname, if_date_str(date_of_birth)
                )),
            })
        self.after_build()


class FirstTypePassingSmevReporter(BasePassingSmevReporter):
    u"""Первый тип отчета - Минуя СМЭВ."""

    extension = '.xls'
    template_file_path = './templates/first_type'
    data_provider_class = FirstTypePassingSmevProvider
    builder_class = FirstTypePassingSmevBuilder


class SecondTypePassingSmevProvider(BasePassingSmevProvider):
    u"""Провайдер для первого типа отчета - Минуя СМЭВ."""

    def get_declarations(self):
        attr_lookup = 'declarationprivilege__privilegeconfirmationattributes'
        delegate_lookup = '{}__delegate'.format(attr_lookup)
        delegate_contingent = '{}__delegatecontingent'.format(delegate_lookup)

        return Declaration.objects.filter(
            pk__in=self.declaration_ids
        ).values_list(
            '{}__fullname'.format(delegate_lookup),
            '{}__date_of_birth'.format(delegate_lookup),
            '{}__birthplace'.format(delegate_contingent),
            '{}__reg_address_full'.format(delegate_lookup),
            '{}__snils'.format(delegate_lookup),
            '{}__name_of_unit'.format(attr_lookup),
            '{}__rank'.format(attr_lookup),
            'children__fullname',
            'children__date_of_birth',
        )


class SecondTypePassingSmevBuilder(BasePassingSmevBuilder):
    u"""Построитель для первого типа отчета - Минуя СМЭВ."""

    def build(self):
        self._init_sections()
        self.header_section.flush({'name': self.provider.report_name})

        for idx, (
            delegate_fullname,
            delegate_date_of_birth,
            delegate_birthplace,
            delegate_address,
            delegate_snils,
            name_of_unit,
            delegate_rank,
            fullname,
            date_of_birth
        ) in enumerate(self.provider.get_declarations(), 1):
            self.item_section.flush({
                'idx': idx,
                'delegate_fullname': delegate_fullname,
                'delegate_date_of_birth': if_date_str(delegate_date_of_birth),
                'delegate_birthplace': delegate_birthplace,
                'delegate_address': delegate_address,
                'delegate_snils': delegate_snils,
                'name_of_unit': name_of_unit,
                'delegate_rank': delegate_rank,
                'children_info': u', '.join((
                    fullname, if_date_str(date_of_birth)
                )),
            })
        self.after_build()


class SecondTypePassingSmevReporter(BasePassingSmevReporter):
    u"""Первый тип отчета - Минуя СМЭВ."""

    extension = '.xls'
    template_file_path = './templates/second_type'
    data_provider_class = SecondTypePassingSmevProvider
    builder_class = SecondTypePassingSmevBuilder


class ThirdTypePassingSmevProvider(BasePassingSmevProvider):
    u"""Провайдер для третьего типа отчета - Минуя СМЭВ."""

    def get_declarations(self):
        attr_lookup = 'declarationprivilege__privilegeconfirmationattributes'
        delegate_lookup = '{}__delegate'.format(attr_lookup)
        delegate_contingent = '{}__delegatecontingent'.format(delegate_lookup)

        return Declaration.objects.filter(
            pk__in=self.declaration_ids
        ).values_list(
            '{}__fullname'.format(delegate_lookup),
            '{}__date_of_birth'.format(delegate_lookup),
            '{}__birthplace'.format(delegate_contingent),
            '{}__reg_address_full'.format(delegate_lookup),
            '{}__snils'.format(delegate_lookup),
            '{}__ovd'.format(attr_lookup),
            '{}__rank'.format(attr_lookup),
            'children__fullname',
            'children__date_of_birth',
        )


class ThirdTypePassingSmevBuilder(BasePassingSmevBuilder):
    u"""Построитель для третьего типа отчета - Минуя СМЭВ."""

    def build(self):
        self._init_sections()
        self.header_section.flush({'name': self.provider.report_name})

        for idx, (
            delegate_fullname,
            delegate_date_of_birth,
            delegate_birthplace,
            delegate_address,
            delegate_snils,
            delegate_ovd,
            delegate_rank,
            fullname,
            date_of_birth
        ) in enumerate(self.provider.get_declarations(), 1):
            self.item_section.flush({
                'idx': idx,
                'delegate_fullname': delegate_fullname,
                'delegate_date_of_birth': if_date_str(delegate_date_of_birth),
                'delegate_birthplace': delegate_birthplace,
                'delegate_address': delegate_address,
                'delegate_snils': delegate_snils,
                'delegate_ovd': delegate_ovd,
                'delegate_rank': delegate_rank,
                'children_info': u', '.join((
                    fullname, if_date_str(date_of_birth)
                )),
            })
        self.after_build()


class ThirdTypePassingSmevReporter(BasePassingSmevReporter):
    u"""Третий тип отчета - Минуя СМЭВ."""

    extension = '.xls'
    template_file_path = './templates/third_type'
    data_provider_class = ThirdTypePassingSmevProvider
    builder_class = ThirdTypePassingSmevBuilder


class FourthTypePassingSmevProvider(BasePassingSmevProvider):
    u"""Провайдер для четвертого типа отчета - Минуя СМЭВ."""

    def get_declarations(self):
        attr_lookup = 'declarationprivilege__privilegeconfirmationattributes'
        delegate_lookup = '{}__delegate'.format(attr_lookup)

        return Declaration.objects.filter(
            pk__in=self.declaration_ids
        ).values_list(
            '{}__fullname'.format(delegate_lookup),
            '{}__date_of_birth'.format(delegate_lookup),
            '{}__personal_number'.format(attr_lookup),
            '{}__force_kind'.format(attr_lookup),
            '{}__military_unit'.format(attr_lookup),
            '{}__dismissal_date'.format(attr_lookup),
            '{}__dul_type__name'.format(delegate_lookup),
            '{}__dul_series'.format(delegate_lookup),
            '{}__dul_number'.format(delegate_lookup),
            '{}__document'.format(attr_lookup),
            '{}__military_document'.format(attr_lookup),
            'children__fullname',
            'children__date_of_birth',
        )


class FourthTypePassingSmevBuilder(BasePassingSmevBuilder):
    u"""Построитель для четвертого типа отчета - Минуя СМЭВ."""

    def build(self):
        self._init_sections()
        self.header_section.flush({'name': self.provider.report_name})

        for idx, (
            delegate_fullname,
            delegate_date_of_birth,
            personal_number,
            force_kind,
            military_unit,
            dismissal_date,
            dul_type,
            dul_series,
            dul_number,
            document,
            military_document,
            fullname,
            date_of_birth
        ) in enumerate(self.provider.get_declarations(), 1):
            self.item_section.flush({
                'idx': idx,
                'delegate_fullname': delegate_fullname,
                'delegate_date_of_birth': if_date_str(delegate_date_of_birth),
                'personal_number': personal_number,
                'force_kind': force_kind,
                'military_unit': military_unit,
                'dismissal_date': if_date_str(dismissal_date),
                'dul_info': u', '.join([_f for _f in (
                    dul_type, dul_series, dul_number
                ) if _f]),
                'document': document,
                'military_document': military_document,
                'children_info': u', '.join((
                    fullname, if_date_str(date_of_birth)
                )),
            })
        self.after_build()


class FourthTypePassingSmevReporter(BasePassingSmevReporter):
    u"""Четвертый тип отчета - Минуя СМЭВ."""

    extension = '.xls'
    template_file_path = './templates/fourth_type'
    data_provider_class = FourthTypePassingSmevProvider
    builder_class = FourthTypePassingSmevBuilder
