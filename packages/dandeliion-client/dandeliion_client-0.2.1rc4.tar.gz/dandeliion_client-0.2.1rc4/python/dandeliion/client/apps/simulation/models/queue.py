import importlib
from ..interfaces import http_requests
from dandeliion.client.tools import remote_model as models
from dandeliion.client.apps.simulation.core.models import __all__ as available_models
from ..core.models import fields


class Queue(models.Model, metaclass=fields.serializers.SerializerMetaclass):

    STATUS_CHOICES = [
        ('Q', 'Queue'),
        ('R', 'Running'),
        ('F', 'Finished'),
        ('E', 'Error'),
        ('C', 'Cancelled'),
    ]

    id = fields.UUIDField(label='Job id', read_only=True)
    status = fields.ChoiceField(label="Status",
                                choices=STATUS_CHOICES, default='Q', read_only=True)

    owner = fields.CharField(label="Owner", read_only=True)

    # Header section
    job_name = fields.CharField(label="Job name",
                                help_text="A short name for your simulation to help identify it in the queue so "
                                + "that you can find your results. For example, Gr-Si/NCA battery 1C discharge.",
                                read_only=True)
    description = fields.CharField(label="Description",
                                   help_text="More space for additional description. "
                                   + "For example, you might provide a citation for the parameters you are using.",
                                   read_only=True,
                                   allow_null=True,
                                   allow_blank=True)
    email = fields.EmailField(label="Email",
                              read_only=True,
                              allow_null=True,
                              allow_blank=True)

    # Model section
    MODEL_CHOICES = [
        (model_name,
         getattr(importlib.import_module('dandeliion.client.apps.simulation.core.models'), model_name).label)
        for model_name in available_models
    ]
    model = fields.ChoiceField(label="Model", choices=MODEL_CHOICES,
                               help_text="Battery model used for the simulation.",
                               read_only=True)

    shared = fields.BooleanField(
        label="shared",
        help_text="(optional, links to the parametrisation and simulation results will be available "
        + "on the public Simulation Queue page, anyone will be able to access "
        + "the results and review the simulation parameters)",
        read_only=True,
        default=False
    )

    # Date/Time
    time_submitted = fields.DateTimeField(label="Submission date", read_only=True)
    time_started = fields.DateTimeField(label="Start date", read_only=True)
    time_completed = fields.DateTimeField(label="Completion date", read_only=True)

    class Meta:

        rest_api_cls = http_requests.REST_API  # overload api_client with app-specific version
        api_slug = 'queue'
        pk = 'id'
