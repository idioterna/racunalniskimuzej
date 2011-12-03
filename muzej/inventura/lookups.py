from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from django.core import urlresolvers
import muzej.inventura.models as models

class InventuraLookup(LookupChannel):

	def get_query(self, q, request):
        	return self.model.objects.filter(Q(ime__icontains=q)).order_by('ime')

	def format_item_display(self, obj):
		change_url = urlresolvers.reverse('admin:inventura_' + 
			self.model.__name__.lower() + '_change', args=(obj.id,))
		return u'%s <a href="%s">edit</a>' % (escape(unicode(obj)), change_url)

class EksponatLookup(InventuraLookup):

	model = models.Eksponat

	def get_query(self, q, request):
        	return models.Eksponat.objects.filter(Q(ime__icontains=q) | Q(tip__icontains=q)).order_by('ime')

class OsebaLookup(InventuraLookup):
	model = models.Oseba

class ProizvajalecLookup(InventuraLookup):
	model = models.Proizvajalec
