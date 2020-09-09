import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from core.models import Vulnerability


class ChartView(LoginRequiredMixin, TemplateView):
    template_name = "charts.html"

    def get_column_chart_skeleton(self):
        return {
            'chart': {
                'type': 'column'
            },
            'title': {
                'text': None
            },
            'xAxis': {
                'type': 'category',
            },
            'yAxis': {
                'title': {
                    'text': 'Number of vulnerabilities'
                }
            },
            'plotOptions': {
                'series': {
                    'dataLabels': {
                        'enabled': True
                    }
                }
            },
            'series': [{
                'colorByPoint': True,
                'data': None
            }]
        }

    def get_pie_chart_skeleton(self):
        return {
            'chart': {
                'type': 'pie'
            },
            'title': {
                'text': None
            },
            'plotOptions': {
                'pie': {
                    'cursor': 'pointer',
                    'dataLabels': {
                        'enabled': True,
                        'format': '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            'series': [{
                'colorByPoint': True,
                'data': None
            }]
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = Vulnerability.objects

        years_count = qs.values('publish_date__year').annotate(
            dcount=Count('publish_date__year')
        )
        years_chart = self.get_column_chart_skeleton()
        years_chart['title']['text'] = 'Number of vulnerabilities by year'
        years_chart['yAxis']['title']['text'] = 'Number of vulnerabilities'
        years_chart['series'][0]['data'] = [
            {'name': year['publish_date__year'], 'y': year['dcount']}
            for year in years_count
        ]

        vtypes_count = qs.values('vulnerability_type__abbr').annotate(
            dcount=Count('vulnerability_type__abbr')
        )
        vtypes_chart = self.get_column_chart_skeleton()
        vtypes_chart['title']['text'] = 'Number of vulnerabilities by vulnerability type'
        vtypes_chart['yAxis']['title']['text'] = 'Number of appereances'
        vtypes_chart['series'][0]['data'] = [
            {'name': vtype['vulnerability_type__abbr'], 'y': vtype['dcount']}
            for vtype in vtypes_count
            if vtype['vulnerability_type__abbr']
        ]

        vtypes_pie_chart = self.get_pie_chart_skeleton()
        vtypes_pie_chart['title']['text'] = 'Vulnerabilities type share'
        vtypes_pie_chart['series'][0]['data'] = [
            {'name': vtype['vulnerability_type__abbr'], 'y': vtype['dcount']}
            for vtype in vtypes_count
            if vtype['vulnerability_type__abbr']
        ]

        integrity_impacts_count = qs.values('integrity_impact').annotate(
            dcount=Count('integrity_impact')
        )
        integrity_impacts_chart = self.get_pie_chart_skeleton()
        integrity_impacts_chart['title']['text'] = 'The impact of vulnerabilities on system integrity share'
        integrity_impacts_chart['series'][0]['data'] = [
            {'name': integrity_impact['integrity_impact'], 'y': integrity_impact['dcount']}
            for integrity_impact in integrity_impacts_count
        ]

        availability_impacts_count = qs.values('availability_impact').annotate(
            dcount=Count('availability_impact')
        )
        availability_impacts_chart = self.get_pie_chart_skeleton()
        availability_impacts_chart['title']['text'] = 'The impact of vulnerabilities on system availability share'
        availability_impacts_chart['series'][0]['data'] = [
            {'name': availability_impact['availability_impact'], 'y': availability_impact['dcount']}
            for availability_impact in availability_impacts_count
        ]

        years_dump = json.dumps(years_chart)
        vtypes_dump = json.dumps(vtypes_chart)
        vtypes_pie_dump = json.dumps(vtypes_pie_chart)
        integrity_impacts_dump = json.dumps(integrity_impacts_chart)
        availability_impacts_dump = json.dumps(availability_impacts_chart)


        context['years_chart'] = years_dump
        context['vtypes_chart'] = vtypes_dump
        context['vtypes_pie_chart'] = vtypes_pie_dump
        context['integrity_impacts_chart'] = integrity_impacts_dump
        context['availability_impacts_chart'] = availability_impacts_dump

        return context
