from ckan.common import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckanext.wikidatakeyword import validators


class WikidatakeywordPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'wikidatakeyword')

    # IPackageController

    # CKAN < 2.10
    def before_index(self, data_dict):
        return self.before_dataset_index(data_dict)

    # CKAN >= 2.10
    def before_dataset_index(self, data_dict):
        value = data_dict.get('keywords', [])
        if value:
            data_dict['keywords_facet'] = json.loads(value)

        return data_dict

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        return _add_facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        return _add_facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type, package_type):
        return _add_facets(facets_dict)

    # IValidators

    def get_validators(self):
        return {
            'wikidata_keyword': validators.wikidata_keyword,
            'wikidata_keyword_output': validators.wikidata_keyword_output
            }


def _add_facets(facets_dict):
    facets_dict['keywords_facet'] = plugins.toolkit._('Wikidata Keywords')

    return facets_dict
