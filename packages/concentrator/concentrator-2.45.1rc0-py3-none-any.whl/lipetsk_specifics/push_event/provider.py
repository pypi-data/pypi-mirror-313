from kinder.core.children.models import Delegate
from kinder.webservice.push_event.provider import PushEventDataProvider

from .utils import NotificationGenerator
from .utils import binary_notification_creator


class ChangeDeclarationDataProvider(PushEventDataProvider):
    """Изменены статусы и комментарии базового класса"""

    DECISION_STATUS_ID = {
        True: 3,
        False: 10
    }

    DECISION_STATUS_COMMENT = {
        True: u"Сведения изменены",
        False: u"Причина отказа: «Данные не подтверждены»"
    }

    def __init__(self, declaration, **kwargs):
        self._decision = kwargs.get('decision', False)
        self._case_number = kwargs.get('case_number', None)
        super(ChangeDeclarationDataProvider, self).__init__(
            declaration=declaration, **kwargs)
        self._client_id = self._declaration.client_id

    def _get_status_code(self):
        return self.DECISION_STATUS_ID[self._decision]

    def _get_comment(self):
        return self.DECISION_STATUS_COMMENT[self._decision]

    def get_data(self):

        data = super(ChangeDeclarationDataProvider, self).get_data()
        data["case_number"] = self._case_number
        data["order_id"] = self._case_number

        return data


class QueueDirectionDecisionDataProvider(PushEventDataProvider):
    """Изменены статусы, комментарии базового класса и добавлена
    отправка файла
    """

    REJECT_CODE = 10
    APPLY_CODE = 3

    def __init__(self, declaration, comment, user, is_apply=False):

        self._is_apply = is_apply
        self._comment = comment
        self._profile = user.get_profile()
        super(QueueDirectionDecisionDataProvider, self).__init__(**{
            'user': user,
            'commentary': comment,
            'declaration': declaration
        })
        self._client_id = self._declaration.client_id

    def _get_status_code(self):

        if self._is_apply:
            return self.APPLY_CODE
        else:
            return self.REJECT_CODE

    def _get_comment(self):

        return self._comment

    def _get_file(self):

        try:
            delegate = Delegate.objects.get(
                childrendelegate__children=self._declaration.children)
        except Delegate.DoesNotExist:
            return ""
        except Delegate.MultipleObjectsReturned:
            delegate = Delegate.objects.filter(
                childrendelegate__children=self._declaration.children)[0]

        notification_type = (
            NotificationGenerator.IN_QUEUE
            if self._is_apply else NotificationGenerator.REJECT)

        return binary_notification_creator(
            self._declaration, delegate, self._profile, notification_type)

    def get_data(self):

        data = super(QueueDirectionDecisionDataProvider, self).get_data()
        data["file"] = self._get_file()

        return data
