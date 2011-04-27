import models
from django.contrib import admin
from django.contrib.auth.models import User

class PrimerekInline(admin.StackedInline):
	model = models.Primerek
	extra = 1

class EksponatAdmin(admin.ModelAdmin):
	inlines = [
			PrimerekInline,
	]

	list_display = ('ime', 'tip', 'proizvajalec')

	list_filter = ('proizvajalec',)

class PrimerekAdmin(admin.ModelAdmin):
	list_display = ('inventarna_st', 'eksponat', 'serijska_st')

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
       		if db_field.name == "inventariziral":
			print db_field.name
            		kwargs["queryset"] = User.objects.filter(id=request.user.id)

        	return super(PrimerekAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Kategorija)
admin.site.register(models.Proizvajalec)
admin.site.register(models.Eksponat, EksponatAdmin)
admin.site.register(models.Donator)
admin.site.register(models.Lokacija)
admin.site.register(models.Primerek, PrimerekAdmin)
admin.site.register(models.Zgodba)
