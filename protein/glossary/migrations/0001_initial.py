# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('term', models.CharField(max_length=160)),
                ('definition', models.TextField()),
                ('reference', models.CharField(max_length=160)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
