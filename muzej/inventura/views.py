import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from django import forms

from muzej.inventura.models import Vhod, Primerek, Lokacija

def root(request):
	return redirect('/admin/')

@login_required
def vhod(request, id):
	vhod = Vhod.objects.get(pk=id)
	context = {
			'vhod': vhod,
		}
	return render(request, 'vhod.html', context)

@login_required
def vhod_short(request, id):
	try:
		vhod = Vhod.objects.get(pk=id)
	except Vhod.DoesNotExist:
		raise Http404
	return redirect(vhod)

@login_required
def primerek_short(request, id):
	try:
		primerek = Primerek.objects.get(pk=id)
	except Primerek.DoesNotExist:
		raise Http404
	return redirect(primerek)

class PremikForm(forms.Form):
	zapisnik = forms.CharField(widget=forms.Textarea)
	lokacija = forms.ModelChoiceField(queryset=Lokacija.objects.all())

@login_required
def premik(request):
	if request.method == 'POST':
		form = PremikForm(request.POST)
		if form.is_valid():

			zapisnik = form.cleaned_data['zapisnik']
			lokacija = form.cleaned_data['lokacija']

			id_set = set()
			for id in re.findall("http://racunalniski-muzej.si/i/([0-9]+)/?", zapisnik, re.I):
				id_set.add(int(id))

			primerki = []
			for id in id_set:
				try:
					primerek = Primerek.objects.get(pk=id)
					primerki.append(primerek)
				except Primerek.DoesNotExist:
					messages.add_message(request, messages.ERROR,
							"Ne najdem primerka %d!" % (id,))

			for primerek in primerki:
				primerek.lokacija = lokacija
				primerek.save()

			messages.add_message(request, messages.SUCCESS,
					"Premaknil %d primerkov na lokacijo %s." % (len(primerki), lokacija))

	else:
		form = PremikForm() # An unbound form

	context = {'form': form}
	return render(request, 'premik.html', context)
