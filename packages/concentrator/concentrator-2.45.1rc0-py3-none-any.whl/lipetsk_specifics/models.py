import os

from django.db import models
from django.dispatch import receiver
from kinder.core.audit_log_kndg.managers import AuditLog
from kinder.core.db import upload_file_handler
from kinder.core.declaration.models import Declaration
from kinder.core.models import LogableModel
from kinder.core.models import SimpleDictionary
from kinder.core.models import pre_safe_delete
from kinder.core.privilege.models import Privilege
from kinder.users.models import UserProfile
from m3.db import BaseEnumerate

from concentrator.models import ChangeDeclaration
from lipetsk_specifics.constants import DepartmentAttribute


class Department(SimpleDictionary):
    """
    Справочник "Ведомства"
    """
    # TODO: На самом деле, к одной льготе принадлежит только 1 ведомство,
    #  нужен ключ!!!
    privileges = models.ManyToManyField(Privilege)

    class Meta:
        verbose_name = u"Ведомства"


class DepartmentAttributes(LogableModel):
    """
    Атрибуты ведомства
    """

    department = models.ForeignKey(Department, null=False,
                                   on_delete=models.CASCADE)
    attribute = models.CharField(
        max_length=256,
        choices=DepartmentAttribute.get_choices(),
        verbose_name=u"Атрибут")

    audit_log = AuditLog()

    class Meta:
        verbose_name = u"Атрибуты ведомства"
        unique_together = ('department',
                           'attribute')


class PassingSmev(LogableModel):
    u"""Обращения в не электронные ведомства."""

    department = models.ForeignKey(Department, verbose_name=u'Ведомство',
                                   on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, verbose_name=u'Пользователь',
                                on_delete=models.CASCADE)
    request = models.FileField(
        u'Запрос', upload_to=upload_file_handler, max_length=150)
    time = models.DateTimeField(
        u'Дата и время', auto_now_add=True, db_index=True)
    result = models.FileField(
        u'Результат', upload_to=upload_file_handler, max_length=150, null=True,
        blank=True)

    @property
    def request_link(self):
        file_name, ext = os.path.splitext(self.request.name)
        return u'<a href="{0}" download="Запрос{1}">Запрос{1}</a>'.format(
            self.request.url, ext)

    @property
    def result_link(self):
        if not self.result:
            return

        file_name, ext = os.path.splitext(self.request.name)
        return u'<a href="{0}" download="Ответ{1}">Ответ{1}</a>'.format(
            self.result.url, ext)

    class Meta:
        verbose_name = u'Обращения в не электронные ведомства'


class DeclarationPassingSmev(LogableModel):
    u"""Привязка обращений в не электронные ведомства и заявлений."""

    passing_smev = models.ForeignKey(
        PassingSmev, verbose_name=u'Обращение в не электронные ведомства',
        on_delete=models.CASCADE)
    declaration = models.ForeignKey(
        Declaration, verbose_name=u'Заявление',
        on_delete=models.CASCADE)


class ReportType(BaseEnumerate):
    u"""Перечисление типов отчета.

    Используетсся в модели доп. атрибутов льготы.
    """

    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4

    values = {
        FIRST: 'ФИО, дата рождения, адрес, СНИЛС',
        SECOND: 'ФИО, дата рождения, место рождения, адрес, СНИЛС, '
                'наименование подразделения, '
                'в котором служит (служил) обладатель льготы, звание',
        THIRD: 'ФИО, дата рождения, место рождения, адрес, СНИЛС, '
               'ОВД, выдавшее удостоверение, звание',
        FOURTH: 'ФИО, дата рождения, личный номер, '
                'принадлежность к виду или роду войск, воинская часть, '
                'дата увольнения, документ, '
                'удостоверяющий личность, удостоверение, военный билет'
    }


class ExtendedPrivilege(LogableModel):
    u"""Модель дополнительных атрибутов льготы."""

    privilege = models.OneToOneField('privilege.Privilege',
                                     on_delete=models.CASCADE)
    name_to_query_at_depart = models.CharField(
        u'Наименования для запроса в ведомства',
        max_length=500, blank=True)

    report_type = models.IntegerField(u'Тип отчета',
                                      default=ReportType.FIRST,
                                      choices=ReportType.get_choices())


class Changes(models.Model):
    u"""
    Перечень ID concentrator.ChangeDeclaration, полученных от Липецкого сервиса
    """

    change_declaration = models.OneToOneField(
        ChangeDeclaration, on_delete=models.CASCADE,
        related_name='change_declaration', unique=True)


@receiver(pre_safe_delete, sender=Privilege)
def delete_privilege(sender, instance, **kwargs):
    u"""Удаляет связанные записи перед удалением льготы"""
    if hasattr(instance, 'extendedprivilege'):
        instance.extendedprivilege.delete()
