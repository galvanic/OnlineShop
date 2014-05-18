# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('killbill_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['killbill.UserGroup'])),
        ))
        db.send_create_signal('killbill', ['Person'])

        # Adding model 'Item'
        db.create_table('killbill_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5)),
        ))
        db.send_create_signal('killbill', ['Item'])

        # Adding M2M table for field shop on 'Item'
        m2m_table_name = db.shorten_name('killbill_item_shop')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['killbill.item'], null=False)),
            ('shop', models.ForeignKey(orm['killbill.shop'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'shop_id'])

        # Adding M2M table for field person on 'Item'
        m2m_table_name = db.shorten_name('killbill_item_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['killbill.item'], null=False)),
            ('person', models.ForeignKey(orm['killbill.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'person_id'])

        # Adding model 'Shop'
        db.create_table('killbill_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('delivery_date', self.gf('django.db.models.fields.DateField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['killbill.UserGroup'])),
        ))
        db.send_create_signal('killbill', ['Shop'])

        # Adding model 'UserGroup'
        db.create_table('killbill_usergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('killbill', ['UserGroup'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('killbill_person')

        # Deleting model 'Item'
        db.delete_table('killbill_item')

        # Removing M2M table for field shop on 'Item'
        db.delete_table(db.shorten_name('killbill_item_shop'))

        # Removing M2M table for field person on 'Item'
        db.delete_table(db.shorten_name('killbill_item_person'))

        # Deleting model 'Shop'
        db.delete_table('killbill_shop')

        # Deleting model 'UserGroup'
        db.delete_table('killbill_usergroup')


    models = {
        'killbill.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'person': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['killbill.Person']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'shop': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['killbill.Shop']"})
        },
        'killbill.person': {
            'Meta': {'object_name': 'Person'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['killbill.UserGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'killbill.shop': {
            'Meta': {'object_name': 'Shop'},
            'delivery_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['killbill.UserGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'killbill.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['killbill']