from collections import defaultdict

from esengine.bases import ELASTICSEARCH_BASE_VERSION

try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable


class Mapping(object):
    """
    Used to generate mapping based in document field definitions

    >>> class Obj(Document):
    ...     name = StringField()

    And you can use a Mapping to refresh mappings
    (use in cron jobs or call periodically)

    obj_mapping = Mapping(Obj)
    obj_mapping.save()

    Adicionally this class handle index settings configuration. However this
    operation must be done at elasticsearch index creation.

    """
    def __init__(self, document_class=None, enable_all=True):
        self.document_class = document_class
        self.enable_all = enable_all

    def _generate(self, doc_class):
        """
        Generate the mapping acording to doc_class.

        Args:
            doc_class: esengine.Document object containing the model to be
            mapped to elasticsearch.
        """
        properties = {
            "_all": {"enabled": self.enable_all},
            "properties": {
                field_name: field_instance.mapping
                for field_name, field_instance in doc_class._fields.items()
                if field_name != "id"
            }
        }
        if ELASTICSEARCH_BASE_VERSION >= 6:
            del properties["_all"]
        if ELASTICSEARCH_BASE_VERSION >= 8:
            m = properties
        else:
            m = {
                doc_class._doctype: properties
            }
        return m

    def generate(self):
        return self._generate(self.document_class)

    def save(self, es=None):
        """
        Save the mapping to index.

        Args:
            es: elasticsearch client intance.
        """
        es = self.document_class.get_es(es)

        if not es.indices.exists(index=self.document_class._index):
            request_body = {
                "body": {"mappings": self.generate()}
            }
            if ELASTICSEARCH_BASE_VERSION >= 6 and ELASTICSEARCH_BASE_VERSION < 8:
                request_body["params"] = {"include_type_name": "true"}
            return es.indices.create(
                index=self.document_class._index,
                **request_body
            )
        else:
            request_body = {
                "body": {"mappings": self.generate()}
            }
            if ELASTICSEARCH_BASE_VERSION < 6:
                request_body["doc_type"] = self.document_class._doctype
            if ELASTICSEARCH_BASE_VERSION >= 6 and ELASTICSEARCH_BASE_VERSION < 8:
                request_body["params"] = {"include_type_name": "true"}
                request_body["doc_type"] = self.document_class._doctype
            if ELASTICSEARCH_BASE_VERSION >= 2:
                request_body["body"] = request_body["body"]["mappings"]
            return es.indices.put_mapping(
                index=self.document_class._index,
                **request_body
            )

    def build_configuration(self, models_to_mapping, custom_settings, es=None):
        """
        Build request body to add custom settings (filters, analizers, etc) to index.

        Build request body to add custom settings, like filters and analizers,
        to index.

        Args:
            models_to_mapping: A list with the esengine.Document objects that
            we want generate mapping.

            custom_settings: a dict containing the configuration that will be
            sent to elasticsearch/_settings (www.elastic.co/guide/en/
                elasticsearch/reference/current/indices-update-settings.html)

            es: elasticsearch client intance.
        """  # noqa
        indexes = set()
        configuration = {}
        mapped_models = [x for x in models_to_mapping]
        for model in mapped_models:
            indexes.add(model._index)
            es = model.get_es(es)
        for index in indexes:
            if es.indices.exists(index=index):
                msg = 'Settings are supported only on index creation'
                raise ValueError(msg)
        mappings_by_index = defaultdict(dict)
        for model in mapped_models:
            mapping = self._generate(model)
            mappings_by_index[model._index].update(mapping)
        for index, mappings in mappings_by_index.items():
            settings = {
                "settings": custom_settings,
                "mappings": mappings
            }
            configuration[index] = settings
        return configuration

    def configure(self, models_to_mapping, custom_settings=None, es=None):
        """
        Add custom settings like filters and analizers to index.

        Add custom settings, like filters and analizers, to index. Be aware
        that elasticsearch only allow this operation on index creation.

        Args:
            models_to_mapping: A list with the esengine.Document objects that
            we want generate mapping.

            custom_settings: a dict containing the configuration that will be
            sent to elasticsearch/_settings (www.elastic.co/guide/en/
                elasticsearch/reference/current/indices-update-settings.html)

            es: elasticsearch client intance.
        """
        if not isinstance(models_to_mapping, Iterable):
            raise AttributeError('models_to_mapping must be iterable')

        if custom_settings:
            for model in models_to_mapping:
                es = model.get_es(es)
                if es:
                    break
            configurations = self.build_configuration(
                models_to_mapping,
                custom_settings,
                es
            )
            for index, settings in configurations.items():
                es.indices.create(index=index, body=settings)
        else:
            mapped_models = [x for x in models_to_mapping]
            for model in mapped_models:
                model.put_mapping()
