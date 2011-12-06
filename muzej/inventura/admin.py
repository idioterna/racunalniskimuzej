import models
from django.contrib import admin
from django.contrib.auth.models import User

import ajax_select
import ajax_select.admin

class PrimerekInline(admin.StackedInline):
	model = models.Primerek
	extra = 0

class EksponatAdmin(ajax_select.admin.AjaxSelectAdmin):
	inlines = [
			PrimerekInline,
	]

	list_display = ('ime', 'tip', 'proizvajalec', 'leto_proizvodnje', 'st_primerkov')

	list_filter = ('proizvajalec',)

	search_fields = ('ime', 'tip')

	form = ajax_select.make_ajax_form(models.Eksponat, {'proizvajalec':'proizvajalec'})

class OsebaAdmin(admin.ModelAdmin):
	search_fields = ('ime',)

class PrimerekAdmin(ajax_select.admin.AjaxSelectAdmin):
	list_display = ('stevilka', 'eksponat', 'serijska_st', 'leto_proizvodnje')
	readonly_fields = ('inventariziral', 'datum_inventarizacije')

	form = ajax_select.make_ajax_form(models.Primerek, {'eksponat':'eksponat', 'donator':'oseba'})

	def save_model(self, request, obj, form, change):
		if not change:
			obj.inventariziral = request.user
		obj.save()

class VhodAdmin(ajax_select.admin.AjaxSelectAdmin):
	list_display = ('stevilka', 'lastnik', 'razlog', 'prevzel', 'cas_prevzema')

	search_fields = ('opis',)

	form = ajax_select.make_ajax_form(models.Vhod, {
		'izrocitelj':'oseba', 'lastnik':'oseba'})

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
admin.site.register(models.Oseba, OsebaAdmin)
admin.site.register(models.Vhod, VhodAdmin)
admin.site.register(models.Lokacija)
admin.site.register(models.Primerek, PrimerekAdmin)
admin.site.register(models.Zgodba)
