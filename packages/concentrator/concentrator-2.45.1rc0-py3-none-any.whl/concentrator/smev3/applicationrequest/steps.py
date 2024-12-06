from datetime import date

from django.core.exceptions import ValidationError
from django.db.models import Q

from kinder import logger
from kinder.core.children.models import Children
from kinder.core.children.models import Delegate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration_status.models import DSS
from kinder.webservice.api.declaration import ApiException
from kinder.webservice.api.declaration import get_decl_by_client_id

from concentrator.change import ChangeSource
from concentrator.change import StorageHelper
from concentrator.models import DocExtraInfo
from concentrator.smev3.base.constants import CODE_ERROR
from concentrator.smev3.base.constants import CODE_OK


from .application import Application
from .changes import Smev3ChangeHelper
from .changes import Smev3ChangesMap
from .changes import Smev3DeclarationPrivilegeChangeHelper
from .changes import Smev3DeclarationUnitChangeHelper
from .changes import Smev3DeclarationDocsChangeHelper
from .constants import ApplicationRequestMessage as _Message
from .constants import MAX_AGE
from .constants import Response


class Step:
    """Класс шага обработки заявления."""

    number = 0

    def __init__(self, request_declaration, 
                 declaration=None, attachments=None):
        """
        :param request_declaration: XML структура заявления
        :param declaration: Сохраненное заявление в ЭДС
        :param attachments: Вложения
        """

        self.request_declaration = request_declaration
        self.declaration = declaration
        self.attachments = attachments

    def __repr__(self):
        return f'<{self.number}: {self.__class__.__name__}>'


class CheckOrderStep(Step):
    """Поиск совпадения по идентификатору заявления orderId."""

    number = 1

    def __next__(self):
        try:
            declaration = get_decl_by_client_id(
                self.request_declaration.orderId)
        except ApiException:
            return RequestValidationStep(
                self.request_declaration, attachments=self.attachments)
        return ExistingDeclarationStep(
            self.request_declaration, declaration, self.attachments)


class ExistingDeclarationStep(Step):
    """Сравнение данных заявления в ЭДС и данных в запросе."""

    number = 2

    def _unit_helper(self):
        """Возвращает хелпер проверки изменений в желаемых учреждениях."""

        helper = Smev3DeclarationUnitChangeHelper(
            DeclarationUnit, 'DeclarationUnit')
        helper.check_diff(self.request_declaration, self.declaration)
        return helper

    def _benefits_helper(self):
        """Возвращает хелпер проверки изменений льгот."""

        helper = Smev3DeclarationPrivilegeChangeHelper(
            DeclarationPrivilege, 'DeclarationPrivilege')
        helper.check_diff(self.request_declaration, self.declaration)
        return helper

    def __next__(self):
        today = date.today()
        border = date(today.year - MAX_AGE, today.month, today.day)
        birth = self.request_declaration.ChildInfo.ChildBirthDate
        if birth and birth <= border:
            return Response(
                order_id=self.request_declaration.orderId,
                status_code=CODE_ERROR, comment=_Message.OLD)

        change_map = Smev3ChangesMap()

        helpers = [
            self._unit_helper(),
            self._benefits_helper(),
        ]

        check_diff = [
            (Declaration, 'Declaration', self.declaration),
            (Children, 'Children', self.declaration.children),
        ]

        for children_delegate in (
                self.declaration.children.childrendelegate_set.all()):
            delegate = children_delegate.delegate
            check_diff.append((Delegate, 'Delegate', delegate))

        for model, model_name, instance in check_diff:
            helper = Smev3ChangeHelper(
                model, model_name, map_changes=change_map)
            helper.check_diff(self.request_declaration, instance)
            helpers.append(helper)

        if self.attachments:
            helper = Smev3DeclarationDocsChangeHelper(DocExtraInfo)
            helper.check_diff(
                self.declaration, self.attachments)
            helpers.append(helper)

        updated = StorageHelper.create_change(
            self.declaration, helpers, source=ChangeSource.UPDATE_APPLICATION)

        if not updated:
            return Response(
                order_id=self.request_declaration.orderId,
                status_code=CODE_ERROR,
                comment=_Message.NO_CHANGES)
        return Response(
            order_id=self.request_declaration.orderId,
            status_code=CODE_OK,
            comment=_Message.CHANGES_SUCCESS)


class RequestValidationStep(Step):
    """Валидация запроса и создание заявления."""

    number = 3

    def __next__(self):

        child_info = self.request_declaration.ChildInfo

        today = date.today()
        border = date(today.year - MAX_AGE, today.month, today.day)
        if (child_info.ChildBirthDate
                and child_info.ChildBirthDate <= border):
            return Response(
                order_id=self.request_declaration.orderId,
                status_code=CODE_ERROR, comment=_Message.OLD)

        base_filter = (
                Q(children__surname__iexact=child_info.ChildSurname)
                & Q(children__firstname__iexact=child_info.ChildName)
                & Q(children__date_of_birth=child_info.ChildBirthDate)
                & ~Q(status__code__in=DSS.no_active_statuses())
                & (Q(children__snils=child_info.ChildSNILS)
                   | Q(children__dul_series=(
                    child_info.ChildBirthDocRF.ChildBirthDocSeries),
                    children__dul_number=(
                        child_info.ChildBirthDocRF.ChildBirthDocNumber),
                    children__dul_date=(
                        child_info.ChildBirthDocRF.ChildBirthDocIssueDate))))

        if Declaration.objects.filter(base_filter).exists():
            # Формирует ответ с сообщением о существовании дубля в системе
            return Response(
                order_id=self.request_declaration.orderId,
                status_code=CODE_ERROR, comment=_Message.MULTIPLE)

        try:
            Application(self.request_declaration, self.attachments).create()
        except ValidationError as e:
            logger.error(f'{_Message.DATA_ERROR} ApplicationRequest '
                         f'({"; ".join(e.messages)})')
            return Response(
                order_id=self.request_declaration.orderId,
                status_code=CODE_ERROR, comment=_Message.DATA_ERROR)

        return Response(
            order_id=self.request_declaration.orderId,
            status_code=CODE_OK, comment=_Message.SUCCESS)
