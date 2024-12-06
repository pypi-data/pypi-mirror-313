from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaration', '0001_initial'),
        ('privilege', '0001_initial'),
        ('lipetsk_specifics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='privileges',
            field=models.ManyToManyField(to='privilege.Privilege'),
        ),
        migrations.AddField(
            model_name='declarationrejectreason',
            name='declaration',
            field=models.ForeignKey(verbose_name='\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u0438\u0435', to='declaration.Declaration', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='declarationrejectreason',
            name='reject_reason',
            field=models.ForeignKey(verbose_name='\u041f\u0440\u0438\u0447\u0438\u043d\u0430 \u043e\u0442\u043a\u0430\u0437\u0430', blank=True, to='lipetsk_specifics.RejectReason', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AlterUniqueTogether(
            name='privilegeconfirmationattributes',
            unique_together=set([('delegate', 'declaration_privilege')]),
        ),
        migrations.AlterUniqueTogether(
            name='departmentattributes',
            unique_together=set([('department', 'attribute')]),
        ),
        migrations.AlterUniqueTogether(
            name='declarationrejectreason',
            unique_together=set([('declaration', 'reject_reason')]),
        ),
    ]
