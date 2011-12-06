from django.shortcuts import render, redirect

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
	vhod = Vhod.objects.get(pk=id)
	return redirect(vhod)

def primerek_short(request, id):
	primerek = Primerek.objects.get(pk=id)
	return redirect(primerek)
