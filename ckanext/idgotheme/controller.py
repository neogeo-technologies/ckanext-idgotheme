# coding: utf-8


from ckan.common import _
from ckan.common import c
from ckan.common import config
from ckan.common import request
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import asint
from logging import getLogger
import requests
import urlparse


class ExportController(base.BaseController):

    def query_export(self, *args, **kwargs):
        args = dict(kwargs['environ']['paste.parsed_dict_querystring'][0])
        facet_filters = [
            'organization',
            'groups',
            'datatype',
            'res_format',
            'support',
            'license_id',
            'tags',
            'frequency',
            'granularity',
        ]

        q = ''
        fq = ''
        bbox = ''
        resformat = 'odl'

        for key in args:
            if key == 'resformat':
                resformat = args[key]
            elif key == 'ext_bbox':
                bbox = args[key]
            elif key == 'q':
                q = args[key]
            else:
                if key in facet_filters:
                    fq += ' +' + key + ':' + args[key]

        context = {
            'model': base.model,
            'session': base.model.Session,
            'user': base.c.user,
        }

        data_dict = {
            'rows': 100000,
            'q': q,
            'fq': fq,
            'ext_bbox': bbox,
        }

        search_result = toolkit.get_action('package_search')(context, data_dict)
        results = [x['id'] for x in search_result.get('results', [])]

        # POST REQUEST
        export_url = url_site_publier = config.get('ckanext.idgotheme.url_site_publier', '') + '/dataset/export?'
        export_data = {'ids': ','.join(results), 'format': resformat}
        r = requests.post(url=export_url, data=export_data)

        return r
