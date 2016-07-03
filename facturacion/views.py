from facturacion import models, forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .serializers import ProductoSerializer, FacturaSerializer
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import detail_route

# internas
productos_txt="productos"
ordenes_txt="ordenes"
orden_txt="orden"
login_url="/iniciar"
ok_msg = "ok"
error_msg = "error"

def obtener_ordenes(user):
    if user.usuario.tipo == 'Vendedor':
        return models.Factura.objects.filter(vendedor=user.usuario) 
    else:
        return models.Factura.objects.filter(comprador=user.usuario)

def obtener_productos(user):
    if user.usuario.tipo == 'Vendedor':
        return models.Producto.objects.filter(vendedor=user.usuario) 
    else:
        return models.Producto.objects.filter(activo=True) #cantidad > 0
		
def obtener_template(request, txt):
	if request.user.usuario.tipo == 'Vendedor':
		return 'granjero_'+txt+'.html'
	else:
		return 'comprador_'+txt+'.html'

# de URLs generales
def iniciar_sesion(request):
	error = '0'
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		loginform=AuthenticationForm(request.POST)
		pusername = request.POST['email']
		ppassword = request.POST['password']
		acc = authenticate(username=pusername, password=ppassword)

		if acc is not None and acc.is_active:
			login(request, acc)
			return HttpResponseRedirect('/')
		else:
			error = '1'
	else:
		loginform = AuthenticationForm()
	context = RequestContext(request,{'loginform':loginform,'error':error})
	return render_to_response('login.html',context)

def cerrar_session(request):
    logout(request)
    return HttpResponseRedirect('/iniciar')



@login_required(login_url=login_url)
def cambiar_clave(request):
	if request.method == 'POST':
		form = ClaveForm(request.POST)
		try:
			if form.is_valid():
				cu = User.objects.get(pk=request.user.id)				
				if cu.check_password(request.POST['oldpassword']):
					cu.set_password(request.POST['newpassword'])
					cu.save()
					return HttpResponseRedirect('/')
				else:
					form.errors['oldpassword'] = ErrorList([u"La 'contraseña anterior' indicada no es correcta."])
		except Exception:
			return render_to_response('alterpass.html', {'alterpassform':form},context_instance=RequestContext(request))
	else:
		form = ClaveForm()
	return render_to_response('alterpass.html', {'alterpassform':form}, context_instance=RequestContext(request))

@login_required(login_url=login_url)
def registro(request):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))

@login_required(login_url=login_url)
def index(request):
	lista = obtener_productos(request.user)
	return render_to_response(obtener_template(request,productos_txt), {'productos':lista})

@login_required(login_url=login_url)
def busqueda(request):
	lista = obtener_productos(request.user)
	if request.method=='POST':
		lista = lista.extra(where=['nombre like %"' + request.POST['filtro'] + '"'])
	return render_to_response('...html', {'productos':lista})

@login_required(login_url=login_url)
def categorias(request):
    lista = models.Categoria.objects.all()
    return render_to_response('categorias.html', {'categorias':lista})

@login_required(login_url=login_url)
def categoria(request, id):
    lista = obtener_productos(request.user).filter(categoria=id)    
    return render_to_response(obtener_template(request,productos_txt), {'productos':lista})


@login_required(login_url=login_url)
def producto(request, id):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))

@login_required(login_url=login_url)
def nuevo_producto(request):
	if request.method == 'POST':
		try:
			establecer_vendedor(request)
			form = crear_producto(request)
		except Exception:
	  		form = forms.ProductoForm(request.POST)
	else:
		form = forms.ProductoForm()
	return render_to_response('form_producto.html', {'form':form}, context_instance=RequestContext(request))

def crear_producto(request):
	form = forms.ProductoForm(request.POST) 
	if form.is_valid():
		form.save()
		return forms.ProductoForm()
	else:
		return form

def establecer_vendedor(request):
	request.POST._mutable = True
	request.POST['vendedor'] = request.user.usuario.id
	request.POST._mutable = False

@login_required(login_url=login_url)
def editar_producto(request, id):	
	producto_id = models.Producto.objects.get(pk=id)	
	if request.method == 'POST':
		try:
			establecer_vendedor(request)
			form = forms.ProductoForm(request.POST, instance=producto_id)		
			if form.is_valid():
				form.save()
		except Exception:
	  		form = forms.ProductoForm(instance=producto_id)
	else:
		form = forms.ProductoForm(instance=producto_id)		
	return render_to_response('form_producto.html', {'form':form}, context_instance=RequestContext(request))

@login_required(login_url=login_url)
def ordenes(request):
	lista =obtener_ordenes(request.user).filter(entregado=False).filter(anulado=False)
	return render_to_response(obtener_template(request,ordenes_txt), {'ordenes':lista})

@login_required(login_url=login_url)
def ordenes_historial(request):
	lista = obtener_ordenes(request.user)
	return render_to_response(obtener_template(request,ordenes_txt), {'ordenes':lista})

@login_required(login_url=login_url)
def orden(request, id):
	#hay que evaluar si es post, para ver si esta anulando o entregando, o anulando detalle
	item = obtener_ordenes(request.user).get(pk=id)
	return render_to_response(obtener_template(request,orden_txt),{'orden':item})

@login_required(login_url=login_url)
def comprador_producto(request, id):
    item = obtener_productos().get(pk=id)
    return render_to_response('...html', {'producto':'item'}, context_instance=RequestContext(request))

@login_required(login_url=login_url)
def granjeros(request):
    lista = models.Usuario.objects.all()
    return render_to_response('_vendedores.html', {'vendedores':lista})

@login_required(login_url=login_url)
def productos_de_granjero(request):
    lista = obtener_productos(request.user)
    return render_to_response('')

#API
class ProductoViewSet(viewsets.ModelViewSet): 
    serializer_class = ProductoSerializer
    queryset = models.Producto.objects.all()

class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    queryset = models.Factura.objects.all()
    
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])    
    def highlight(self, request, *args, **kwargs):
        factura = self.get_object()
        return Response(factura.highlighted)

    def perform_create(self, serializer):
        serializer.save()
