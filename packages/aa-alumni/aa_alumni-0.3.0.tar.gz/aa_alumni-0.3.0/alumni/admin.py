from django.contrib import admin

from .models import (
    AlumniSetup, CharacterCorporationHistory, CorporationAllianceHistory,
)


@admin.register(AlumniSetup)
class AlumniSetupAdmin(admin.ModelAdmin):
    search_fields = ['alumni_corporations', ]
    filter_horizontal = ["alumni_corporations", "alumni_alliances"]


@admin.register(CorporationAllianceHistory)
class CorporationAllianceHistoryAdmin(admin.ModelAdmin):
    search_fields = ['corporation_id', 'alliance_id']
    list_display = ('corporation_id', 'alliance_id')


@admin.register(CharacterCorporationHistory)
class CharacterCorporationHistoryAdmin(admin.ModelAdmin):
    search_fields = ['corporation_id', 'character']
    list_display = ('corporation_id', 'character')
