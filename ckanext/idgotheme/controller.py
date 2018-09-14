# coding: utf-8
from logging import getLogger
from ckan.common import config
import ckan.logic as logic
import ckan.lib.base as base
from ckan.common import _, request 
from ckan.plugins.toolkit import asint
import urlparse

import ckan.plugins.toolkit as toolkit
import ckan.model as model
from ckan.common import config, c
import requests

class ExportController(base.BaseController):
    
    def query_export(self, *args, **kwargs):
        args = dict(kwargs['environ']['paste.parsed_dict_querystring'][0])
        
        q = ''
        fq = ''
        bbox = ''
        resformat = 'odl1'
        for key in args:
            if key == 'resformat':
                resformat = args[key]
            elif key == 'ext_bbox':
                bbox = args[key]
            elif key == 'q':
                q = args[key]
            else:
                if key not in ['ext_prev_extent','sort']:
                    fq += ' +' + key + ':' + args[key]

        context = { 'model': base.model,
                    'session': base.model.Session,
                    'user': base.c.user }
        data_dict = {'rows': 100000, 'q': q, 'fq': fq, 'ext_bbox': bbox}
        search_result = toolkit.get_action('package_search')(context, data_dict)
        results = [x['id'] for x in search_result.get('results', [])]

        # POST REQUEST
        export_url = url_site_publier = config.get('ckanext.idgotheme.url_site_publier', '') + '/dataset/export?'
        export_data = {'ids': ','.join(results), 'format': resformat} 
        r = requests.post(url=export_url, data=export_data)

        return r
