from django.shortcuts import render, redirect
from django.http import Http404

from muzej.inventura.models import Vhod, Primerek

def root(request):
	return redirect('/admin/')

def vhod(request, id):
	vhod = Vhod.objects.get(pk=id)
	context = {
			'vhod': vhod,
		}
	return render(request, 'vhod.html', context)

def vhod_short(request, id):
	try:
		vhod = Vhod.objects.get(pk=id)
	except Vhod.DoesNotExist:
		raise Http404
	return redirect(vhod)

def primerek_short(request, id):
	try:
		primerek = Primerek.objects.get(pk=id)
	except Primerek.DoesNotExist:
		raise Http404
	return redirect(primerek)
