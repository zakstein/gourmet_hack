# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Restaurant.location'
        db.delete_column('restaurant_list_restaurant', 'location')

        # Adding field 'Restaurant.full_address'
        db.add_column('restaurant_list_restaurant', 'full_address', self.gf('django.db.models.fields.CharField')(default='', max_length=1023), keep_default=False)

        # Adding field 'Restaurant.address'
        db.add_column('restaurant_list_restaurant', 'address', self.gf('django.db.models.fields.CharField')(default='', max_length=256), keep_default=False)

        # Adding field 'Restaurant.city'
        db.add_column('restaurant_list_restaurant', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)

        # Adding field 'Restaurant.state'
        db.add_column('restaurant_list_restaurant', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=64), keep_default=False)

        # Adding field 'Restaurant.zip_code'
        db.add_column('restaurant_list_restaurant', 'zip_code', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Restaurant.neighborhood'
        db.add_column('restaurant_list_restaurant', 'neighborhood', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)

        # Adding field 'Restaurant.geo_coordinate'
        db.add_column('restaurant_list_restaurant', 'geo_coordinate', self.gf('django.db.models.fields.CharField')(default='', max_length=1024), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Restaurant.location'
        db.add_column('restaurant_list_restaurant', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=512), keep_default=False)

        # Deleting field 'Restaurant.full_address'
        db.delete_column('restaurant_list_restaurant', 'full_address')

        # Deleting field 'Restaurant.address'
        db.delete_column('restaurant_list_restaurant', 'address')

        # Deleting field 'Restaurant.city'
        db.delete_column('restaurant_list_restaurant', 'city')

        # Deleting field 'Restaurant.state'
        db.delete_column('restaurant_list_restaurant', 'state')

        # Deleting field 'Restaurant.zip_code'
        db.delete_column('restaurant_list_restaurant', 'zip_code')

        # Deleting field 'Restaurant.neighborhood'
        db.delete_column('restaurant_list_restaurant', 'neighborhood')

        # Deleting field 'Restaurant.geo_coordinate'
        db.delete_column('restaurant_list_restaurant', 'geo_coordinate')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'restaurant_list.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'full_address': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'geo_coordinate': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {})
        },
        'restaurant_list.restaurantlist': {
            'Meta': {'object_name': 'RestaurantList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'restaurant_list.restaurantlistelement': {
            'Meta': {'object_name': 'RestaurantListElement'},
            'has_been': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant_list.Restaurant']"}),
            'restaurantList': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant_list.RestaurantList']"})
        }
    }

    complete_apps = ['restaurant_list']
