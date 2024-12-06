from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0001_initial'),
        ('declaration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeclarationRejectReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u041f\u0440\u0438\u0447\u0438\u043d\u044b \u043e\u0442\u043a\u0430\u0437\u0430',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20, null=True, verbose_name='\u041a\u043e\u0434', blank=True)),
                ('name', models.CharField(max_length=150, verbose_name='\u0418\u043c\u044f')),
            ],
            options={
                'verbose_name': '\u0412\u0435\u0434\u043e\u043c\u0441\u0442\u0432\u0430',
            },
        ),
        migrations.CreateModel(
            name='DepartmentAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=256, verbose_name='\u0410\u0442\u0440\u0438\u0431\u0443\u0442', choices=[(b'birthplace', '\u041c\u0435\u0441\u0442\u043e \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f'), (b'military_unit', '\u0412\u043e\u0438\u043d\u0441\u043a\u0430\u044f \u0447\u0430\u0441\u0442\u044c (\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435)'), (b'personal_number', '\u041b\u0438\u0447\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440'), (b'force_kind', '\u041f\u0440\u0438\u043d\u0430\u0434\u043b\u0435\u0436\u043d\u043e\u0441\u0442\u044c \u043a \u0432\u0438\u0434\u0443 \u0438\u043b\u0438 \u0440\u043e\u0434\u0443 \u0432\u043e\u0439\u0441\u043a'), (b'dismissal_date', '\u0414\u0430\u0442\u0430 \u0443\u0432\u043e\u043b\u044c\u043d\u0435\u043d\u0438\u044f'), (b'rank', '\u0417\u0432\u0430\u043d\u0438\u0435')])),
                ('department', models.ForeignKey(to='lipetsk_specifics.Department', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': '\u0410\u0442\u0440\u0438\u0431\u0443\u0442\u044b \u0432\u0435\u0434\u043e\u043c\u0441\u0442\u0432\u0430',
            },
        ),
        migrations.CreateModel(
            name='PrivilegeConfirmationAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('privilege_owner', models.SmallIntegerField(null=True, verbose_name='\u041f\u0440\u0438\u043d\u0430\u0434\u043b\u0435\u0436\u043d\u043e\u0441\u0442\u044c \u043b\u044c\u0433\u043e\u0442\u044b', choices=[(1, '\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c'), (2, '\u0420\u0435\u0431\u0435\u043d\u043e\u043a'), (3, '\u041f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u0438\u0442\u0435\u043b\u044c')])),
                ('document_issued_by', models.CharField(max_length=256, null=True, verbose_name='\u041a\u0435\u043c \u0432\u044b\u0434\u0430\u043d', blank=True)),
                ('document_date', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u0434\u0430\u0447\u0438', blank=True)),
                ('birthplace_country', models.CharField(max_length=256, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', blank=True)),
                ('birthplace_region', models.CharField(max_length=256, null=True, verbose_name='\u0420\u0435\u0433\u0438\u043e\u043d', blank=True)),
                ('birthplace_city', models.CharField(max_length=256, null=True, verbose_name='\u041d\u0430\u0441\u0435\u043b\u0435\u043d\u043d\u044b\u0439 \u043f\u0443\u043d\u043a\u0442', blank=True)),
                ('personal_number', models.CharField(max_length=256, null=True, verbose_name='\u041b\u0438\u0447\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440', blank=True)),
                ('force_kind', models.CharField(max_length=256, null=True, verbose_name='\u041f\u0440\u0438\u043d\u0430\u0434\u043b\u0435\u0436\u043d\u043e\u0441\u0442\u044c \u043a \u0432\u0438\u0434\u0443 \u0438\u043b\u0438 \u0440\u043e\u0434\u0443 \u0432\u043e\u0439\u0441\u043a', blank=True)),
                ('military_unit', models.CharField(max_length=256, null=True, verbose_name='\u0412\u043e\u0438\u043d\u0441\u043a\u0430\u044f \u0447\u0430\u0441\u0442\u044c (\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435)', blank=True)),
                ('dismissal_date', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0443\u0432\u043e\u043b\u044c\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('rank', models.CharField(max_length=256, null=True, verbose_name='\u0417\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('portal', models.BooleanField(default=False, verbose_name='\u041f\u0440\u0438\u0437\u043d\u0430\u043a \u0447\u0442\u043e \u043b\u044c\u0433\u043e\u0442\u0430 \u043f\u0440\u0438\u0448\u043b\u0430 \u0441 \u043f\u043e\u0440\u0442\u0430\u043b\u0430')),
                ('declaration_privilege', models.ForeignKey(to='declaration.DeclarationPrivilege', on_delete=models.CASCADE)),
                ('delegate', models.ForeignKey(verbose_name='\u041e\u0431\u043b\u0430\u0434\u0430\u0442\u0435\u043b\u044c \u043b\u044c\u0433\u043e\u0442\u044b', to='children.Delegate', null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'verbose_name': '\u0410\u0442\u0440\u0438\u0431\u0443\u0442\u044b \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u043b\u044c\u0433\u043e\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='RejectReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20, null=True, verbose_name='\u041a\u043e\u0434', blank=True)),
                ('name', models.CharField(max_length=150, verbose_name='\u0418\u043c\u044f')),
            ],
            options={
                'verbose_name': '\u041f\u0440\u0438\u0447\u0438\u043d\u044b \u043e\u0442\u043a\u0430\u0437\u0430',
            },
        ),
    ]
