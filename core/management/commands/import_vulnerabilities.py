import csv
import logging

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import (
    ComplexityTypes,
    ImpactTypes,
    Vulnerability,
    VulnerabilityType
)


logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('core')


class Command(BaseCommand):
    help = "Imports the vulnerabilities data into the database."
    
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def get_vulnerability_data(self, row):
        vulnerability_type = None
        if row[4]:
            vulnerability_type = VulnerabilityType.objects.get_or_create(
                abbr=row[4]
            )[0]
        access_complexity = ComplexityTypes(row[10])
        confidentiality_impact = ImpactTypes(row[12])
        integrity_impact = ImpactTypes(row[13])
        availability_impact = ImpactTypes(row[14])
        if row[11] == 'Not required':
            authentication_required = False
        else:
            authentication_required = True

        return {
            'cve_id': row[1],
            'vulnerability_type_id': vulnerability_type.id if vulnerability_type else None,
            'publish_date': datetime.strptime(row[5], "%Y-%m-%d"),
            'update_date': datetime.strptime(row[6], "%Y-%m-%d"),
            'score': row[7],
            'access_complexity': access_complexity.value,
            'confidentiality_impact': confidentiality_impact.value,
            'integrity_impact': integrity_impact.value,
            'availability_impact': availability_impact.value,
            'authentication_required': authentication_required
        }
    
    @transaction.atomic()
    def insert_vulnerabilities(self, entries):
        for entry in entries:
            if not Vulnerability.objects.filter(cve_id=entry['cve_id']).exists():
                Vulnerability.objects.create(**entry)
                logger.info("Vulnerability with CVE ID %s created.", entry['cve_id'])
            else:
                logger.warning("Vulnerability with CVE ID %s already exists, skipping.", entry['cve_id'])
 
    def handle(self, *args, **options):
        with open(options['file']) as f:
            reader = csv.reader(f)

            # skip the first iteration, since we don't need the hearders
            iter_reader = iter(reader)
            next(iter_reader)

            entries = []
            for row in iter_reader:
                entries.append(self.get_vulnerability_data(row))

            self.insert_vulnerabilities(entries)
