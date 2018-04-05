# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-03-12 21:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from data.utilities import update_mupit_structure_for_existing_variants
from django.core.management import call_command


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0026_auto_20180312_2100'),
    ]

    operations = [
        migrations.RunPython(update_mupit_structure_for_existing_variants),
        migrations.RunSQL(
            """
            DROP MATERIALIZED VIEW IF EXISTS currentvariant;
            CREATE MATERIALIZED VIEW currentvariant AS (
                SELECT * FROM "variant" WHERE (
                    "id" IN ( SELECT DISTINCT ON ("Genomic_Coordinate_hg38") "id" FROM "variant" ORDER BY "Genomic_Coordinate_hg38" ASC, "Data_Release_id" DESC )
                )
            );
            """
        ),
    ]
