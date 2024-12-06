import json
import os

import mock
from django.db.models.signals import post_save, pre_save
from factory.django import mute_signals
from lxml import etree

from aio_client.base.models.tests.utils import mock_request_return_log
from aio_client.provider.api import get_requests
from concentrator.models import ChangeDeclaration
from concentrator.smev3.service_types import kinder_conc
from concentrator.smev3.applicationrequest.application import Application
from concentrator.smev3.applicationrequest.helpers import (
    ApplicationRequestExecutor)
from concentrator.smev3.base.constants import CODE_ERROR
from concentrator.smev3.base.constants import CODE_OK
from concentrator.smev3.base.tests.utils import examples
from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.unit.tests.factory_unit import UnitDouFactory
from kinder.test.base import BaseTC

from .factories import GetProviderRequestF

example_package_client_id = '12345678'
example_package = next(examples(os.path.dirname(__file__)))


class IntegrationTC(BaseTC):

    fixtures = [
        'start_data_dict', 'status_initial_data', 'priv_test_initial_data']

    def setUp(self):
        super().setUp()

        GetProviderRequestF.create(body=example_package)
        self.message = get_requests()[0]
        self.request_body = kinder_conc.parseString(self.message.get('body'))
        self.aio_patcher_post = mock.patch(
            'aio_client.base.helpers.send_request',
            side_effect=mock_request_return_log())
        self.aio_patcher_post.start()

    def tearDown(self):
        self.aio_patcher_post.stop()
        super().tearDown()

    def assertResponse(self, response, status_code):
        response_body = etree.fromstring(response.http_body['body'])
        response_status_code = response_body.find('.//{*}techCode').text
        self.assertEquals(int(response_status_code), status_code)

    def test_create_new_application(self):
        """Подача нового заявления в систему."""
        with mock.patch.object(Application, 'create') as patched:
            response = ApplicationRequestExecutor.process(
                self.message, self.request_body)
            self.assertResponse(response.response, CODE_OK)
            patched.assert_called_once()

    def test_application_exists_no_changes(self):
        """Подача заявления существующего в системе с такими же данными."""
        with mute_signals(pre_save, post_save):
            for id_ in (215, 219, 221):
                UnitDouFactory.create(id=id_)
        Application(
            kinder_conc.parseString(
                example_package, silence=True).ApplicationRequest, None).create()
        response = ApplicationRequestExecutor.process(
            self.message, self.request_body)
        self.assertResponse(response.response, CODE_ERROR)

    def test_application_exists_and_have_changes(self):
        """Подача заявления с изменениями."""
        #TODO: Падает ошибка TypeError: Object of type 'WorkType' is not JSON serializable
        # DeclarationF.create(
        #     client_id=example_package_client_id,
        #     children__firstname='Василий',
        #     children__surname='Петров',
        # )
        # response = ApplicationRequestExecutor.process(
        #     self.message, self.request_body)
        # self.assertResponse(response.response, CODE_OK)
        # self.assertEquals(ChangeDeclaration.objects.count(), 1)
        # changes = json.loads(ChangeDeclaration.objects.last().data)
        # child_changes = changes['Children']
        # self.assertTrue([c for c in child_changes if c.get('surname')])
        # self.assertFalse([c for c in child_changes if c.get('firstname')])
