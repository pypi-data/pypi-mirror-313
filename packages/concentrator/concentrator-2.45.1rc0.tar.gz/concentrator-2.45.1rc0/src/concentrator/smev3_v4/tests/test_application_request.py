import datetime
import os

from concentrator.smev3_v321.executors import RepositoryExecutors
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.services import FormDataMessageProcessingService
from concentrator.smev3_v321.tests.factory import GetProviderRequestF
from concentrator.smev3_v4.executors import RepositoryExecutorsSmev3V4
from concentrator.smev3_v4.service_types import kinder_conc4
from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.models import Declaration
from kinder.core.unit.tests.factory_unit import UnitDouFactory
from kinder.test.base import BaseTC


def get_template_path(template_name: str) -> str:
    """Возвращает путь до шаблона запроса"""

    return os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'templates', template_name)

class BaseApplicationRequestTest(BaseTC):

    SMEV_321_TEMPLATE = 'tests/smev3_321.xml'
    SMEV_400_TEMPLATE = 'tests/smev3_4.xml'

    @staticmethod
    def create_request(xml: str, params: dict = None):
        """Создает GetProviderRequest файла по переданному пути"""

        with open(get_template_path(xml), 'r') as test_xml:
            test_data = test_xml.read()
            if params:
                test_data = test_data.format(**params)
            GetProviderRequestF.create(body=test_data, message_type='FormData')


class Smev321vs4ApplicationRequestTestCase(BaseApplicationRequestTest):
    """Тестируем работу сервиса ApplicationRequest для обеих версий СМЭВ3 (3.2.1, 4.0.1)"""

    def test_parse_message(self):
        """Проверка правильной обработки обоих типов сообщений"""

        requests = (
            (self.SMEV_400_TEMPLATE, kinder_conc4.FormDataType, 'test_smev4_message_parsing'),
            (self.SMEV_321_TEMPLATE, kinder_conc.FormDataType, 'test_smev321_message_parsing')
        )

        for xml, expected_obj_type, test_name in requests:
            with self.subTest(test_name):
                self.create_request(xml)

                for msg in FormDataMessageProcessingService().get_messages():
                    obj = msg.parse_body

                    self.assertEqual(True, isinstance(obj, expected_obj_type))

    def test_executors(self):
        """Проверяем, что выбираются правильные исполнители запроса для каждой версии"""

        requests = (
            (self.SMEV_400_TEMPLATE, RepositoryExecutorsSmev3V4, 'test_smev4_executors'),
            (self.SMEV_321_TEMPLATE, RepositoryExecutors, 'test_smev321_executors'),
        )

        for xml, expected_executors, test_name in requests:
            with self.subTest(test_name):
                self.create_request(xml)

                for msg in FormDataMessageProcessingService().get_messages():
                    excs = FormDataMessageProcessingService().get_executors_repository(msg)

                    self.assertEqual(excs, expected_executors)

class Smev4ApplicationRequestTestCase(BaseApplicationRequestTest):
    """Тестируем работу сервиса ApplicationRequest СМЭВ3 4.0.1 и 3.2.1"""

    def setUp(self):
        self.dou = UnitDouFactory.create()
        params = {'dou_id': self.dou.id, 'entry_date': datetime.datetime.today().date}
        self.create_request(self.SMEV_400_TEMPLATE, params)
        self.create_request(self.SMEV_321_TEMPLATE, params)

        FormDataMessageProcessingService().run()

        self.smev_321_declaration = Declaration.objects.filter(client_id='321').first()
        self.smev_400_declaration = Declaration.objects.filter(client_id='4').first()

    def check_declaration_consents_request(
            self, declaration: Declaration, value: bool):
        """"Проверяем заполнение согласий в заявлении"""

        self.assertEqual(declaration.adapted_program_consent, value)
        self.assertEqual(declaration.consent_full_time_group, value)

    def check_delegate_confirming_rights_located_rf(
            self, declaration: Declaration, value: bool):
        """"Проверяем заполнение поля наличия Документа о праве нахождения в РФ"""

        delegate = ChildrenDelegate.objects.get(
            children_id=declaration.children_id).delegate

        self.assertEqual(delegate.confirming_rights_located_rf, value)


    def test_number_of_declarations(self):
        """"Проверяем, что создаются заявления с версией СМЭВ3 3.2.1 и 4.0.1"""

        self.assertEqual(len(Declaration.objects.all()), 2)

    def test_declaration_consents(self):
        """"Проверяем, что заполняются согласия в заявлении в обеих версиях"""

        self.check_declaration_consents_request(self.smev_321_declaration, False)
        self.check_declaration_consents_request(self.smev_400_declaration, True)

    def test_delegate_confirming_rights_located_rf(self):
        """"Проверяем, что заполняется Документ о праве нахождения в РФ в обеих версиях"""

        self.check_delegate_confirming_rights_located_rf(self.smev_321_declaration, False)
        self.check_delegate_confirming_rights_located_rf(self.smev_400_declaration, True)
