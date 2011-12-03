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
			verbose_name="izročitelj",
			help_text="kdo je prinesel eksponat (če ni lastnik)")

	lastnik = models.ForeignKey(Oseba, 
			related_name="lastnik",
			help_text="kdo je trenutno lastnik eksponata")

	opis = models.TextField(
			help_text="kratek opis izročenih predmetov, stanje, vidne poškodbe, "
			"zgodovina predmeta")

	RAZLOG_CHOICES = (
			('dar', 'dar'),
			('izposoja', 'izposoja'),
	)

	razlog = models.CharField(choices=RAZLOG_CHOICES, max_length=255,
			help_text="razlog za sprejem eksponata")

	zacasna_lokacija = models.ForeignKey(Lokacija,
			verbose_name="začasna lokacija",
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
			max_length=255)

	tip = models.CharField(
			max_length=255)

	proizvajalec = models.ForeignKey(Proizvajalec)

	leto_proizvodnje = models.PositiveIntegerField(blank=True, null=True)

	visina_cm = models.PositiveIntegerField(
			verbose_name="Višina [cm]")
	dolzina_cm = models.PositiveIntegerField(
			verbose_name="Dolžina [cm]")
	sirina_cm = models.PositiveIntegerField(
			verbose_name="Širina [cm]")

	opis = models.TextField(
			help_text="splošni opis izdelka, ki ga eksponat predstavlja, "
			"in se ne nanaša na specifični primerek (naj vsebuje najmanj "
			"fizični opis, po katerem je mogoče razpoznati eksponat)")

	kategorija = models.ForeignKey(Kategorija)

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Eksponati"

def get_default_lokacija():
	return Lokacija.objects.get(ime="Skladišče Lesnina, Vič")

class Primerek(models.Model):
	inventarna_st = models.PositiveIntegerField(
			primary_key=True,
			verbose_name="Inventarna številka")

	eksponat = models.ForeignKey(Eksponat, blank=True, null=True,
			help_text="pusti prazno, če gre za muzejsko opremo in ne eksponat")

	st_delov = models.PositiveIntegerField(
			default=1,
			verbose_name="Število delov",
			help_text="iz koliko delov je sestavljen primerek (vsak del ima "
			"svojo nalepko z inventarno št. in št. dela - npr. 12345/6)")

	serijska_st = models.CharField(
			max_length=255, blank=True,
			verbose_name="Serijska številka")

	inventariziral = models.ForeignKey(
			User,
			help_text="kdo je iz vhodnega dokumenta naredil kataloški vnos")

	datum_inventarizacije = models.DateTimeField(auto_now_add=True)

	stanje = models.TextField(
			blank=True,
			help_text="opis stanja (poškodbe, posebnosti, spremembe) in "
			"ostale opombe, specifične za ta primerek")

	donator = models.ForeignKey(
			Oseba, 
			blank=True,
			null=True,
			help_text="kdo je primerek podaril muzeju")

	lokacija = models.ForeignKey(Lokacija, default=get_default_lokacija)

	def stevilka(self):
		return "IN%05d" % (self.inventarna_st,)

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
