from importlib.metadata import metadata

from django.db.utils import OperationalError, ProgrammingError
from django.db.models.signals import post_migrate

from netbox.plugins import PluginConfig

metadata = metadata('netbox_secrets')

def configure_generic_relations(sender, **kwargs):
    from django.contrib.contenttypes.fields import GenericRelation
    from django.contrib.contenttypes.models import ContentType

    from .constants import SECRET_ASSIGNABLE_MODELS
    from .models import Secret

    try:
        for content_type in ContentType.objects.filter(SECRET_ASSIGNABLE_MODELS):
            GenericRelation(
                to=Secret,
                content_type_field='assigned_object_type',
                object_id_field='assigned_object_id',
                related_query_name=content_type.model,
            ).contribute_to_class(
                content_type.model_class(),
                'secrets',
            )
    except (OperationalError, ProgrammingError):
        pass


class NetBoxSecrets(PluginConfig):
    name = metadata.get('Name').replace('-', '_')
    verbose_name = metadata.get('Name')
    description = metadata.get('Summary')
    version = metadata.get('Version')
    author = metadata.get('Author')
    author_email = metadata.get('Author-email')
    base_url = 'secrets'
    min_version = '4.1.0'
    max_version = '4.1.99'
    required_settings = []
    default_settings = {
        'apps': ['dcim.device', 'virtualization.virtualmachine'],
        'display_default': 'left_page',
        'display_setting': {},
        'enable_contacts': False,
        'public_key_size': 2048,
    }

    def ready(self):
        super().ready()
        post_migrate.connect(configure_generic_relations, sender=self)


config = NetBoxSecrets
