from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from m3.db import BaseEnumerate

from kinder.core.declaration.models import DeclarationPrivilege

from concentrator.constants import ConcentratorDelegateDocType


class DelegatePerson(models.Model):
    """Физ. лицо представителя"""

    doc_type = models.PositiveSmallIntegerField(
        choices=list(ConcentratorDelegateDocType.values.items()),
        verbose_name='Тип документа')
    delegate = models.OneToOneField(
        'children.Delegate', related_name='concentrator_delegate',
        null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Расширение модели Представителя'


class ChangeStatus(BaseEnumerate):
    """Статус изменения."""

    WAIT = 0
    REJECT = 1
    ACCEPT = 2

    values = {
        WAIT: 'Ожидает решения',
        REJECT: 'Отказано',
        ACCEPT: 'Исполнено',
    }


class ChangeSource(BaseEnumerate):
    """Источник изменений."""

    UPDATE_APPLICATION = 0
    NEW_APPLICATION = 1

    values = {
        UPDATE_APPLICATION: 'Обновление данных заявки',
        NEW_APPLICATION: 'Создание новой заявки'
    }


class ChangeDeclaration(models.Model):
    """Модель хранит список изменений по заявке."""

    create = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания изменения')
    declaration = models.ForeignKey(
        'declaration.Declaration', on_delete=models.CASCADE)
    data = models.TextField(verbose_name='Содержимое объекта', null=True)
    state = models.SmallIntegerField(
        choices=ChangeStatus.get_choices(),
        verbose_name='Статус изменений', default=ChangeStatus.WAIT)
    commentary = models.TextField(
        null=True, blank=True, verbose_name='Комментарий')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        verbose_name='Пользователь', on_delete=models.SET_NULL)
    source = models.SmallIntegerField(
        choices=ChangeSource.get_choices(),
        null=True, blank=True, default=ChangeSource.UPDATE_APPLICATION,
        verbose_name='Источник изменений')

    case_number = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Номер заявки')

    class Meta:
        verbose_name = 'Список изменений заявки с ЕПГУ'


class UpdateParams(models.Model):

    model_name = models.CharField(
        max_length=250, verbose_name='Наименование модели')
    field_name = models.CharField(
        max_length=250, verbose_name='Наименование поля')

    def clean(self):
        super().clean()

        if self.model_name is None:
            raise ValidationError(
                'Поле {} обязательно для заполнения'.format(
                    UpdateParams._meta.get_field('model_name').verbose_name))
        if self.field_name is None:
            raise ValidationError(
                'Поле {} обязательно для заполнения'.format(
                    UpdateParams._meta.get_field('field_name').verbose_name))

    class Meta:
        verbose_name = 'Параметры для изменения данных'
        unique_together = ('model_name', 'field_name')


class DocExtraInfo(models.Model):
    """Информация о файлах пришедших из концентратора."""

    declaration = models.ForeignKey(
        'declaration.Declaration', on_delete=models.CASCADE)
    code = models.CharField(max_length=350, verbose_name='Код')
    name = models.CharField(
        max_length=350, verbose_name='Имя',
        null=True, blank=True)
    description = models.CharField(
        max_length=350, null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Дополнительная информация о документах'


class PrivilegeComment(models.Model):
    """Комментарий к привилегии, пришедшей с концентратора."""

    declaration_privilege = models.OneToOneField(
        DeclarationPrivilege, on_delete=models.CASCADE,
        related_name='declaration_privilege', unique=True)
    concentrator_comment = models.TextField(
        null=True, verbose_name='Комментарий из концентратора')

    class Meta:
        verbose_name = 'Комментарий к льготе'
