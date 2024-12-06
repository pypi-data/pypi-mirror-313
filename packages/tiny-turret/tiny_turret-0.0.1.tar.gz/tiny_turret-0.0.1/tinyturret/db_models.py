

class TimeStampedModel(models.Model):

    created = models.DateTimeField(
        auto_now_add=True, editable=False,
        db_index=True, verbose_name=_('Creation date'))
    modified = models.DateTimeField(
        auto_now=True, editable=False, db_index=True,
        verbose_name=_('Modification date'))

    # pylint: disable=old-style-class
    class Meta:
        abstract = True

from django.db.models import JSONField

from django.core.serializers.json import DjangoJSONEncoder


class ExceptionGroup(TimeStampedModel):

    first_seen = models.DateTimeField(
        db_index=True, blank=True,
        verbose_name=_('Creation date')
    )
    last_seen = models.DateTimeField(
        db_index=True, blank=True,
        verbose_name=_('Creation date'),
    )
    error_count = models.PositiveIntegerField(
        default=0
    )


class ExceptionGroup(TimeStampedModel):
    exception_group = models.ForeignKey(ExceptionGroup)
    stack_trace = extra = JSONField(
        default=dict, encoder=DjangoJSONEncoder
    )
     = models.TextField(
        default='', null=True, blank=True
    )
