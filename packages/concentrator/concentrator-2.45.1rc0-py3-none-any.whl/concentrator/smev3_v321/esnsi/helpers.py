from django.db import transaction
from django.db.models import QuerySet
from m3.plugins import ExtensionManager

from kinder.helpers import RequestFactory

from concentrator.smev3_v321.models import ESNSIClassifier
from concentrator.smev3_v321.models import UpdateClassifierRequest

from .classifiers import EduControlUnitClassifier
from .classifiers import MaxDooClassifier
from .classifiers import UnitClassifier
from .tasks import EsnsiSendingAllTask
from .tasks import EsnsiSendingTask


class ESNSIRequestFactory(RequestFactory):
    """Фабрика запросов ЕСНСИ
    Обязательные параметры:
    classifier - классификатор ЕСНСИ (ClassifierBase)
    request_type - Тип запроса ЕСНСИ
    instances - один или несколько инстансов соответствующей классификатору модели
    """

    def __init__(self, classifier=None, request_type=None, instances=None):
        super().__init__(instances)

        self.classifier = classifier
        self.request_type = request_type

    def _collect_data_part(self, instance):
        classifier_class = self.classifier.get_classifier_class_by_name()
        return classifier_class.get_data(instance)

    def create_request(self):
        """Создание запроса."""

        data = self._collect_data()

        request = UpdateClassifierRequest.objects.create(
            request_type=self.request_type,
            classifier=self.classifier,
            data=data)

        return request


class ESNSITaskFactory(ESNSIRequestFactory):
    """Фабрика задач ЕСНСИ"""

    def _create_task(self):
        """Создание задачи"""

        return EsnsiSendingTask()

    def set_task(self):
        """Запуск задачи"""

        task = self._create_task()
        request_id = self.create_request().id
        return transaction.on_commit(lambda: task.apply_async((request_id,)))


class ESNSIUnitTaskFactory(ESNSITaskFactory):
    """Фабрика задач ЕСНСИ для справочников.

    Организации (детсады);
    Максимальное количество детсадов, которое может выбрать заявитель.
    """

    pass


class ESNSIUnitAllTaskFactory(ESNSITaskFactory):
    """
    Аналог ESNSIUnitTaskFactory но для запросов 
    в котором передаётся весь справочник

    В этом случае будет передан параметр removeMissing, 
    чтобы удалялись все справочники, которые не были переданы
    """
    def _create_task(self):
        return EsnsiSendingAllTask()


class ESNSITaskFacade:
    """
    Фасад для связывания Фабрик задач ЕСНСИ с соответствующими
    классификаторами.
    """

    CLASSIFIERS = {
        # (classifier, all): factory
        (UnitClassifier.__name__, False): ESNSIUnitTaskFactory,
        (MaxDooClassifier.__name__, False): ESNSIUnitTaskFactory,
        (EduControlUnitClassifier.__name__, False): ESNSIUnitTaskFactory,
        (UnitClassifier.__name__, True): ESNSIUnitAllTaskFactory,
        (MaxDooClassifier.__name__, True): ESNSIUnitAllTaskFactory,
        (EduControlUnitClassifier.__name__, True): ESNSIUnitAllTaskFactory,
    }

    def __init__(self, 
                 classifier: ESNSIClassifier, 
                 request_type: str, 
                 instances: QuerySet, 
                 all_: bool) -> None:
        """
        :param classifier: Классификатор для отправки
        :param request_type: Вид запроса
        :param instances: Объекты для отправки
        :param all_: Отправляются ли все объекты ИС
        """
        self._classifier = classifier
        self._request_type = request_type
        self._instances = instances
        self._all = all_
        self._extend_classifiers()

    def _chose_factory(self):
        """Выбор соответствующей классификатору фабрики"""

        factory = self.CLASSIFIERS.get((self._classifier.classifier_class, self._all))
        return factory

    def chose_factory_set_task(self):
        """Запуск таски для выбранной фабрики"""

        factory = self._chose_factory()
        if not factory:
            return
        return factory(
            self._classifier,
            self._request_type,
            self._instances
        ).set_task()

    def _extend_classifiers(self):
        """Расширение для добавления классификаторов"""

        extra_classifiers = ExtensionManager().execute(
            'esnsi_classifiers_facade_extension')
        if extra_classifiers:
            self.CLASSIFIERS.update(extra_classifiers)


def get_classifier_instance(classifier):
    """Получение инстанса модели ESNSIClassifier по классификатору"""
    return ESNSIClassifier.objects.get(classifier_class=classifier.__name__)
