import models
from django.contrib import admin
from django.contrib.auth.models import User

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

class PrimerekInline(admin.StackedInline):
	model = models.Primerek
	extra = 1

class ProizvajalecAutocomplete(AutocompleteSettings):
	search_fields = ('^ime',)

autocomplete.register(models.Eksponat.proizvajalec, ProizvajalecAutocomplete)

class EksponatAdmin(AutocompleteAdmin, admin.ModelAdmin):
	inlines = [
			PrimerekInline,
	]

	list_display = ('ime', 'tip', 'proizvajalec')

	list_filter = ('proizvajalec',)

class EksponatAutocomplete(AutocompleteSettings):
	search_fields = ('^ime', 'tip')

autocomplete.register(models.Primerek.eksponat, EksponatAutocomplete)

class PrimerekAdmin(AutocompleteAdmin, admin.ModelAdmin):
	list_display = ('inventarna_st', 'eksponat', 'serijska_st')

class VhodAdmin(admin.ModelAdmin):
	list_display = ('stevilka', 'lastnik', 'razlog', 'prevzel', 'cas_prevzema')

	fieldsets = (
			(None, {
				'fields': (	'izrocitelj', 'lastnik', 'opis', 'razlog',
						'zacasna_lokacija', 'prevzel', 'cas_prevzema'),
			}),
			('Vrnitev', {
				'fields': (	'dogovorjeni_datum_vrnitve', 'datum_vrnitve', 'opombe'),
			}),
		)

admin.site.register(models.Kategorija)
admin.site.register(models.Proizvajalec)
admin.site.register(models.Eksponat, EksponatAdmin)
admin.site.register(models.Oseba)
admin.site.register(models.Vhod, VhodAdmin)
admin.site.register(models.Lokacija)
admin.site.register(models.Primerek, PrimerekAdmin)
admin.site.register(models.Zgodba)
