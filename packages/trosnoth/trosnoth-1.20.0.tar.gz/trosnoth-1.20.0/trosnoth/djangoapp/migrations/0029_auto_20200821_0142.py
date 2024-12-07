from django.db import migrations, models


def change_default_port_from_6787_to_6780(apps, schema_editor):
    TrosnothServerSettings = apps.get_registered_model('trosnoth', 'TrosnothServerSettings')
    rows = TrosnothServerSettings.objects.all()
    if rows.count() == 0:
        return
    record = rows[0]
    if record.serverPort == 6787:
        record.serverPort = 6780
        record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('trosnoth', '0028_auto_20191028_0108'),
    ]

    operations = [
        migrations.RunPython(change_default_port_from_6787_to_6780),
        migrations.AddField(
            model_name='trosnothserversettings',
            name='tls_certificate',
            field=models.BinaryField(default=None, null=True, verbose_name='This server’s private TLS certificate in PEM format.'),
        ),
        migrations.AlterField(
            model_name='trosnotharena',
            name='balance_bot_difficulty',
            field=models.IntegerField(blank=True, default=20, null=True, verbose_name='Difficulty for BalanceBot'),
        ),
        migrations.AlterField(
            model_name='trosnothserversettings',
            name='serverPort',
            field=models.SmallIntegerField(default=6780, verbose_name='Authentication port'),
        ),
    ]
