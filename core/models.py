import enum

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


@enum.unique
class ComplexityTypes(enum.Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


@enum.unique
class ImpactTypes(enum.Enum):
    NONE = 'None'
    PARTIAL = 'Partial'
    COMPLETE = 'Complete'


class VulnerabilityType(models.Model):
    """
    Model used to describe the vulnerability types.
    """

    abbr = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128, blank=True)


class Vulnerability(models.Model):
    """
    Model used to describe the characteristics of a vulnerability. 
    """

    class Meta:
        verbose_name_plural = "vulnerabilities"

    cve_id = models.CharField(max_length=64, unique=True)
    vulnerability_type = models.ForeignKey(
        VulnerabilityType,
        null=True,
        blank=True,
        related_name='vulnerabilities',
        on_delete=models.PROTECT
    )
    publish_date = models.DateField()
    update_date = models.DateField()
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    access_complexity = models.CharField(
        max_length=64, choices=((s.value, s.name) for s in ComplexityTypes),
        help_text="How much knowledge or skill is required to exploit this vulnerabilty."
    )
    confidentiality_impact = models.CharField(
        max_length=64, choices=((s.value, s.name) for s in ImpactTypes),
        help_text="The degree of information disclosure, caused by this vulnerability."
    )
    integrity_impact = models.CharField(
        max_length=64, choices=((s.value, s.name) for s in ImpactTypes),
        help_text="How compromise the system is, due to this vulnerability."
    )
    availability_impact = models.CharField(
        max_length=64, choices=((s.value, s.name) for s in ImpactTypes),
        help_text="The level of impact on resource availability, caused by this vulnerability."
    )
    authentication_required = models.BooleanField()
