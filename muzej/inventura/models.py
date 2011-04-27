# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Kategorija(models.Model):
	ime = models.CharField(
			max_length=255)

class Proizvajalec(models.Model):
	ime = models.CharField(
			max_length=255)

	drzava = models.CharField(
			max_length=255)

	ustanovljen = models.PositiveIntegerField(blank=True)
	propadel = models.PositiveIntegerField(blank=True)

	opis = models.TextField()

class Eksponat(models.Model):
	ime = models.CharField(
			max_length=255)

	tip = models.CharField(
			max_length=255)

	proizvajalec = models.ForeignKey(Proizvajalec)

	leto_proizvodnje = models.PositiveIntegerField(blank=True)

	visina_cm = models.PositiveIntegerField()
	dolzina_cm = models.PositiveIntegerField()
	sirina_cm = models.PositiveIntegerField()

	opis = models.TextField()

	kategorija = models.ForeignKey(Kategorija)

class Donator(models.Model):
	ime = models.CharField(
			max_length=255)

class Lokacija(models.Model):
	ime = models.CharField(
			max_length=255)

class Primerek(models.Model):
	inventarna_st = models.PositiveIntegerField(
			primary_key=True,
			verbose_name="Inventarna številka")

	serijska_st = models.CharField(
			max_length=255, blank=True)

	inventariziral = models.ForeignKey(User)

	datum_inventarizacije = models.DateTimeField(auto_now_add=True)

	stanje = models.TextField()

	donator = models.ForeignKey(Donator, blank=True)

	lokacija = models.ForeignKey(Lokacija)

	eksponat = models.ForeignKey(Eksponat)

class Zgodba(models.Model):
	eksponat = models.ForeignKey(Eksponat)

	naslov = models.CharField(
			max_length=255)

	besedilo = models.TextField()
