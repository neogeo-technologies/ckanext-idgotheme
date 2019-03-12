# coding: utf-8


import ckan.lib.helpers as h
from ckanext.scheming.errors import SchemingException
import ckanext.scheming.helpers as sh
from ckantoolkit import _
from ckantoolkit import get_validator
from ckantoolkit import Invalid
from ckantoolkit import missing
from ckantoolkit import UnknownValidator
import datetime
import json
import pytz
import re


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
            except (TypeError, ValueError), e:
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
