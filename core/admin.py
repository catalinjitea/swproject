from django.contrib import admin

from .models import Vulnerability, VulnerabilityType

class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ['cve_id',]
    
class VulnerabilityTypeAdmin(admin.ModelAdmin):
    list_display = ['abbr',]

admin.site.register(Vulnerability, VulnerabilityAdmin)
admin.site.register(VulnerabilityType, VulnerabilityTypeAdmin)
