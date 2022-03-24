# Generated by Django 4.0.3 on 2022-03-24 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='username',
        ),
        migrations.RemoveField(
            model_name='cartdetail',
            name='img',
        ),
        migrations.RemoveField(
            model_name='cartdetail',
            name='price',
        ),
        migrations.RemoveField(
            model_name='cartdetail',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='cartdetail',
            name='username',
        ),
        migrations.RemoveField(
            model_name='order',
            name='username',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='img',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='price',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand_id',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cartdetail',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='core.product'),
        ),
        migrations.AddField(
            model_name='cartdetail',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='core.order'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='core.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='core.brand'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
