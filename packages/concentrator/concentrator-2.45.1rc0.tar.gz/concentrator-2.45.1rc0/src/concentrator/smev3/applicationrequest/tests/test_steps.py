from django.db.models.signals import post_save, pre_save
from factory.django import mute_signals

from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.declaration.tests.factory_declaration import DUnitF
from kinder.core.unit.tests.factory_unit import UnitDouFactory

from concentrator.smev3.applicationrequest.constants import Response
from concentrator.smev3.applicationrequest.constants import (
    ApplicationRequestMessage as _Message)
from concentrator.smev3.applicationrequest.steps import CheckOrderStep
from concentrator.smev3.applicationrequest.steps import ExistingDeclarationStep
from concentrator.smev3.applicationrequest.steps import RequestValidationStep
from concentrator.smev3.base.constants import CODE_ERROR
from concentrator.smev3.base.constants import CODE_OK

from .base import ApplicationTC


class StepsTC(ApplicationTC):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        with mute_signals(pre_save, post_save):
            for id_ in (215, 219, 221):
                UnitDouFactory.create(id=id_)

    def assertNextStep(self, step, next_step_class):
        self.assertTrue(isinstance(step, next_step_class))

    def test_step_1(self):
        """Шаг 1. Поиск совпадения по идентификатору заявления orderId."""

        self.assertNextStep(
            next(CheckOrderStep(self.application)), RequestValidationStep)

        declaration = DeclarationF.create(client_id=self.application.orderId)
        DUnitF(
            declaration=declaration,
            unit=self.unit
        )

        self.assertNextStep(
            next(CheckOrderStep(self.application, declaration)),
            ExistingDeclarationStep)

    def test_step_2(self):
        """Шаг 2. Сравнение данных заявления в ЭДС и данных в запросе."""
        #TODO: Падает ошибка TypeError: Object of type 'WorkType' is not JSON serializable
        # declaration = DeclarationF.create(
        #             children__firstname=self.application.ChildInfo.ChildName,
        #             children__surname=self.application.ChildInfo.ChildSurname
        # )
        # DUnitF(
        #     declaration=declaration,
        #     unit=self.unit
        # )
        #
        # next_step = next(
        #     ExistingDeclarationStep(
        #         self.application,
        #         declaration))
        # self.assertNextStep(next_step, Response)
        #
        # next_step = next(
        #     ExistingDeclarationStep(
        #         self.application,
        #         DeclarationF.create(children__firstname='A')))
        # self.assertNextStep(next_step, Response)

    def test_step_3(self):
        """Шаг 3. Валидация запроса и создание заявления."""
        declaration = DeclarationF.create()
        DUnitF(
            declaration=declaration,
            unit=self.unit
        )
        step = next(
            RequestValidationStep(self.application, declaration))
        self.assertNextStep(step, Response)
        self.assertEquals(step.status_code, CODE_OK)
        self.assertEquals(step.comment, _Message.SUCCESS)

        child_info = self.application.ChildInfo
        declaration = DeclarationF.create(
                children__firstname=child_info.ChildName,
                children__surname=child_info.ChildSurname,
                children__date_of_birth=child_info.ChildBirthDate,
                children__dul_series=(
                    child_info.ChildBirthDocRF.ChildBirthDocSeries),
                children__dul_number=(
                    child_info.ChildBirthDocRF.ChildBirthDocNumber),
                children__dul_date=(
                    child_info.ChildBirthDocRF.ChildBirthDocIssueDate))
        DUnitF(
            declaration=declaration,
            unit=self.unit
        )
        next_step = next(RequestValidationStep(
            self.application,
            declaration
        ))
        self.assertNextStep(next_step, Response)
        self.assertEquals(next_step.status_code, CODE_ERROR)
        self.assertEquals(next_step.comment, _Message.MULTIPLE)
