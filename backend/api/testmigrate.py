from django.db import migrations, models

def copy_data_from_old_field(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'MyModel')
    for instance in MyModel.objects.all():
        instance.new_field = instance.old_field
        instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='new_field',
            field=models.CharField(max_length=100),
        ),
        migrations.RunPython(copy_data_from_old_field),
    ]
