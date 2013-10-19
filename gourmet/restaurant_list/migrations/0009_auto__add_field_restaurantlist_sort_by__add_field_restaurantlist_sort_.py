# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RestaurantList.sort_by'
        db.add_column(u'restaurant_list_restaurantlist', 'sort_by', self.gf('django.db.models.fields.CharField')(default='rating', max_length=256), keep_default=False)

        # Adding field 'RestaurantList.sort_direction'
        db.add_column(u'restaurant_list_restaurantlist', 'sort_direction', self.gf('django.db.models.fields.CharField')(default='DESC', max_length=256), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RestaurantList.sort_by'
        db.delete_column(u'restaurant_list_restaurantlist', 'sort_by')

        # Deleting field 'RestaurantList.sort_direction'
        db.delete_column(u'restaurant_list_restaurantlist', 'sort_direction')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 19, 13, 54, 45, 384384)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 19, 13, 54, 45, 383985)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'restaurant_list.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'full_address': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'geo_coordinate': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'db_index': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {})
        },
        u'restaurant_list.restaurantlist': {
            'Meta': {'object_name': 'RestaurantList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'sort_by': ('django.db.models.fields.CharField', [], {'default': "'rating'", 'max_length': '256'}),
            'sort_direction': ('django.db.models.fields.CharField', [], {'default': "'DESC'", 'max_length': '256'})
        },
        u'restaurant_list.restaurantlistelement': {
            'Meta': {'object_name': 'RestaurantListElement'},
            'has_been': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'raw_upload_info': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['restaurant_list.Restaurant']", 'null': 'True'}),
            'restaurantList': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['restaurant_list.RestaurantList']"})
        }
    }

    complete_apps = ['restaurant_list']
