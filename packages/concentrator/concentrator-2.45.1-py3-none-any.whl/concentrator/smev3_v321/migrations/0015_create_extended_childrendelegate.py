from django.db import migrations
from django.db.models import Count
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models import Q

from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration.enum import DeclPortalEnum
from kinder.core.declaration_status.enum import DSS


def forwards(apps, schema_editor):
    """Создание связи для представителей ребенка в заявках СМЭВ 3."""

    ChildrenDelegate = apps.get_model('children', 'ChildrenDelegate')
    Declaration = apps.get_model('declaration', 'Declaration')
    ExtendedChildrenDelegate = (
        apps.get_model('smev3_v321', 'ExtendedChildrenDelegate'))

    # Активные заявления СМЭВ 3 Концентратора, у которых у ребенка указан
    # один представитель. Считает, что он был получен при создании
    # заявления в сервисе приема заявок и будет обновлять именно его.
    declarations = Declaration.objects.annotate(
        exists_gte_2_delegate=Exists(
            ChildrenDelegate.objects.filter(
                children_id=OuterRef('children_id')
            ).values(
                'children_id'
            ).annotate(
                delegate_count=Count('id')
            ).filter(delegate_count__gte=2)),
        children_delegate_id=Subquery(
            ChildrenDelegate.objects.filter(
                children_id=OuterRef('children_id')).values('id')[:1])
    ).filter(
        Q(source=DeclarationSourceEnum.CONCENTRATOR)
        & Q(portal=DeclPortalEnum.PORTAL)
        & Q(type_interaction=DTIE.SMEV_3)
        & ~Q(status__code__in=DSS.no_active_statuses())
        & Q(children_delegate_id__isnull=False)
        & Q(exists_gte_2_delegate=False)
    ).values_list('children_delegate_id', 'client_id')

    for children_delegate_id, client_id in declarations.iterator():
        ExtendedChildrenDelegate.objects.get_or_create(
            children_delegate_id=children_delegate_id,
            defaults={'order_id': client_id})


class Migration(migrations.Migration):

    dependencies = [
        ('smev3_v321', '0014_extendedchildrendelegate'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
