# coding: utf-8

# Copyright (c) 2017-2020 Neogeo-Technologies.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import datetime

import ckan.model as model
from ckantoolkit import _
from ckantoolkit import get_validator
from ckantoolkit import Invalid


OneOf = get_validator('OneOf')
ignore_missing = get_validator('ignore_missing')
not_empty = get_validator('not_empty')


def scheming_validator(fn):
    """
    Decorate a validator that needs to have the scheming fields
    passed with this function. When generating navl validator lists
    the function decorated will be called passing the field
    and complete schema to produce the actual validator for each field.
    """
    fn.is_a_scheming_validator = True
    return fn


def generic_date_validator(metadata_key, key, data, errors, context):
    value = data[key]
    date = None
    if value:
        if isinstance(value, datetime.datetime):
            date = value
        else:
            try:
                date = datetime.datetime.strptime(value, '%Y-%m-%d')
            except (TypeError, ValueError, AttributeError):
                raise Invalid(_('Date format incorrect'))

        data[(metadata_key, )] = date.isoformat()


@scheming_validator
def scheming_replace_created_date(field, schema):
    def validator(key, data, errors, context):
        generic_date_validator('metadata_created', key, data, errors, context)
    return validator


@scheming_validator
def scheming_replace_modified_date(field, schema):
    def validator(key, data, errors, context):
        generic_date_validator('metadata_modified', key, data, errors, context)
    return validator


@scheming_validator
def scheming_datasetfield_null_if_empty(field, schema):
    def validator(key, data, errors, context):
        value = data[key]
        if not value:
            for i in xrange(len(schema['dataset_fields'])):
                if schema['dataset_fields'][i]['field_name'] == field['field_name']:
                    schema['dataset_fields'][i]['display_snippet'] = None
    return validator


@scheming_validator
def force_resource_url_type(field, schema):
    def validator(key, data, errors, context):
        value = data[key]
        if value in ('upload',):
            resource_id = data[(key[0], key[1], 'id')]
            data = {'url_type': value}
            model.Session.query(model.Resource).filter_by(id=resource_id).update(data)
    return validator
