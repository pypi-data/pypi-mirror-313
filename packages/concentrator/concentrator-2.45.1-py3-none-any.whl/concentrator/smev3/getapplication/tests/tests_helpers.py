import os

from kinder.webservice.api.declaration import get_declaration_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.smev3.base.constants import CODE_ERROR
from concentrator.smev3.base.constants import CODE_ERROR_COMMENT
from concentrator.smev3.base.tests.base import Smev3TC
from concentrator.smev3.base.tests.utils import examples
from concentrator.smev3.service_types import kinder_conc

from ..helpers import GetApplicationRequestExecutor

# из ./examples/1.xml
ORDER_ID = 12345678


class GetApplicationTC(Smev3TC):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.request_body = kinder_conc.parseString(
            next(examples(os.path.dirname(__file__))))

        cls.order_id = cls.request_body.GetApplicationRequest.orderId
        try:
            cls.declaration = get_declaration_by_client_id(
                GetApplicationRequestExecutor.prepare_query(), cls.order_id)
        except ApiException:
            cls.declaration = None

    def test_get_params(self):

        self.assertEqual(self.declaration, None)
        self.assertEqual(self.order_id, ORDER_ID)

    def test_get_application_response(self):
        response = GetApplicationRequestExecutor.get_response(
            self.declaration, self.order_id)
        self.assertEqual(response.changeOrderInfo.orderId.pguId, ORDER_ID)
        self.assertEqual(response.changeOrderInfo.statusCode.techCode,
                         CODE_ERROR)
        self.assertEqual(response.changeOrderInfo.comment,
                         CODE_ERROR_COMMENT)
