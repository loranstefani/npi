# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from uuid import UUID

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Enumeration'
        db.create_table(u'enumerations_enumeration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1, blank=True)),
            ('enumeration_type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('number', self.gf('django.db.models.fields.CharField')(default='', max_length=10, db_index=True, blank=True)),
            ('enumeration_date', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('name_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True, blank=True)),
            ('name_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('sole_proprietor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('organizational_subpart', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('credential', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('organization_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300, db_index=True, blank=True)),
            ('doing_business_as', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
            ('organization_other_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
            ('organization_other_name_code', self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True)),
            ('other_first_name_1', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('other_middle_name_1', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('other_last_name_1', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('other_name_prefix_1', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('other_name_suffix_1', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('other_name_credential_1', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('other_name_code_1', self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True)),
            ('other_first_name_2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('other_middle_name_2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('other_last_name_2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('other_name_prefix_2', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('other_name_suffix_2', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('other_name_credential_2', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('other_name_code_2', self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True)),
            ('parent_organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_parent_organization', null=True, to=orm['enumerations.Enumeration'])),
            ('parent_organization_legal_business_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
            ('parent_organization_ein', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('custom_profile_url', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('facebook_handle', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('public_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True)),
            ('driving_directions', self.gf('django.db.models.fields.TextField')(default='', max_length=256, blank=True)),
            ('bio_headline', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('bio_detail', self.gf('django.db.models.fields.TextField')(default='', max_length=1024, blank=True)),
            ('background_image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=255L, blank=True)),
            ('avatar_image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=255L, blank=True)),
            ('pecos_id', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('mailing_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_primary_mailing_address', null=True, to=orm['addresses.Address'])),
            ('location_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_location_address', null=True, to=orm['addresses.Address'])),
            ('medical_record_storage_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_medical_record_storage_address', null=True, to=orm['addresses.Address'])),
            ('correspondence_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_correspondence_address', null=True, to=orm['addresses.Address'])),
            ('ten_ninety_nine_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_ten_ninety_nine_address', null=True, to=orm['addresses.Address'])),
            ('revalidation_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_revalidation_address', null=True, to=orm['addresses.Address'])),
            ('taxonomy', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enumeration_primary_taxonomy', null=True, to=orm['taxonomy.TaxonomyCode'])),
            ('state_of_birth', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True)),
            ('country_of_birth', self.gf('django.db.models.fields.CharField')(default='US', max_length=2, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True)),
            ('itin', self.gf('django.db.models.fields.CharField')(default='', max_length=10, db_index=True, blank=True)),
            ('ssn', self.gf('django.db.models.fields.CharField')(default='', max_length=10, db_index=True, blank=True)),
            ('ein', self.gf('django.db.models.fields.CharField')(default='', max_length=9, db_index=True, blank=True)),
            ('ein_image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=255L, blank=True)),
            ('modify_token', self.gf('django.db.models.fields.CharField')(default=UUID('11b2a04a-88e2-4f93-994b-29f63c0d3e11'), max_length=36, blank=True)),
            ('national_agency_check', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fingerprinted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('negative_action', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deactivation_reason_code', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True)),
            ('deactivated_details', self.gf('django.db.models.fields.TextField')(default='', max_length=1000, blank=True)),
            ('deactivation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('reactivation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('replacement_npi', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('contact_person_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, db_index=True, blank=True)),
            ('contact_person_first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('contact_person_middle_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('contact_person_last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('contact_person_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('contact_person_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('contact_person_credential', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('contact_person_telephone_number', self.gf('localflavor.us.models.PhoneNumberField')(default='', max_length=20, blank=True)),
            ('contact_person_telephone_extension', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('contact_person_title_or_position', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('contact_person_title', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('authorized_official_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, db_index=True, blank=True)),
            ('authorized_official_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('authorized_official_first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('authorized_official_middle_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('authorized_official_last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('authorized_official_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('authorized_official_credential', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('authorized_official_telephone_number', self.gf('localflavor.us.models.PhoneNumberField')(default='', max_length=20, blank=True)),
            ('authorized_official_telephone_extension', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('authorized_official_title_or_position', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('authorized_official_title', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'enumerations', ['Enumeration'])

        # Adding M2M table for field associations on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_associations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('to_enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_enumeration_id', 'to_enumeration_id'])

        # Adding M2M table for field other_addresses on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_other_addresses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('address', models.ForeignKey(orm[u'addresses.address'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'address_id'])

        # Adding M2M table for field identifiers on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_identifiers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('identifier', models.ForeignKey(orm[u'identifiers.identifier'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'identifier_id'])

        # Adding M2M table for field other_taxonomies on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_other_taxonomies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('taxonomycode', models.ForeignKey(orm[u'taxonomy.taxonomycode'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'taxonomycode_id'])

        # Adding M2M table for field licenses on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_licenses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('license', models.ForeignKey(orm[u'licenses.license'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'license_id'])

        # Adding M2M table for field specialties on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_specialties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('specialty', models.ForeignKey(orm[u'specialties.specialty'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'specialty_id'])

        # Adding M2M table for field direct_addresses on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_direct_addresses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('directaddress', models.ForeignKey(orm[u'direct.directaddress'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'directaddress_id'])

        # Adding M2M table for field managers on 'Enumeration'
        m2m_table_name = db.shorten_name(u'enumerations_enumeration_managers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumeration', models.ForeignKey(orm[u'enumerations.enumeration'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumeration_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Enumeration'
        db.delete_table(u'enumerations_enumeration')

        # Removing M2M table for field associations on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_associations'))

        # Removing M2M table for field other_addresses on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_other_addresses'))

        # Removing M2M table for field identifiers on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_identifiers'))

        # Removing M2M table for field other_taxonomies on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_other_taxonomies'))

        # Removing M2M table for field licenses on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_licenses'))

        # Removing M2M table for field specialties on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_specialties'))

        # Removing M2M table for field direct_addresses on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_direct_addresses'))

        # Removing M2M table for field managers on 'Enumeration'
        db.delete_table(db.shorten_name(u'enumerations_enumeration_managers'))


    models = {
        u'addresses.address': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Address'},
            'active': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'address_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'db_index': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'address_purpose': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'address_type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '2', 'blank': 'True'}),
            'county_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'deliverable': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'diplay_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_fax': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'driving_details': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'foreign_fax_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'foreign_postal': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12', 'blank': 'True'}),
            'foreign_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'foreign_telephone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'hours_of_operation': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_standardized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'long': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'mpo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'phone_number_extension': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'private_email_contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'public_email_contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'rdi': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'record_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'telephone_number_extension': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'us_fax_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12', 'blank': 'True'}),
            'us_telephone_number': ('localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'usps_stadardized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vacant': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'})
        },
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'direct.directaddress': {
            'Meta': {'object_name': 'DirectAddress'},
            'certificate': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '255L', 'blank': 'True'}),
            'dns': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'db_index': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '150', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'enumerations.enumeration': {
            'Meta': {'ordering': "('-enumeration_date',)", 'object_name': 'Enumeration'},
            'added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'associations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'associations_rel_+'", 'null': 'True', 'to': u"orm['enumerations.Enumeration']"}),
            'authorized_official_credential': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'authorized_official_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'db_index': 'True', 'blank': 'True'}),
            'authorized_official_first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'authorized_official_last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'authorized_official_middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'authorized_official_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'authorized_official_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'authorized_official_telephone_extension': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'authorized_official_telephone_number': ('localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'authorized_official_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'authorized_official_title_or_position': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'avatar_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255L', 'blank': 'True'}),
            'background_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255L', 'blank': 'True'}),
            'bio_detail': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'bio_headline': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact_person_credential': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'contact_person_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'db_index': 'True', 'blank': 'True'}),
            'contact_person_first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'contact_person_last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'contact_person_middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'contact_person_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'contact_person_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'contact_person_telephone_extension': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'contact_person_telephone_number': ('localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'contact_person_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'contact_person_title_or_position': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'correspondence_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_correspondence_address'", 'null': 'True', 'to': u"orm['addresses.Address']"}),
            'country_of_birth': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '2', 'blank': 'True'}),
            'credential': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'custom_profile_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True', 'blank': 'True'}),
            'deactivated_details': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'deactivation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deactivation_reason_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'direct_addresses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enumerations_direct_addresses'", 'to': u"orm['direct.DirectAddress']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'doing_business_as': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'driving_directions': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'ein': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '9', 'db_index': 'True', 'blank': 'True'}),
            'ein_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255L', 'blank': 'True'}),
            'enumeration_date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'enumeration_type': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'facebook_handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'fingerprinted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enumeration_identifiers'", 'to': u"orm['identifiers.Identifier']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'itin': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'db_index': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'licenses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enumerations_licenses'", 'to': u"orm['licenses.License']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'location_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_location_address'", 'null': 'True', 'to': u"orm['addresses.Address']"}),
            'mailing_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_primary_mailing_address'", 'null': 'True', 'to': u"orm['addresses.Address']"}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'medical_record_storage_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_medical_record_storage_address'", 'null': 'True', 'to': u"orm['addresses.Address']"}),
            'middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'modify_token': ('django.db.models.fields.CharField', [], {'default': "UUID('c39f549c-c90f-4410-98db-c5d44cfc839b')", 'max_length': '36', 'blank': 'True'}),
            'name_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'name_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'national_agency_check': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'negative_action': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'db_index': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'db_index': 'True', 'blank': 'True'}),
            'organization_other_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'organization_other_name_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'organizational_subpart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other_addresses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'enumeration_other_addresses'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['addresses.Address']"}),
            'other_first_name_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'other_first_name_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'other_last_name_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'other_last_name_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'other_middle_name_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'other_middle_name_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'other_name_code_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'other_name_code_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'other_name_credential_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'other_name_credential_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'other_name_prefix_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'other_name_prefix_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'other_name_suffix_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'other_name_suffix_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'other_taxonomies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'enumeration_other_taxonomies'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['taxonomy.TaxonomyCode']"}),
            'parent_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_parent_organization'", 'null': 'True', 'to': u"orm['enumerations.Enumeration']"}),
            'parent_organization_ein': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'parent_organization_legal_business_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'pecos_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'public_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'reactivation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'replacement_npi': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'revalidation_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_revalidation_address'", 'null': 'True', 'to': u"orm['addresses.Address']"}),
            'sole_proprietor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specialties': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enumerations_specialties'", 'to': u"orm['specialties.Specialty']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'db_index': 'True', 'blank': 'True'}),
            'state_of_birth': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1', 'blank': 'True'}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_primary_taxonomy'", 'null': 'True', 'to': u"orm['taxonomy.TaxonomyCode']"}),
            'ten_ninety_nine_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enumeration_ten_ninety_nine_address'", 'null': 'True', 'to': u"orm['addresses.Address']"}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'identifiers.identifier': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Identifier'},
            'added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'issuer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'licenses.license': {
            'Meta': {'unique_together': "(('license_type', 'number'),)", 'object_name': 'License'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_note': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'license_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255L', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licenses.LicenseType']"}),
            'note': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'note_restictions': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '10'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_by_issuing_board': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_by_ther_means': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'licenses.licensetype': {
            'Meta': {'ordering': "('state', 'license_type')", 'unique_together': "(('state', 'license_type'),)", 'object_name': 'LicenseType'},
            'credential': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mac': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'provider_type': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'specialties.specialty': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Specialty'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxonomy': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'db_index': 'True', 'blank': 'True'})
        },
        u'taxonomy.taxonomycode': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'TaxonomyCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inactive': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'npi_worthy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent_taxonomycode_id': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True'}),
            'pt': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'speciality': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_index': 'True'}),
            'taxclass': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['enumerations']