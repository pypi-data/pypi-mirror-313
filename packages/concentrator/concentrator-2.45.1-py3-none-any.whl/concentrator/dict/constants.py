# coding:
# utf-8

"""
Created on 19.09.14

@author: kasimova
"""

from m3.db import BaseEnumerate


class OperationEnumerate(BaseEnumerate):
    """
    тип операции
    """
    ADD = 'Add'
    UPDATE = 'Update'
    DELETE = 'Delete'
    values = {
        ADD: u'Добавление',
        UPDATE: u'Изменение',
        DELETE: u'Удаление'
    }


class ModelForSend(BaseEnumerate):
    """
    Модель для отправки
    """
    GROUP = 'GroupAgeSubCathegoryProxy'
    HEALTH = 'HealthNeedProxy'
    PRIVILEGE = 'PrivilegeProxy'
    UNIT = 'UnitProxy'
    STAT = 'GroupStatisticProxy'
    values = {
        GROUP: u'ДОО.ВозрастнаяГруппа',
        HEALTH: u'ДОО.СпецификаГрупп',
        PRIVILEGE: u'Льготы.ДОО.Региональные',
        UNIT: u'Организации.ДОО.Региональные',
        STAT: u'Статистика.ВозрастнаяГруппа',
    }
