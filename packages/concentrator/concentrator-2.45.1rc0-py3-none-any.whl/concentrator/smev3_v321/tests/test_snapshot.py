from datetime import date
from unittest.mock import MagicMock

from django.conf import settings
from django.core.files import File
from educommon.contingent import catalogs

from kinder.test.base import BaseTC
from kinder.core.children.models import Children
from kinder.core.children.models import Delegate
from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.tests.factory_child import ChildF
from kinder.core.children.tests.factory_child import DelegateF
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationDoc
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.declaration.tests.factory_declaration import DUnitF
from kinder.core.declaration.tests.factory_declaration import DPrivilegeF
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import GroupOrientationDocuments
from kinder.core.dict.models import GroupSpec
from kinder.core.dict.models import GroupType
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.dict.models import HealthNeed
from kinder.core.dict.models import HealthNeedEnumerate
from kinder.core.dict.models import WorkType
from kinder.core.dict.models import WorkTypeEnumerate
from kinder.core.privilege.tests.factory_privilege import PrivilegeF
from kinder.core.unit.tests.factory_unit import UnitDouFactory
from kinder.core.unit.tests.factory_unit import UnitMoFactory
from kinder.plugins.contingent.models import DelegateContingent

from concentrator.smev3_v321.application_request.snapshot import DeclarationDocsSnapshotCreator
from concentrator.smev3_v321.application_request.snapshot import DeclarationPrivilegeSnapshotCreator
from concentrator.smev3_v321.application_request.snapshot import DeclarationSnapshotCreator
from concentrator.smev3_v321.application_request.snapshot import DeclarationUnitSnapshotCreator
from concentrator.smev3_v321.application_request.snapshot import DelegateSnapshotCreator
from concentrator.smev3_v321.application_request.snapshot import ChildSnapshotCreator


class DeclarationSnapshotTestCase(BaseTC):
    def setUp(self):
        self.desired_date_name = 'Заявление - Желаемая дата зачисления'
        self.desired_date_1 = date(2000, 1, 1)
        self.desired_date_2 = date(2000, 2, 1)

        self.work_type_name = 'Заявление - Время пребывания'
        self.work_type_1 = WorkType.objects.get(code=WorkTypeEnumerate.FULL)
        self.work_type_2 = WorkType.objects.get(code=WorkTypeEnumerate.EXTEND)
        
        self.spec_name = 'Заявление - Специфика'
        self.spec_1 = GroupSpec.objects.get(code=GroupSpec.TAT)
        self.spec_2 = GroupSpec.objects.get(code=GroupSpec.RUS)

        self.consent_full_time_group_name = 'Заявление - Согласие на группу полного дня'
        self.consent_full_time_group_1 = False
        self.consent_full_time_group_2 = True

        self.offer_other_name = 'Заявление - Предлагать другие варианты'
        self.offer_other_1 = True
        self.offer_other_2 = False

        self.consent_dev_group_name = 'Заявление - Согласие на общеразвивающую группу (вне зависимости от наличия ОВЗ)'
        self.consent_dev_group_1 = False
        self.consent_dev_group_2 = True

        self.consent_care_group_name = 'Заявление - Согласие на группу по присмотру и уходу'
        self.consent_care_group_1 = True
        self.consent_care_group_2 = False

        self.desired_group_type_name = 'Заявление - Желаемая направленность группы при зачислении'
        self.desired_group_type_1 = GroupType.objects.get(code=GroupTypeEnumerate.DEV)
        self.desired_group_type_2 = GroupType.objects.get(code=GroupTypeEnumerate.COMP)

        self.declaration = DeclarationF.create(
            desired_date=self.desired_date_1,
            work_type=self.work_type_1,
            spec=self.spec_1,
            consent_full_time_group=self.consent_full_time_group_1,
            offer_other=self.offer_other_1,
            consent_dev_group=self.consent_dev_group_1,
            consent_care_group=self.consent_care_group_1,
            desired_group_type=self.desired_group_type_1,
        )

    def test_declaration_create_changes(self):
        snapshot_creator = DeclarationSnapshotCreator(self.declaration.id)
        changes = snapshot_creator.created()

        self.assertCountEqual(
            changes,
            [
                {'field': self.desired_date_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.desired_date_1)},
                {'field': self.work_type_name, 'old_value': '-', 'new_value': self.work_type_1.name},
                {'field': self.spec_name, 'old_value': '-', 'new_value': self.spec_1.name},
                {'field': self.consent_full_time_group_name, 'old_value': '-', 'new_value': snapshot_creator._get_bool_repr(self.consent_full_time_group_1)},
                {'field': self.offer_other_name, 'old_value': '-', 'new_value': snapshot_creator._get_bool_repr(self.offer_other_1)},
                {'field': self.consent_dev_group_name, 'old_value': '-', 'new_value': snapshot_creator._get_bool_repr(self.consent_dev_group_1)},
                {'field': self.consent_care_group_name, 'old_value': '-', 'new_value': snapshot_creator._get_bool_repr(self.consent_care_group_1)},
                {'field': self.desired_group_type_name, 'old_value': '-', 'new_value': self.desired_group_type_1.name},
            ]
        )

    def test_declaration_delete_changes(self):
        snapshot_creator = DeclarationSnapshotCreator(self.declaration.id)
        snapshot = snapshot_creator.get_snapshot()
        changes = snapshot_creator.deleted(snapshot)
    
        self.assertCountEqual(
            changes,
            [
                {'field': self.desired_date_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.desired_date_1)},
                {'field': self.work_type_name, 'new_value': '-', 'old_value': self.work_type_1.name},
                {'field': self.spec_name, 'new_value': '-', 'old_value': self.spec_1.name},
                {'field': self.consent_full_time_group_name, 'new_value': '-', 'old_value': snapshot_creator._get_bool_repr(self.consent_full_time_group_1)},
                {'field': self.offer_other_name, 'new_value': '-', 'old_value': snapshot_creator._get_bool_repr(self.offer_other_1)},
                {'field': self.consent_dev_group_name, 'new_value': '-', 'old_value': snapshot_creator._get_bool_repr(self.consent_dev_group_1)},
                {'field': self.consent_care_group_name, 'new_value': '-', 'old_value': snapshot_creator._get_bool_repr(self.consent_care_group_1)},
                {'field': self.desired_group_type_name, 'new_value': '-', 'old_value': self.desired_group_type_1.name},
            ]
        )
    
    def test_declaration_updated_changes(self):
        snapshot_creator = DeclarationSnapshotCreator(self.declaration.id)
        snapshot = snapshot_creator.get_snapshot()

        Declaration.objects.filter(pk=self.declaration.id).update(
            desired_date=self.desired_date_2,
            work_type=self.work_type_2,
            spec=self.spec_2,
            consent_full_time_group=self.consent_full_time_group_2,
            offer_other=self.offer_other_2,
            consent_dev_group=self.consent_dev_group_2,
            consent_care_group=self.consent_care_group_2,
            desired_group_type=self.desired_group_type_2,
        )

        changes = snapshot_creator.updated(snapshot)
    
        self.assertCountEqual(
            changes,
            [
                {'field': self.desired_date_name, 'new_value': snapshot_creator._get_date_repr(self.desired_date_2), 'old_value': snapshot_creator._get_date_repr(self.desired_date_1)},
                {'field': self.work_type_name, 'new_value': self.work_type_2.name, 'old_value': self.work_type_1.name},
                {'field': self.spec_name, 'new_value': self.spec_2.name, 'old_value': self.spec_1.name},
                {'field': self.consent_full_time_group_name, 'new_value': snapshot_creator._get_bool_repr(self.consent_full_time_group_2), 'old_value': snapshot_creator._get_bool_repr(self.consent_full_time_group_1)},
                {'field': self.offer_other_name, 'new_value': snapshot_creator._get_bool_repr(self.offer_other_2), 'old_value': snapshot_creator._get_bool_repr(self.offer_other_1)},
                {'field': self.consent_dev_group_name, 'new_value': snapshot_creator._get_bool_repr(self.consent_dev_group_2), 'old_value': snapshot_creator._get_bool_repr(self.consent_dev_group_1)},
                {'field': self.consent_care_group_name, 'new_value': snapshot_creator._get_bool_repr(self.consent_care_group_2), 'old_value': snapshot_creator._get_bool_repr(self.consent_care_group_1)},
                {'field': self.desired_group_type_name, 'new_value': self.desired_group_type_2.name, 'old_value': self.desired_group_type_1.name},
            ]
        )


class ChildSnapshotTestCase(BaseTC):
    def setUp(self):
        self.child_firstname_name = 'Ребенок - Имя'
        self.child_firstname_1 = 'Иван_1'
        self.child_firstname_2 = 'Иван_2'

        self.child_surname_name = 'Ребенок - Фамилия'
        self.child_surname_1 = 'Иванов_1'
        self.child_surname_2 = 'Иванов_2'

        self.child_patronymic_name = 'Ребенок - Отчество'
        self.child_patronymic_1 = 'Иванович_1'
        self.child_patronymic_2 = 'Иванович_2'
        
        self.child_date_of_birth_name = 'Ребенок - Дата рождения'
        self.child_date_of_birth_1 = date(1996, 1, 1)
        self.child_date_of_birth_2 = date(1996, 2, 1)
        
        self.child_health_need_special_support_name = 'Ребенок - Нужны специальные меры поддержки'
        self.child_health_need_special_support_1 = False
        self.child_health_need_special_support_2 = True
        
        self.child_health_need_confirmation_name = 'Ребенок - Документ, подтверждающий специфику'
        self.child_health_need_confirmation_1 = GroupOrientationDocuments.objects.first()
        self.child_health_need_confirmation_2 = GroupOrientationDocuments.objects.last()
        
        self.child_health_series_name = 'Ребенок - Серия'
        self.child_health_series_1 = 'Серия_1'
        self.child_health_series_2 = 'Серия_2'
        
        self.child_health_number_name = 'Ребенок - Номер'
        self.child_health_number_1 = 'Номер_1'
        self.child_health_number_2 = 'Номер_2'
        
        self.child_health_need_start_date_name = 'Ребенок - Дата выдачи'
        self.child_health_need_start_date_1 = date(2000, 1, 1)
        self.child_health_need_start_date_2 = date(2000, 2, 1)
        
        self.child_health_issued_by_name = 'Ребенок - Кем выдан'
        self.child_health_issued_by_1 = 'Выдан_1'
        self.child_health_issued_by_2 = 'Выдан_2'
        
        self.child_health_need_expiration_date_name = 'Ребенок - Срок действия'
        self.child_health_need_expiration_date_1 = date(2001, 1, 1)
        self.child_health_need_expiration_date_2 = date(2001, 2, 1)
        
        self.child_dul_series_name = 'Ребенок - Серия'
        self.child_dul_series_1 = 'СЕРИЯ_1'
        self.child_dul_series_2 = 'СЕРИЯ_2'
        
        self.child_dul_number_name = 'Ребенок - Номер'
        self.child_dul_number_1 = 'Номер_1'
        self.child_dul_number_2 = 'Номер_2'
        
        self.child_dul_date_name = 'Ребенок - Дата выдачи'
        self.child_dul_date_1 = date(1997, 1, 2)
        self.child_dul_date_2 = date(1997, 2, 2)
        
        self.child_zags_act_number_name = 'Ребенок - Номер актовой записи'
        self.child_zags_act_number_1 = 'Номер_1'
        self.child_zags_act_number_2 = 'Номер_2'
        
        self.child_zags_act_place_name = 'Ребенок - Место государственной регистрации (отдел ЗАГС)'
        self.child_zags_act_place_1 = 'Место_1'
        self.child_zags_act_place_2 = 'Место_2'
        
        self.child_zags_act_date_name = 'Ребенок - Дата создания актовой записи'
        self.child_zags_act_date_1 = date(1997, 1, 2)
        self.child_zags_act_date_2 = date(1997, 2, 2)
        
        self.child_health_need_name = 'Ребенок - Специфика'
        self.child_health_need_1 = HealthNeed.objects.get(code=HealthNeedEnumerate.NOT)
        self.child_health_need_2 = HealthNeed.objects.get(code=HealthNeedEnumerate.OTHER)

        self.child = ChildF.create(
            firstname=self.child_firstname_1,
            surname=self.child_surname_1,
            patronymic=self.child_patronymic_1,
            date_of_birth=self.child_date_of_birth_1,
            health_need_special_support=self.child_health_need_special_support_1,
            health_need_confirmation=self.child_health_need_confirmation_1,
            health_series=self.child_health_series_1,
            health_number=self.child_health_number_1,
            health_need_start_date=self.child_health_need_start_date_1,
            health_issued_by=self.child_health_issued_by_1,
            health_need_expiration_date=self.child_health_need_expiration_date_1,
            dul_series=self.child_dul_series_1,
            dul_number=self.child_dul_number_1,
            dul_date=self.child_dul_date_1,
            zags_act_number=self.child_zags_act_number_1,
            zags_act_place=self.child_zags_act_place_1,
            zags_act_date=self.child_zags_act_date_1,
            health_need=self.child_health_need_1,
        )

    def test_child_create_changes(self):
        snapshot_creator = ChildSnapshotCreator(self.child.id)
        changes = snapshot_creator.created()

        self.assertCountEqual(
            changes,
            [
                {'field': self.child_firstname_name, 'old_value': '-', 'new_value': self.child_firstname_1},
                {'field': self.child_surname_name, 'old_value': '-', 'new_value': self.child_surname_1},
                {'field': self.child_patronymic_name, 'old_value': '-', 'new_value': self.child_patronymic_1},
                {'field': self.child_date_of_birth_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.child_date_of_birth_1)},
                {'field': self.child_health_need_special_support_name, 'old_value': '-', 'new_value': snapshot_creator._get_bool_repr(self.child_health_need_special_support_1)},
                {'field': self.child_health_need_confirmation_name, 'old_value': '-', 'new_value': self.child_health_need_confirmation_1.name},
                {'field': self.child_health_series_name, 'old_value': '-', 'new_value': self.child_health_series_1},
                {'field': self.child_health_number_name, 'old_value': '-', 'new_value': self.child_health_number_1},
                {'field': self.child_health_need_start_date_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.child_health_need_start_date_1)},
                {'field': self.child_health_issued_by_name, 'old_value': '-', 'new_value': self.child_health_issued_by_1},
                {'field': self.child_health_need_expiration_date_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.child_health_need_expiration_date_1)},
                {'field': self.child_dul_series_name, 'old_value': '-', 'new_value': self.child_dul_series_1},
                {'field': self.child_dul_number_name, 'old_value': '-', 'new_value': self.child_dul_number_1},
                {'field': self.child_dul_date_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.child_dul_date_1)},
                {'field': self.child_zags_act_number_name, 'old_value': '-', 'new_value': self.child_zags_act_number_1},
                {'field': self.child_zags_act_place_name, 'old_value': '-', 'new_value': self.child_zags_act_place_1},
                {'field': self.child_zags_act_date_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.child_zags_act_date_1)},
                {'field': self.child_health_need_name, 'old_value': '-', 'new_value': self.child_health_need_1.name},
            ]
        )

    def test_child_delete_changes(self):
        snapshot_creator = ChildSnapshotCreator(self.child.id)
        snapshot = snapshot_creator.get_snapshot()
        changes = snapshot_creator.deleted(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.child_firstname_name, 'new_value': '-', 'old_value': self.child_firstname_1},
                {'field': self.child_surname_name, 'new_value': '-', 'old_value': self.child_surname_1},
                {'field': self.child_patronymic_name, 'new_value': '-', 'old_value': self.child_patronymic_1},
                {'field': self.child_date_of_birth_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.child_date_of_birth_1)},
                {'field': self.child_health_need_special_support_name, 'new_value': '-', 'old_value': snapshot_creator._get_bool_repr(self.child_health_need_special_support_1)},
                {'field': self.child_health_need_confirmation_name, 'new_value': '-', 'old_value': self.child_health_need_confirmation_1.name},
                {'field': self.child_health_series_name, 'new_value': '-', 'old_value': self.child_health_series_1},
                {'field': self.child_health_number_name, 'new_value': '-', 'old_value': self.child_health_number_1},
                {'field': self.child_health_need_start_date_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.child_health_need_start_date_1)},
                {'field': self.child_health_issued_by_name, 'new_value': '-', 'old_value': self.child_health_issued_by_1},
                {'field': self.child_health_need_expiration_date_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.child_health_need_expiration_date_1)},
                {'field': self.child_dul_series_name, 'new_value': '-', 'old_value': self.child_dul_series_1},
                {'field': self.child_dul_number_name, 'new_value': '-', 'old_value': self.child_dul_number_1},
                {'field': self.child_dul_date_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.child_dul_date_1)},
                {'field': self.child_zags_act_number_name, 'new_value': '-', 'old_value': self.child_zags_act_number_1},
                {'field': self.child_zags_act_place_name, 'new_value': '-', 'old_value': self.child_zags_act_place_1},
                {'field': self.child_zags_act_date_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.child_zags_act_date_1)},
                {'field': self.child_health_need_name, 'new_value': '-', 'old_value': self.child_health_need_1.name},
            ]
        )

    def test_child_update_changes(self):
        snapshot_creator = ChildSnapshotCreator(self.child.id)
        snapshot = snapshot_creator.get_snapshot()

        Children.objects.filter(pk=self.child.id).update(
            firstname=self.child_firstname_2,
            surname=self.child_surname_2,
            patronymic=self.child_patronymic_2,
            date_of_birth=self.child_date_of_birth_2,
            health_need_special_support=self.child_health_need_special_support_2,
            health_need_confirmation=self.child_health_need_confirmation_2,
            health_series=self.child_health_series_2,
            health_number=self.child_health_number_2,
            health_need_start_date=self.child_health_need_start_date_2,
            health_issued_by=self.child_health_issued_by_2,
            health_need_expiration_date=self.child_health_need_expiration_date_2,
            dul_series=self.child_dul_series_2,
            dul_number=self.child_dul_number_2,
            dul_date=self.child_dul_date_2,
            zags_act_number=self.child_zags_act_number_2,
            zags_act_place=self.child_zags_act_place_2,
            zags_act_date=self.child_zags_act_date_2,
            health_need=self.child_health_need_2,
        )

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.child_firstname_name, 'new_value': self.child_firstname_2, 'old_value': self.child_firstname_1},
                {'field': self.child_surname_name, 'new_value': self.child_surname_2, 'old_value': self.child_surname_1},
                {'field': self.child_patronymic_name, 'new_value': self.child_patronymic_2, 'old_value': self.child_patronymic_1},
                {'field': self.child_date_of_birth_name, 'new_value': snapshot_creator._get_date_repr(self.child_date_of_birth_2), 'old_value': snapshot_creator._get_date_repr(self.child_date_of_birth_1)},
                {'field': self.child_health_need_special_support_name, 'new_value': snapshot_creator._get_bool_repr(self.child_health_need_special_support_2), 'old_value': snapshot_creator._get_bool_repr(self.child_health_need_special_support_1)},
                {'field': self.child_health_need_confirmation_name, 'new_value': self.child_health_need_confirmation_2.name, 'old_value': self.child_health_need_confirmation_1.name},
                {'field': self.child_health_series_name, 'new_value': self.child_health_series_2, 'old_value': self.child_health_series_1},
                {'field': self.child_health_number_name, 'new_value': self.child_health_number_2, 'old_value': self.child_health_number_1},
                {'field': self.child_health_need_start_date_name, 'new_value': snapshot_creator._get_date_repr(self.child_health_need_start_date_2), 'old_value': snapshot_creator._get_date_repr(self.child_health_need_start_date_1)},
                {'field': self.child_health_issued_by_name, 'new_value': self.child_health_issued_by_2, 'old_value': self.child_health_issued_by_1},
                {'field': self.child_health_need_expiration_date_name, 'new_value': snapshot_creator._get_date_repr(self.child_health_need_expiration_date_2), 'old_value': snapshot_creator._get_date_repr(self.child_health_need_expiration_date_1)},
                {'field': self.child_dul_series_name, 'new_value': self.child_dul_series_2, 'old_value': self.child_dul_series_1},
                {'field': self.child_dul_number_name, 'new_value': self.child_dul_number_2, 'old_value': self.child_dul_number_1},
                {'field': self.child_dul_date_name, 'new_value': snapshot_creator._get_date_repr(self.child_dul_date_2), 'old_value': snapshot_creator._get_date_repr(self.child_dul_date_1)},
                {'field': self.child_zags_act_number_name, 'new_value': self.child_zags_act_number_2, 'old_value': self.child_zags_act_number_1},
                {'field': self.child_zags_act_place_name, 'new_value': self.child_zags_act_place_2, 'old_value': self.child_zags_act_place_1},
                {'field': self.child_zags_act_date_name, 'new_value': snapshot_creator._get_date_repr(self.child_zags_act_date_2), 'old_value': snapshot_creator._get_date_repr(self.child_zags_act_date_1)},
                {'field': self.child_health_need_name, 'new_value': self.child_health_need_2.name, 'old_value': self.child_health_need_1.name},
            ]
        )


class DelegateSnapshotTestCase(BaseTC):
    def setUp(self):
        self.delegate_firstname_name = 'Представитель - Имя'
        self.delegate_firstname_1 = 'Мария_1'
        self.delegate_firstname_2 = 'Иван_2'

        self.delegate_surname_name = 'Представитель - Фамилия'
        self.delegate_surname_1 = 'Иванова_1'
        self.delegate_surname_2 = 'Иванов_2'
        
        self.delegate_patronymic_name = 'Представитель - Отчество'
        self.delegate_patronymic_1 = 'Ивановна_1'
        self.delegate_patronymic_2 = 'Иванович_2'
        
        self.delegate_dul_type_name = 'Представитель - Тип документа'
        self.delegate_dul_type_1 = DULDelegateType.objects.get(pk=DULDelegateType.BIRTH_CERTIFICATE)
        self.delegate_dul_type_2 = DULDelegateType.objects.get(pk=DULDelegateType.RF_PASSPORT)
        
        self.delegate_dul_series_name = 'Представитель - Серия'
        self.delegate_dul_series_1 = 'Серия_1'
        self.delegate_dul_series_2 = 'Серия_2'
        
        self.delegate_dul_number_name = 'Представитель - Номер'
        self.delegate_dul_number_1 = 'Номер_1'
        self.delegate_dul_number_2 = 'Номер_2'
        
        self.delegate_dul_issued_by_name = 'Представитель - Кем выдан'
        self.delegate_dul_issued_by_1 = 'Выдан_1'
        self.delegate_dul_issued_by_2 = 'Выдан_2'
        
        self.delegate_dul_date_name = 'Представитель - Дата выдачи'
        self.delegate_dul_date_1 = date(1970, 1, 1)
        self.delegate_dul_date_2 = date(1970, 2, 1)
        
        self.delegate_email_name = 'Представитель - E-mail'
        self.delegate_email_1 = 'E-mail_1'
        self.delegate_email_2 = 'E-mail_2'
        
        self.delegate_phones_name = 'Представитель - Телефоны'
        self.delegate_phones_1 = 'Телефон_1'
        self.delegate_phones_2 = 'Телефон_2'
        
        self.delegate_type_name = 'Представитель - Тип представителя'
        self.delegate_type_1 = DelegateTypeEnumerate.MOTHER
        self.delegate_type_2 = DelegateTypeEnumerate.FATHER

        self.delegate_contingent_doc_type_name = 'Представитель - Тип документа, подтверждающего права'
        self.delegate_contingent_doc_type_1 = catalogs.DocumentConfirmingTypes.BIRTH_CERT
        self.delegate_contingent_doc_type_2 = catalogs.DocumentConfirmingTypes.OTHER_DOC
        
        self.delegate_contingent_series_name = 'Представитель - Серия'
        self.delegate_contingent_series_1 = 'Серия_1'
        self.delegate_contingent_series_2 = 'Серия_2'
        
        self.delegate_contingent_number_name = 'Представитель - Номер'
        self.delegate_contingent_number_1 = 'Номер_1'
        self.delegate_contingent_number_2 = 'Номер_2'
        
        self.delegate_contingent_date_issue_name = 'Представитель - Дата выдачи'
        self.delegate_contingent_date_issue_1 = date(1997, 1, 1)
        self.delegate_contingent_date_issue_2 = date(1997, 2, 1)
        
        self.delegate_contingent_issued_by_name = 'Представитель - Кем выдан'
        self.delegate_contingent_issued_by_1 = 'Выдан_1'
        self.delegate_contingent_issued_by_2 = 'Выдан_2'

        self.delegate = DelegateF.create(
            firstname=self.delegate_firstname_1,
            surname=self.delegate_surname_1,
            patronymic=self.delegate_patronymic_1,
            dul_type=self.delegate_dul_type_1,
            dul_series=self.delegate_dul_series_1,
            dul_number=self.delegate_dul_number_1,
            dul_issued_by=self.delegate_dul_issued_by_1,
            dul_date=self.delegate_dul_date_1,
            email=self.delegate_email_1,
            phones=self.delegate_phones_1,
            type=self.delegate_type_1,
        )

        self.delegate_contingent = DelegateContingent.objects.create(
            delegate=self.delegate,
            doc_type=self.delegate_contingent_doc_type_1,
            series=self.delegate_contingent_series_1,
            number=self.delegate_contingent_number_1,
            date_issue=self.delegate_contingent_date_issue_1,
            issued_by=self.delegate_contingent_issued_by_1,
        )

    def test_delegate_create_changes(self):
        snapshot_creator = DelegateSnapshotCreator(self.delegate.id)
        changes = snapshot_creator.created()

        self.assertCountEqual(
            changes,
            [
                {'field': self.delegate_firstname_name, 'old_value': '-', 'new_value': self.delegate_firstname_1},
                {'field': self.delegate_surname_name, 'old_value': '-', 'new_value': self.delegate_surname_1},
                {'field': self.delegate_patronymic_name, 'old_value': '-', 'new_value': self.delegate_patronymic_1},
                {'field': self.delegate_dul_type_name, 'old_value': '-', 'new_value': self.delegate_dul_type_1.name},
                {'field': self.delegate_dul_series_name, 'old_value': '-', 'new_value': self.delegate_dul_series_1},
                {'field': self.delegate_dul_number_name, 'old_value': '-', 'new_value': self.delegate_dul_number_1},
                {'field': self.delegate_dul_issued_by_name, 'old_value': '-', 'new_value': self.delegate_dul_issued_by_1},
                {'field': self.delegate_dul_date_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.delegate_dul_date_1)},
                {'field': self.delegate_email_name, 'old_value': '-', 'new_value': self.delegate_email_1},
                {'field': self.delegate_phones_name, 'old_value': '-', 'new_value': self.delegate_phones_1},
                {'field': self.delegate_type_name, 'old_value': '-', 'new_value': DelegateTypeEnumerate.values[self.delegate_type_1]},
                {'field': self.delegate_contingent_doc_type_name, 'old_value': '-', 'new_value': catalogs.DocumentConfirmingTypes.values[self.delegate_contingent_doc_type_1]},
                {'field': self.delegate_contingent_series_name, 'old_value': '-', 'new_value': self.delegate_contingent_series_1},
                {'field': self.delegate_contingent_number_name, 'old_value': '-', 'new_value': self.delegate_contingent_number_1},
                {'field': self.delegate_contingent_date_issue_name, 'old_value': '-', 'new_value': snapshot_creator._get_date_repr(self.delegate_contingent_date_issue_1)},
                {'field': self.delegate_contingent_issued_by_name, 'old_value': '-', 'new_value': self.delegate_contingent_issued_by_1},
            ]
        )

    def test_delegate_delete_changes(self):
        snapshot_creator = DelegateSnapshotCreator(self.delegate.id)
        snapshot = snapshot_creator.get_snapshot()
        changes = snapshot_creator.deleted(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.delegate_firstname_name, 'new_value': '-', 'old_value': self.delegate_firstname_1},
                {'field': self.delegate_surname_name, 'new_value': '-', 'old_value': self.delegate_surname_1},
                {'field': self.delegate_patronymic_name, 'new_value': '-', 'old_value': self.delegate_patronymic_1},
                {'field': self.delegate_dul_type_name, 'new_value': '-', 'old_value': self.delegate_dul_type_1.name},
                {'field': self.delegate_dul_series_name, 'new_value': '-', 'old_value': self.delegate_dul_series_1},
                {'field': self.delegate_dul_number_name, 'new_value': '-', 'old_value': self.delegate_dul_number_1},
                {'field': self.delegate_dul_issued_by_name, 'new_value': '-', 'old_value': self.delegate_dul_issued_by_1},
                {'field': self.delegate_dul_date_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.delegate_dul_date_1)},
                {'field': self.delegate_email_name, 'new_value': '-', 'old_value': self.delegate_email_1},
                {'field': self.delegate_phones_name, 'new_value': '-', 'old_value': self.delegate_phones_1},
                {'field': self.delegate_type_name, 'new_value': '-', 'old_value': DelegateTypeEnumerate.values[self.delegate_type_1]},
                {'field': self.delegate_contingent_doc_type_name, 'new_value': '-', 'old_value': catalogs.DocumentConfirmingTypes.values[self.delegate_contingent_doc_type_1]},
                {'field': self.delegate_contingent_series_name, 'new_value': '-', 'old_value': self.delegate_contingent_series_1},
                {'field': self.delegate_contingent_number_name, 'new_value': '-', 'old_value': self.delegate_contingent_number_1},
                {'field': self.delegate_contingent_date_issue_name, 'new_value': '-', 'old_value': snapshot_creator._get_date_repr(self.delegate_contingent_date_issue_1)},
                {'field': self.delegate_contingent_issued_by_name, 'new_value': '-', 'old_value': self.delegate_contingent_issued_by_1},
            ]
        )

    def test_delegate_update_changes(self):
        snapshot_creator = DelegateSnapshotCreator(self.delegate.id)
        snapshot = snapshot_creator.get_snapshot()

        Delegate.objects.filter(pk=self.delegate.id).update(
            firstname=self.delegate_firstname_2,
            surname=self.delegate_surname_2,
            patronymic=self.delegate_patronymic_2,
            dul_type=self.delegate_dul_type_2,
            dul_series=self.delegate_dul_series_2,
            dul_number=self.delegate_dul_number_2,
            dul_issued_by=self.delegate_dul_issued_by_2,
            dul_date=self.delegate_dul_date_2,
            email=self.delegate_email_2,
            phones=self.delegate_phones_2,
            type=self.delegate_type_2,
        )

        DelegateContingent.objects.filter(delegate_id=self.delegate.id).update(
            doc_type=self.delegate_contingent_doc_type_2,
            series=self.delegate_contingent_series_2,
            number=self.delegate_contingent_number_2,
            date_issue=self.delegate_contingent_date_issue_2,
            issued_by=self.delegate_contingent_issued_by_2,
        )

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.delegate_firstname_name, 'new_value': self.delegate_firstname_2, 'old_value': self.delegate_firstname_1},
                {'field': self.delegate_surname_name, 'new_value': self.delegate_surname_2, 'old_value': self.delegate_surname_1},
                {'field': self.delegate_patronymic_name, 'new_value': self.delegate_patronymic_2, 'old_value': self.delegate_patronymic_1},
                {'field': self.delegate_dul_type_name, 'new_value': self.delegate_dul_type_2.name, 'old_value': self.delegate_dul_type_1.name},
                {'field': self.delegate_dul_series_name, 'new_value': self.delegate_dul_series_2, 'old_value': self.delegate_dul_series_1},
                {'field': self.delegate_dul_number_name, 'new_value': self.delegate_dul_number_2, 'old_value': self.delegate_dul_number_1},
                {'field': self.delegate_dul_issued_by_name, 'new_value': self.delegate_dul_issued_by_2, 'old_value': self.delegate_dul_issued_by_1},
                {'field': self.delegate_dul_date_name, 'new_value': snapshot_creator._get_date_repr(self.delegate_dul_date_2), 'old_value': snapshot_creator._get_date_repr(self.delegate_dul_date_1)},
                {'field': self.delegate_email_name, 'new_value': self.delegate_email_2, 'old_value': self.delegate_email_1},
                {'field': self.delegate_phones_name, 'new_value': self.delegate_phones_2, 'old_value': self.delegate_phones_1},
                {'field': self.delegate_type_name, 'new_value': DelegateTypeEnumerate.values[self.delegate_type_2], 'old_value': DelegateTypeEnumerate.values[self.delegate_type_1]},
                {'field': self.delegate_contingent_doc_type_name, 'new_value': catalogs.DocumentConfirmingTypes.values[self.delegate_contingent_doc_type_2], 'old_value': catalogs.DocumentConfirmingTypes.values[self.delegate_contingent_doc_type_1]},
                {'field': self.delegate_contingent_series_name, 'new_value': self.delegate_contingent_series_2, 'old_value': self.delegate_contingent_series_1},
                {'field': self.delegate_contingent_number_name, 'new_value': self.delegate_contingent_number_2, 'old_value': self.delegate_contingent_number_1},
                {'field': self.delegate_contingent_date_issue_name, 'new_value': snapshot_creator._get_date_repr(self.delegate_contingent_date_issue_2), 'old_value': snapshot_creator._get_date_repr(self.delegate_contingent_date_issue_1)},
                {'field': self.delegate_contingent_issued_by_name, 'new_value': self.delegate_contingent_issued_by_2, 'old_value': self.delegate_contingent_issued_by_1},
            ]
        )


class DeclarationUnitTestCase(BaseTC):
    def setUp(self):
        self.unit_name = 'Желаемые организации - Организация'
        self.unit_1 = UnitDouFactory.create()
        self.unit_2 = UnitDouFactory.create()

        self.ord_name = 'Желаемые организации - Приоритет'
        self.ord_1 = 1
        self.ord_2 = 2

        self.sibling_name = 'Желаемые организации - Посещает брат/сестра'
        self.sibling_1 = ChildF.create(
            firstname='Брат_1',
            surname='Иванов_1',
            patronymic='Иванович_1',
        )
        self.sibling_2 = ChildF.create(
            firstname='Брат_2',
            surname='Иванов_2',
            patronymic='Иванович_2',
        )

        self.declaration_unit = DUnitF.create(
            unit=self.unit_1,
            ord=self.ord_1,
            sibling=self.sibling_1
        )

    def test_declaration_unit_create_changes(self):
        snapshot_creator = DeclarationUnitSnapshotCreator(self.declaration_unit.id)
        changes = snapshot_creator.created()

        self.assertCountEqual(
            changes,
            [
                {'field': self.unit_name, 'old_value': '-', 'new_value': self.unit_1.name},
                {'field': f'{self.ord_name} ({self.unit_1.name})', 'old_value': '-', 'new_value': self.ord_1},
                {'field': f'{self.sibling_name} ({self.unit_1.name})', 'old_value': '-', 'new_value': self.sibling_1.fullname},
            ]
        )

    def test_declaration_unit_delete_changes(self):
        snapshot_creator = DeclarationUnitSnapshotCreator(self.declaration_unit.id)
        snapshot = snapshot_creator.get_snapshot()
        changes = snapshot_creator.deleted(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.unit_name, 'new_value': '-', 'old_value': self.unit_1.name},
                {'field': f'{self.ord_name} ({self.unit_1.name})', 'new_value': '-', 'old_value': self.ord_1},
                {'field': f'{self.sibling_name} ({self.unit_1.name})', 'new_value': '-', 'old_value': self.sibling_1.fullname},
            ]
        )

    def test_declaration_unit_update_changes(self):
        snapshot_creator = DeclarationUnitSnapshotCreator(self.declaration_unit.id)
        snapshot = snapshot_creator.get_snapshot()

        DeclarationUnit.objects.filter(pk=self.declaration_unit.id).update(
            unit=self.unit_2,
            ord=self.ord_2,
            sibling=self.sibling_2,
        )

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.unit_name, 'new_value': self.unit_2.name, 'old_value': self.unit_1.name},
                {'field': f'{self.ord_name} ({self.unit_2.name})', 'new_value': self.ord_2, 'old_value': self.ord_1},
                {'field': f'{self.sibling_name} ({self.unit_2.name})', 'new_value': self.sibling_2.fullname, 'old_value': self.sibling_1.fullname},
            ]
        )


class DeclarationPrivilegeSnapshotTestCase(BaseTC):
    def setUp(self):
        self.privilege_name = 'Льготы по заявке - Льгота'
        self.privilege_1 = PrivilegeF.create(name='Льгота_1')

        self.privilege_1_privilege_end_date=date(2001, 1, 1)
        self.privilege_1_repr = (
            f'{self.privilege_1.name}, '
            f'-, -, '
            f'{self.privilege_1_privilege_end_date.strftime(settings.DATE_FORMAT)}'
        )

        self.privilege_2 = PrivilegeF.create(name='Льгота_2')

        self.privilege_2_doc_issued_by='Выдан_2',
        self.privilege_2_doc_date=date(1997, 1, 1)
        self.privilege_2_privilege_end_date=date(2001, 1, 1)
        self.privilege_2_repr = (
            f'{self.privilege_2.name}, '
            f'{self.privilege_2_doc_issued_by}, '
            f'{self.privilege_2_doc_date.strftime(settings.DATE_FORMAT)}, '
            f'{self.privilege_2_privilege_end_date.strftime(settings.DATE_FORMAT)}'
        )

        self.declaration_privilege = DPrivilegeF.create(
            privilege=self.privilege_1,
            _privilege_end_date=self.privilege_1_privilege_end_date,
        )

    def test_declaration_privilege_create_changes(self):
        snapshot_creator = DeclarationPrivilegeSnapshotCreator(self.declaration_privilege.id)
        changes = snapshot_creator.created()

        self.assertCountEqual(
            changes,
            [
                {'field': self.privilege_name, 'old_value': '-', 'new_value': self.privilege_1_repr}
            ]
        )

    def test_declaration_privilege_delete_changes(self):
        snapshot_creator = DeclarationPrivilegeSnapshotCreator(self.declaration_privilege.id)
        snaphost = snapshot_creator.get_snapshot()
        changes = snapshot_creator.deleted(snaphost)

        self.assertCountEqual(
            changes,
            [
                {'field': self.privilege_name, 'new_value': '-', 'old_value': self.privilege_1_repr}
            ]
        )

    def test_declaration_privilege_update_changes(self):
        snapshot_creator = DeclarationPrivilegeSnapshotCreator(self.declaration_privilege.id)
        snaphost = snapshot_creator.get_snapshot()

        DeclarationPrivilege.objects.filter(pk=self.declaration_privilege.id).update(
            privilege=self.privilege_2,
            doc_issued_by=self.privilege_2_doc_issued_by,
            doc_date=self.privilege_2_doc_date,
            _privilege_end_date=self.privilege_2_privilege_end_date,
        )

        changes = snapshot_creator.updated(snaphost)

        self.assertCountEqual(
            changes,
            [
                {'field': self.privilege_name, 'new_value': self.privilege_2_repr, 'old_value': self.privilege_1_repr}
            ]
        )


class DeclarationDocsSnapshotTestCase(BaseTC):
    def setUp(self):
        self.declaration = DeclarationF.create()

        self.declaration_doc_name = 'Заявление - Список документов'
        self.declaration_doc_1_name = 'test_1.txt'
        self.declaration_doc_2_name = 'test_2.txt'
    
    def _mock_file(self, name):
        file_mock = MagicMock(spec=File, name='FileMock')
        file_mock.name = name

        return file_mock

    def test_declaration_doc_no_changes(self):
        snapshot_creator = DeclarationDocsSnapshotCreator(self.declaration.id)
        DeclarationDoc.objects.create(
            declaration=self.declaration,
            name=self.declaration_doc_1_name,
            file=self._mock_file(self.declaration_doc_1_name)
        )

        snapshot = snapshot_creator.get_snapshot()
        changes = snapshot_creator.updated(snapshot)

        self.assertFalse(changes)

    def test_declaration_doc_add_changes(self):
        snapshot_creator = DeclarationDocsSnapshotCreator(self.declaration.id)
        snapshot = snapshot_creator.get_snapshot()

        DeclarationDoc.objects.create(
            declaration=self.declaration,
            name=self.declaration_doc_1_name,
            file=self._mock_file(self.declaration_doc_1_name)
        )

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.declaration_doc_name, 'old_value': '-', 'new_value': ', '.join([self.declaration_doc_1_name])}
            ]
        )

        snapshot = snapshot_creator.get_snapshot()

        DeclarationDoc.objects.create(
            declaration=self.declaration,
            name=self.declaration_doc_2_name,
            file=self._mock_file(self.declaration_doc_2_name)
        )

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.declaration_doc_name, 'old_value': ', '.join([self.declaration_doc_1_name]), 'new_value': ', '.join([self.declaration_doc_1_name, self.declaration_doc_2_name])}
            ]
        )

    def test_declaration_doc_remove_changes(self):
        snapshot_creator = DeclarationDocsSnapshotCreator(self.declaration.id)

        doc_1 = DeclarationDoc.objects.create(
            declaration=self.declaration,
            name=self.declaration_doc_1_name,
            file=self._mock_file(self.declaration_doc_1_name)
        )

        doc_2 = DeclarationDoc.objects.create(
            declaration=self.declaration,
            name=self.declaration_doc_2_name,
            file=self._mock_file(self.declaration_doc_2_name)
        )
    
        snapshot = snapshot_creator.get_snapshot()

        doc_2.delete()

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.declaration_doc_name, 'new_value': ', '.join([self.declaration_doc_1_name]), 'old_value': ', '.join([self.declaration_doc_1_name, self.declaration_doc_2_name])}
            ]
        )

        snapshot = snapshot_creator.get_snapshot()

        doc_1.delete()

        changes = snapshot_creator.updated(snapshot)

        self.assertCountEqual(
            changes,
            [
                {'field': self.declaration_doc_name, 'new_value': '-', 'old_value': ', '.join([self.declaration_doc_1_name])}
            ]
        )
