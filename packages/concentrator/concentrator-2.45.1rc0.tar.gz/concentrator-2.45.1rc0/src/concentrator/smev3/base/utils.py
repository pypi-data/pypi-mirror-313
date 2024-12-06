import uuid

from abc import ABC
from abc import abstractmethod
from collections import Iterable
from io import StringIO

from m3 import ApplicationLogicException
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration_status.enum import DSS
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import GroupSpec
from kinder.core.queue_module.context import QueueContext
from kinder.core.queue_module.queue import QueueClass
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitKind
from kinder.plugins.contingent.models import DelegateContingent

from concentrator.smev3.service_types import kinder_conc
from concentrator import settings

from . import constants


class SMEV3Response:

    def __init__(self, response, logging_data):
        """Настройка ответа.

        :param response: ответ
        :type response: requests.Response
        :param logging_data: дополнительные данные для логирования
        :type logging_data: dict
        """

        self.response = response
        self.logging_data = logging_data


class BaseExecutor(ABC):
    """Базовый класс исполнителя сервиса СМЭВ 3."""

    name_service = None
    type_service = None

    @classmethod
    def __subclasshook__(cls, subclass):

        if cls is BaseExecutor:
            return any(
                True for sub in subclass.__mro__
                if sub.__dict__.get('process') is not None)

        return NotImplemented

    @classmethod
    @abstractmethod
    def process(cls, message, request_body):
        """Запускает выполнение логики обработки сервиса.

        :param message: xml пакет
        :param request_body: тип

        :return: инстанс ответа
        :rtype: SMEV3Response
        """
        pass


class SMEV3RepositoryExecutors:
    """Хранилище исполнителей сервисов СМЭВ 3."""

    _store = [
        # (Наименование сервиса, Тип сервиса, Обработчик сервиса),
        # ...
    ]

    @classmethod
    def set_up(cls, config):
        """Инициализирует хранилище класса.

        Принимает список наследников класса BaseExecutor
        или структуру вида:
        (Наименование сервиса, Тип сервиса, Обработчик сервиса).

        :param config: список настроек
        :type config: Union[
            Iterable[Tuple[str, Type, callable]],
            Iterable[BaseExecutor]]
        :return: None
        """
        cls._store.extend(
            (i.name_service, i.type_service, i.process)
            if not isinstance(i, Iterable) and issubclass(i, BaseExecutor)
            else i for i in config)

    @classmethod
    def get_executor(cls, message):
        """Определяет исполнителя для полученного пакета.

        :param message: Тип, содержащий данные сервиса
        :return: Ссылку на метод исполнителя
        """

        for name_service, type_service, executor in cls._store:
            service = getattr(message, name_service, None)
            if (service
                    and isinstance(service, type_service)
                    and callable(executor)):
                return executor


def render_type2xml(type_, name_type, pretty_print=False):
    """Рендерит классы в xml.

    :param type_: инстанс типа
    :param name_type: наименование типа
    :param pretty_print: признак "красивого" вывода в xml
    :return: сформированный xml
    """

    buffer = StringIO()
    type_.export(
        buffer, 0, name_=name_type, pretty_print=pretty_print)

    return buffer.getvalue()


# TODO Его необходимость под вопросом, не используется
class CustomStringIO(StringIO):
    """Обход UnicodeDecodeError: 'ascii' codec can't decode
    при сливание строк
    """

    # def getvalue(self):
    #     """
    #     """

    #     def _complain_ifclosed(closed):
    #         if closed:
    #             raise ValueError("I/O operation on closed file")

    #     _complain_ifclosed(self.closed)
    #     if self.buflist:
    #         for line in self.buflist:
    #             if isinstance(line, str):
    #                 line = str(line, 'utf-8')
    #             self.buf += line
    #         self.buflist = []
    #     return self.buf


def get_queue_info_short(declaration, unit_id, external_context=None):
    """Получение позиции очереди всего в очереди
    :param declaration: Заявление
    :param unit_id:  int Организация, по которой формируется очередь
    :param external_context: dict доп параметры для контекста очереди
    :return:
    """

    context = QueueContext.make_base_context(
        declaration.children.date_of_birth, unit_id)
    if external_context:
        for key, value in external_context.items():
            setattr(context, key, value)

    queue = QueueClass().get_class()(context)
    result = (None, None)

    rows, all = queue.get_list(0)
    for row in rows:
        if row['id'] == declaration.id:
            result = (row['num'], all)
            break
    return result


def get_spec_decl(declaration):
    """Возвращаем специфику групп в заявление.

    :param declaration:
    :type declaration: Declaration

    :return: идентификатор из справочник специфик
    :rtype: Union[int, str]
    """

    default_id = (
        GroupSpec.objects.filter(
            code=GroupSpec.DEFAULT_CODE
        ).values_list('id', flat=True).first() or '')
    return declaration.spec_id or default_id


def get_oktmo_region():
    """Возвращает ОКТМО головного учреждения.

    :return: октмо или None
    :rtype: Optional[str]
    """

    region = Unit.objects.filter(kind=UnitKind.REGION).last()

    return region.octmo if region else None


def get_declaration_units(declaration):
    """
    возвращаем желаемые организации заявки
    в виде списка [('unit_name', 'unit_id', 'ord'), ...]

    :param declaration: заявка
    :return:
    """
    return declaration.declarationunit_set.values_list(
        'unit__name', 'unit_id', 'ord')


def get_dul_delegate_type(delegate):
    """Возвращает  наименование Типы документов удостоверяющего
    личность представителя
    :param delegate: Delegate
    :return:
    """
    try:
        record = DULDelegateType.objects.get(id=delegate.dul_type_id)
    except DULDelegateType.DoesNotExist:
        return None
    return record.name


def get_contingent_param_delegate(delegate):
    """Возвращает сведения гражданства из плагина контингент представителя
    :param delegate: Delegate
    :return: tuple
    """
    try:
        record = DelegateContingent.objects.get(delegate=delegate.id)
    except DelegateContingent.DoesNotExist:
        return None, None, None
    return record.citizenship, record.citizenship_country, record.birthplace


def get_privileges(declaration):
    """Возвращает параметры льгот в заявление
    :param declaration: Declaration
    :return:  list список параметров льготы
    """
    return DeclarationPrivilege.objects.filter(
        declaration=declaration).values_list(
        'privilege_id',
        'privilege__name',
        'doc_type_id',
        'doc_type__name',
        'doc_series',
        'doc_number'
    )


def gender_mapping(delegate):
    """Маппинг в значения для концентратора пола предствителя
    :param delegate: Delegate
    :return: tuple
    """
    return constants.DELEGATE_GENDER_ENUM.get(delegate.gender)


def get_order_id(declaration):
    """Получение идентификатора (кода) заявки.

    :param declaration: заявление
    :type declaration: Declaration

    :return: идентификатор (код заявки)
    :rtype: int

    :raise: ApplicationLogicException
    """

    try:
        _id = int(declaration.client_id)
    except (ValueError, TypeError):
        raise ApplicationLogicException('Идентификатор заявки невалиден')

    return _id


def generate_message_id():
    """Генерация ID сообщения."""
    return str(uuid.uuid1())


def is_cancel_allowed(status):
    """Проверяет разрешена ли отмена заявления в указанном статусе

    :param status: Статус заявления
    :type status: DeclarationStatus
    :return: Разрешена ли отмена
    :rtype: bool
    """

    if status.code in list(DSS.values.keys()):
        if getattr(settings, status.code.upper(), False):
            return True
    elif settings.OTHER_STATUS:
        return True

    return False
