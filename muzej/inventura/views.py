from django.shortcuts import render, redirect

from muzej.inventura.models import Vhod

def vhod(request, id):
	vhod = Vhod.objects.get(pk=id)
	context = {
			'vhod': vhod,
		}
	return render(request, 'vhod.html', context)

def vhod_short(request, id):
	vhod = Vhod.objects.get(pk=id)
	return redirect(vhod)
