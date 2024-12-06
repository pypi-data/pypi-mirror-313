import os

from django.db import migrations, models

from kinder.core.db import LoadFixtureReversible
from kinder.core.db import CorrectSequenceReversible


APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Migration(migrations.Migration):

    dependencies = [
        ('lipetsk_specifics', '0002_auto_20170206_1055'),
    ]

    operations = [
        LoadFixtureReversible(
            os.path.join(APP_DIR, 'fixtures', 'initial_data.json')),
        LoadFixtureReversible(
            os.path.join(APP_DIR, 'fixtures', 'reject_reason_data.json')),
        CorrectSequenceReversible('Department'),
        CorrectSequenceReversible('DepartmentAttributes'),
        CorrectSequenceReversible('RejectReason')
    ]
