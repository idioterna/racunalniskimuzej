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
			max_length=255)

	naslov = models.TextField(blank=True)

	telefon = models.CharField(max_length=255, blank=True)

	email = models.EmailField(blank=True, null=True)

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Osebe"

class Vhod(models.Model):

	izrocitelj = models.ForeignKey(Oseba, null=True, 
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

	zacasna_lokacija = models.ForeignKey(Lokacija,
			verbose_name="začasna lokacija",
			blank=True, null=True)

	razlog = models.CharField(choices=RAZLOG_CHOICES, max_length=255,
			help_text="razlog za sprejem eksponata")

	dogovorjeni_datum_vrnitve = models.DateField(blank=True, null=True)
	datum_vrnitve = models.DateField(blank=True, null=True,
			help_text="datum dejanske vrnitve")

	opombe = models.TextField(blank=True,
			help_text="podrobnosti glede vrnitve")

	prevzel = models.ForeignKey(User,
			help_text="sodelavec muzeja, ki je prevzel eksponat")

	cas_prevzema = models.DateTimeField(verbose_name="čas prevzema")

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

	opis = models.TextField()

	kategorija = models.ForeignKey(Kategorija)

	def __unicode__(self):
		return self.ime

	class Meta:
		verbose_name_plural = "Eksponati"

class Primerek(models.Model):
	inventarna_st = models.PositiveIntegerField(
			primary_key=True,
			verbose_name="Inventarna številka")

	serijska_st = models.CharField(
			max_length=255, blank=True,
			verbose_name="Serijska številka")

	inventariziral = models.ForeignKey(User)

	datum_inventarizacije = models.DateTimeField(auto_now_add=True)

	stanje = models.TextField(blank=True)

	donator = models.ForeignKey(Oseba, blank=True, null=True)

	lokacija = models.ForeignKey(Lokacija)

	eksponat = models.ForeignKey(Eksponat)

	def __unicode__(self):
		return unicode(self.inventarna_st)

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
