from pathlib import Path

from django.template import Template, Context

from kinder.test.base import BaseTC
from concentrator.smev3_v321.service_types import kinder_conc


class BaseApplicationOrderInfoTC(BaseTC):
    """Базовый класс для тестов ApplicationOrderInfo."""

    fixtures = ['start_data_dict', 'status_initial_data']
    REQUEST_TEMPLATE_NAME = 'request_template.xml'

    @staticmethod
    def get_test_template(template_name):
        """Считывает текст шаблона из папки test_templates."""
        template_path = Path(__file__).parent.joinpath(
            f'test_templates/{template_name}')
        return template_path.read_text()

    @classmethod
    def get_prepared_request(cls, data, template_name=REQUEST_TEMPLATE_NAME):
        """Получение объекта запроса ApplicationOrderInfo.

        :param data: Параметры для шаблона для заполнения запроса
        :param template_name: Название шаблона из папки test_templates

        :return: Объект запроса ApplicationOrderInfo
        """
        template = Template(cls.get_test_template(template_name))
        context = Context(data)
        rendered_template = template.render(context)
        return kinder_conc.parseString(
            rendered_template, silence=True).ApplicationOrderInfoRequest
