from django.db import models
from django.utils.translation import gettext_lazy as _


class TinyTurret(models.Model):
    """Placeholder model with no database table, but with django admin page
    and contenttype permission"""
    class Meta:
        managed = False  # not in Django's database
        default_permissions = ()
        permissions = [['view', 'Access admin page']]


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


class Exception(TimeStampedModel):
    group = models.ForeignKey(ExceptionGroup, on_delete=models.CASCADE)
    exception_name = models.TextField(blank=True, null=True)
    exception_message = models.TextField(blank=True, null=True)
    base_file_name = models.TextField(blank=True, null=True)
    directory = models.TextField(blank=True, null=True)
    line_number = models.PositiveIntegerField(
        default=0
    )
    error_count = models.PositiveIntegerField(
        default=0
    )
