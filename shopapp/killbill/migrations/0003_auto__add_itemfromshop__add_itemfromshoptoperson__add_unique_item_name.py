# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemFromShop'
        db.create_table('killbill_itemfromshop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['killbill.Item'])),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['killbill.Shop'])),
        ))
        db.send_create_signal('killbill', ['ItemFromShop'])

        # Adding model 'ItemFromShopToPerson'
        db.create_table('killbill_itemfromshoptoperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_from_shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['killbill.ItemFromShop'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['killbill.Person'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('killbill', ['ItemFromShopToPerson'])

        # Removing M2M table for field shop on 'Item'
        db.delete_table(db.shorten_name('killbill_item_shop'))

        # Removing M2M table for field person on 'Item'
        db.delete_table(db.shorten_name('killbill_item_person'))

        # Adding unique constraint on 'Item', fields ['name']
        db.create_unique('killbill_item', ['name'])

        # Adding unique constraint on 'UserGroup', fields ['address']
        db.create_unique('killbill_usergroup', ['address'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserGroup', fields ['address']
        db.delete_unique('killbill_usergroup', ['address'])

        # Removing unique constraint on 'Item', fields ['name']
        db.delete_unique('killbill_item', ['name'])

        # Deleting model 'ItemFromShop'
        db.delete_table('killbill_itemfromshop')

        # Deleting model 'ItemFromShopToPerson'
        db.delete_table('killbill_itemfromshoptoperson')

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


    models = {
        'killbill.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'killbill.itemfromshop': {
            'Meta': {'object_name': 'ItemFromShop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['killbill.Item']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['killbill.Shop']"})
        },
        'killbill.itemfromshoptoperson': {
            'Meta': {'object_name': 'ItemFromShopToPerson'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_from_shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['killbill.ItemFromShop']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['killbill.Person']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {})
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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['killbill']