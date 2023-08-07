# Generated by Django 4.1.10 on 2023-08-07 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mgahawa', '0002_rename_fooditem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mgahawa.order'),
        ),
    ]