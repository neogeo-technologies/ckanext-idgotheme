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


from collections import OrderedDict
import json
from logging import getLogger
import requests

from ckan.common import c
from ckan.common import config
import ckan.lib.helpers as h
import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckanext.scheming.plugins import _SchemingMixin

from .validation import force_resource_url_type
from .validation import scheming_datasetfield_null_if_empty
from .validation import scheming_replace_created_date
from .validation import scheming_replace_modified_date


log = getLogger(__name__)


def get_platform_name():
    return config.get('ckanext.idgotheme.name', r'IDGO').decode('utf-8')


def get_readthedocs_url():
    return config.get('ckanext.idgotheme.readthedocs', None)


def get_default_extent():
    extent = config.get('ckanext.idgotheme.extent', r'-5.6 41 9.9 51.4').split()
    try:
        return [[float(extent[1]), float(extent[0])],
                [float(extent[3]), float(extent[2])]].__str__()
    except Exception as e:
        log.error(e)
        return [[-5.6, 41], [9.9, 51.4]].__str__()


def get_url_wp():
    url_site_wp = config.get('ckanext.idgotheme.url_site_wp', '')
    return url_site_wp


def get_url_publier():
    url_site_publier = config.get('ckanext.idgotheme.url_site_publier', '')
    return url_site_publier


def get_url_extracteur():
    return config.get('ckanext.idgotheme.url_site_extracteur', '')


def get_url_site_wp():
    url_site_wp = config.get('ckanext.idgotheme.url_site_wp', '')
    return url_site_wp


def href_accessibility():
    return config.get('ckanext.idgotheme.href_accessibility')


def href_terms_and_conditions():
    return config.get('ckanext.idgotheme.href_terms_and_conditions')


def href_legal_notices():
    return config.get('ckanext.idgotheme.href_legal_notices')


def href_contact():
    return config.get('ckanext.idgotheme.href_contact')


def href_site_map():
    return config.get('ckanext.idgotheme.href_site_map')


def href_credit():
    return config.get('ckanext.idgotheme.href_credit')


# Traduction "Groupes" en "Thématiques"
THEMATIQUE_MIN = u"thématique"
THEMATIQUE_MAJ = u"Thématique"
THEMATIQUES_MIN = u"thématiques"
THEMATIQUES_MAJ = u"Thématiques"


def trad_thematique_min():
    return THEMATIQUE_MIN


def trad_thematique_maj():
    return THEMATIQUE_MAJ


def trad_thematiques_min():
    return THEMATIQUES_MIN


def trad_thematiques_maj():
    return THEMATIQUES_MAJ


def is_idgo_partner():
    if not c.userobj:
        return False
    if c.userobj.sysadmin:
        return True

    # /!\ TODO /!\
    # => Affectuer filtre sur le nom du groupe pas sur le type !
    partner_group_id = model.Session.query(model.Group) \
        .filter(model.Group.type == 'partner') \
        .first().id
    # /!\ TODO /!\

    query = model.Session.query(model.Member) \
        .filter(model.Member.state == 'active') \
        .filter(model.Member.table_name == 'user') \
        .filter(model.Member.group_id == partner_group_id) \
        .filter(model.Member.table_id == c.userobj.id)

    return len(query.all()) != 0


def get_ihm_settings():
    data = {
        'download-modal-res-list': {
            'active': False,
            'content': '',
        }
    }

    url = get_url_publier() + "/ihm/ckan/settings"
    try:
        r = requests.get(url)
    except Exception as err:
        log.error(err)
    else:
        # Résout #8789 avec try..except
        try:
            data.update(r.json())
        except json.decoder.JSONDecodeError:
            pass
    return data


def get_proxified_service_url(package_id, resource_id):
    return h.url_for(
        action='proxy_service',
        controller='ckanext.geoview.controllers.service_proxy:ServiceProxyController',
        id=package_id,
        resource_id=resource_id,
    )


class IdgothemePlugin(p.SingletonPlugin, _SchemingMixin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IFacets, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IValidators)

    SCHEMA_OPTION = 'scheming.dataset_schemas'
    FALLBACK_OPTION = 'scheming.dataset_fallback'
    SCHEMA_TYPE_FIELD = 'dataset_type'

    # ITemplateHelpers : Custom Helpers functions
    def get_helpers(self):
        return {
            'idgotheme_href_accessibility': href_accessibility,
            'idgotheme_href_terms_and_conditions': href_terms_and_conditions,
            'idgotheme_href_legal_notices': href_legal_notices,
            'idgotheme_href_contact': href_contact,
            'idgotheme_href_site_map': href_site_map,
            'idgotheme_href_credit': href_credit,
            'idgotheme_get_url_wp': get_url_wp,
            'idgotheme_get_url_publier': get_url_publier,
            'idgotheme_get_url_extracteur': get_url_extracteur,
            'trad_thematique_min': trad_thematique_min,
            'trad_thematique_maj': trad_thematique_maj,
            'trad_thematiques_min': trad_thematiques_min,
            'trad_thematiques_maj': trad_thematiques_maj,
            'is_idgo_partner': is_idgo_partner,
            'proxy_export': self.proxy_export,
            'get_res_api': self.get_res_api,
            'get_ihm_settings': get_ihm_settings,
            'get_platform_name': get_platform_name,
            'get_readthedocs_url': get_readthedocs_url,
            'get_default_extent': get_default_extent,
        }

    def get_validators(self):
        return {
            'force_resource_url_type': force_resource_url_type,
            'scheming_replace_created_date': scheming_replace_created_date,
            'scheming_replace_modified_date': scheming_replace_modified_date,
            'scheming_datasetfield_null_if_empty': scheming_datasetfield_null_if_empty,
        }

    def get_res_api(self, res):
        service_url = get_proxified_service_url(res['package_id'], res['id'])
        try:
            api = json.loads(res.get('api'))
        except Exception:
            return None
        # else:
        if 'url' in api:
            for key in ('geojson', 'shapezip', 'getlegendgraphic',):
                if key not in api:
                    continue
                api[key] = api.pop(key).replace(api['url'], service_url)
        return api

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'idgotheme')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        # Ajouter les filtres, dans l'ordre d'affichage sur la page
        if package_type == 'showcase':
            return OrderedDict({'tags': u'Mots-clés'})
        else:
            return OrderedDict([
                ('organization', u"Organisations"),
                ('groups', u"Thématiques"),
                ('datatype', u"Types"),
                ('support', u"Supports"),
                ('res_format', u"Formats"),
                ('license_id', u"Licences"),
                ('tags', u"Mots-clés"),
                ('frequency', u"Fréquence de mise à jour"),
                ('granularity', u"Granularité de la couverture territoriale"),
            ])

    # IPackageController
    def before_index(self, data_dict):
        data_dict['datatype'] = json.loads(data_dict.get('datatype', '[]'))
        return data_dict

    def before_map(self, m):
        m.connect(
            '/dataset/export',
            controller='ckanext.idgotheme.controller:ExportController',
            action='query_export',
        )
        return m

    def proxy_export(self, resformat, *args):
        kw = dict(list(args)[0].params)
        return h.url_for(
            action='query_export',
            controller='ckanext.idgotheme.controller:ExportController',
            resformat=resformat,
            **kw
        )
