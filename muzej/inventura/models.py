# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Lokacija(models.Model):
	ime = models.CharField(
			max_length=255)

	naslov = models.TextField(blank=True)

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Lokacije"

def get_default_lokacija():
	return Lokacija.objects.get(ime="Skladišče Lesnina, Vič")

class Oseba(models.Model):
	ime = models.CharField(
			max_length=255,
			help_text="za fizične osebe uporabi obliko \"priimek, ime\"")

	naslov = models.TextField(blank=True)

	telefon = models.CharField(max_length=255, blank=True)

	email = models.EmailField(blank=True, null=True)

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Osebe"

class Vhod(models.Model):

	izrocitelj = models.ForeignKey(Oseba, blank=True, null=True, 
			related_name="izrocitelj",
			verbose_name=u"izročitelj",
			help_text=u"kdo je prinesel eksponat (če ni lastnik)")

	lastnik = models.ForeignKey(Oseba, 
			related_name="lastnik",
			help_text="kdo je trenutno lastnik eksponata")

	opis = models.TextField(
			help_text=u"kratek opis izročenih predmetov, stanje, vidne poškodbe, "
			u"zgodovina predmeta")

	RAZLOG_CHOICES = (
			('dar', 'dar'),
			('izposoja', 'izposoja'),
	)

	razlog = models.CharField(choices=RAZLOG_CHOICES, max_length=255,
			help_text="razlog za sprejem eksponata")

	zacasna_lokacija = models.ForeignKey(Lokacija,
			verbose_name="začasna lokacija",
			default=get_default_lokacija,
			blank=True, null=True)

	dogovorjeni_datum_vrnitve = models.DateField(blank=True, null=True)
	datum_vrnitve = models.DateField(blank=True, null=True,
			help_text="datum dejanske vrnitve")

	opombe = models.TextField(blank=True,
			help_text="podrobnosti glede vrnitve")

	prevzel = models.ForeignKey(User,
			help_text="sodelavec muzeja, ki je prevzel eksponat")

	cas_prevzema = models.DateTimeField(verbose_name="čas prevzema", blank=True, null=True)

	def stevilka(self):
		return "VH%05d" % (self.id,)
	stevilka.short_description = u'Številka'

	def inventorizirano(self):
		if Primerek.objects.filter(vhodni_dokument=self):
			return "da"
		else:
			return ""

	def __unicode__(self):
		return self.stevilka()

	def get_absolute_url(self):
		return "/vhod/%d/" % (self.id,)

	class Meta:
		verbose_name_plural = "Vhodi"

class Kategorija(models.Model):
	ime = models.CharField(
			max_length=255)

	opis = models.TextField()

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Kategorije"

class Proizvajalec(models.Model):
	ime = models.CharField(
			max_length=255)

	drzava = models.CharField(
			max_length=255,
			verbose_name="Država")

	ustanovljen = models.PositiveIntegerField(blank=True, null=True)
	propadel = models.PositiveIntegerField(blank=True, null=True)

	opis = models.TextField(blank=True)

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Proizvajalci"

class Eksponat(models.Model):
	ime = models.CharField(
			max_length=255,
			help_text=u"obče izdelka, ki ga eksponat predstavlja")

	tip = models.CharField(
			max_length=255,
			blank=True, null=True,
			help_text=u"tovarniška oznaka, številka tipa")

	proizvajalec = models.ForeignKey(Proizvajalec, blank=True, null=True)

	visina_cm = models.PositiveIntegerField(
			verbose_name=u"Višina [cm]")
	dolzina_cm = models.PositiveIntegerField(
			verbose_name=u"Dolžina [cm]")
	sirina_cm = models.PositiveIntegerField(
			verbose_name=u"Širina [cm]")

	opis = models.TextField(
			help_text=u"splošni opis izdelka, ki ga eksponat predstavlja, "
			u"in se ne nanaša na specifični primerek (naj vsebuje najmanj "
			u"fizični opis, po katerem je mogoče razpoznati eksponat: "
			"oblika, barva, ali je vgrajena tipkovnica, monitor, disketna "
			"enota, itd.)")

	kategorija = models.ForeignKey(Kategorija)

	def leto_proizvodnje(self):
		agg = self.primerek_set.aggregate(
				models.Min("leto_proizvodnje"), 
				models.Max("leto_proizvodnje"))

		leto_min = agg['leto_proizvodnje__min']
		leto_max = agg['leto_proizvodnje__max']

		if leto_min == leto_max:
			return str(leto_min)
		else:
			return "%d - %d" % (leto_min, leto_max) 

	def st_primerkov(self):
		return "%d" % self.primerek_set.count()
	st_primerkov.short_description = u'Št primerkov'

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Eksponati"

class Primerek(models.Model):
	inventarna_st = models.PositiveIntegerField(
			primary_key=True,
			verbose_name=u"Inventarna številka")

	eksponat = models.ForeignKey(Eksponat, blank=True, null=True,
			help_text=u"pusti prazno, če gre za muzejsko opremo in ne eksponat")

	st_delov = models.PositiveIntegerField(
			default=1,
			verbose_name=u"Število delov",
			help_text=u"iz koliko delov je sestavljen primerek (vsak del ima "
			u"svojo nalepko z inventarno št. in št. dela - npr. 12345/6)")

	serijska_st = models.CharField(
			max_length=255, blank=True,
			verbose_name="Serijska številka")

	leto_proizvodnje = models.PositiveIntegerField(blank=True, null=True)

	inventariziral = models.ForeignKey(
			User,
			help_text=u"kdo je iz vhodnega dokumenta naredil kataloški vnos")

	datum_inventarizacije = models.DateTimeField(auto_now_add=True)

	stanje = models.TextField(
			blank=True,
			help_text=u"opis stanja (poškodbe, posebnosti, spremembe) in "
			u"ostale opombe, specifične za ta primerek")

	zgodovina = models.TextField(
			blank=True,
			help_text=u"zgodovina primerka (zakaj se je uporabljal, kdo in kdaj)")

	donator = models.ForeignKey(
			Oseba, 
			blank=True,
			null=True,
			help_text=u"kdo je primerek podaril muzeju")

	lokacija = models.ForeignKey(Lokacija, default=get_default_lokacija)

	vhodni_dokument = models.ForeignKey(Vhod, blank=True, null=True)

	def stevilka(self):
		return "%04d" % (self.inventarna_st,)
	stevilka.short_description = u'Številka'

	def __unicode__(self):
		return unicode(self.inventarna_st)

	def get_absolute_url(self):
		return "/admin/inventura/primerek/%d/" % (self.pk,)

	class Meta:
		verbose_name_plural = "Primerki"

class Zgodba(models.Model):
	eksponat = models.ForeignKey(Eksponat)

	naslov = models.CharField(
			max_length=255)

	besedilo = models.TextField()

	def __unicode__(self):
		return self.naslov

	class Meta:
		verbose_name_plural = "Zgodbe"
