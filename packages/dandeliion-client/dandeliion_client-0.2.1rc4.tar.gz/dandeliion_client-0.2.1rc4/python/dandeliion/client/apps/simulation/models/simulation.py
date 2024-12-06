import importlib
from ..interfaces import http_requests
from dandeliion.client.tools import remote_model as models
from dandeliion.client.apps.simulation.core.models import __all__ as available_models
from ..core.models import fields


class Simulation(models.Model, metaclass=fields.serializers.SerializerMetaclass):

    STATUS_CHOICES = [
        ('Q', 'Queue'),
        ('R', 'Running'),
        ('F', 'Finished'),
        ('E', 'Error'),
        ('C', 'Cancelled'),
    ]

    id = fields.UUIDField(label='Job id', read_only=True)
    status = fields.ChoiceField(label="Current status of the simulation run",
                                choices=STATUS_CHOICES, read_only=True)

    owner = fields.CharField(read_only=True)

    # Header section
    job_name = fields.CharField(label="Job name",
                                help_text="A short name for your simulation to help identify it in the queue so "
                                + "that you can find your results. For example, Gr-Si/NCA battery 1C discharge.",
                                max_length=64)
    description = fields.CharField(label="Description (optional)",
                                   help_text="More space for additional description. "
                                   + "For example, you might provide a citation for the parameters you are using.",
                                   max_length=1024,
                                   required=False,
                                   allow_null=True,
                                   allow_blank=True)
    email = fields.EmailField(label="Email (optional, to send a notification once the job is complete)",
                              max_length=64,
                              required=False,
                              allow_null=True,
                              allow_blank=True)

    # Model section
    MODEL_CHOICES = [
        (model_name,
         getattr(importlib.import_module('dandeliion.client.apps.simulation.core.models'), model_name).label)
        for model_name in available_models
    ]
    model = fields.ChoiceField(label="Model", choices=MODEL_CHOICES,
                               help_text="Battery model used for the simulation.")
    params = fields.JSONField()
    meta = fields.JSONField(read_only=True)

    # Final checkboxes
    shared = fields.BooleanField(
        label="I want to make my simulation parameters and results public",
        help_text="(optional, links to the parametrisation and simulation results will be available "
        + "on the public Simulation Queue page, anyone will be able to access "
        + "the results and review the simulation parameters)",
        default=False
    )

    agree = fields.BooleanField(
        label="I agree to the DandeLiion Cloud Platform "
        + "<a href=\"https://simulation.dandeliion.com/tos/\" target=\"_blank\" rel=\"noopener\">Terms of Service</a>",
        default=False
    )

    # Date/Time
    time_submitted = fields.DateTimeField(label="Submission date", read_only=True)
    time_started = fields.DateTimeField(label="Start date", read_only=True)
    time_completed = fields.DateTimeField(label="Completion date", read_only=True)

    # Reason of stop
    stop_message = fields.CharField(max_length=256, read_only=True)

    class Meta:

        rest_api_cls = http_requests.REST_API  # overload api_client with app-specific version
        api_slug = 'simulation'
        pk = 'id'
