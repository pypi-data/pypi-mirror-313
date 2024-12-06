# coding: utf-8

import os

from kinder.webservice.push_event.loader import PushEventLoader


class QueueDirectionDecisionLoader(PushEventLoader):
    """
    Изменен шаблон
    """

    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__))

    TEMPLATE_NAME = "template_with_file.wsdl"
