from django.contrib import admin

# Register your models here.
from .models import Candidate


class CandidateList(admin.ModelAdmin):
    list_display = ('fullName', 'entryDate', 'position')
    list_filter = ['entryDate', 'position']
    search_fields = ['fullName']


admin.site.register(Candidate, CandidateList)
