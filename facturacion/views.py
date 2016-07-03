from facturacion import models
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

# internas
productos_txt="productos"
ordenes_txt="ordenes"
orden_txt="orden"

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

def registro(request):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))

def index(request):
	lista = obtener_productos(request.user)
	return render_to_response(obtener_template(request,productos_txt), {'productos':lista})

def busqueda(request):
	lista = obtener_productos(request.user)
	if request.method=='POST':
		lista = lista.extra(where=['nombre like %"' + request.POST['filtro'] + '"'])
	return render_to_response('...html', {'productos':lista})

def categorias(request):
    lista = models.Categoria.objects.all()
    return render_to_response('categorias.html', {'categorias':lista})

def categoria(request, id):
    lista = obtener_productos(request.user).filter(categoria=id)    
    return render_to_response(obtener_template(request,productos_txt), {'productos':lista})


def producto(request, id):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))

def nuevo_producto(request):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))
    # esta podria ser, una createView y UpdateVIew de vistas genericas

def editar_producto(request, id):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))
    # esta podria ser, una createView y UpdateVIew de vistas genericas

def ordenes(request):
	lista =obtener_ordenes(request.user).filter(entregado=False).filter(anulado=False)
	return render_to_response(obtener_template(request,ordenes_txt), {'ordenes':lista})

def ordenes_historial(request):
	lista = obtener_ordenes(request.user)
	return render_to_response(obtener_template(request,ordenes_txt), {'ordenes':lista})

def orden(request, id):
	#hay que evaluar si es post, para ver si esta anulando o entregando, o anulando detalle
	item = obtener_ordenes(request.user).get(pk=id)
	return render_to_response(obtener_template(request,orden_txt),{'orden':item})

def comprador_producto(request, id):
    item = obtener_productos().get(pk=id)
    return render_to_response('...html', {'producto':'item'}, context_instance=RequestContext(request))

def granjeros(request):
    lista = models.Usuario.objects.all()
    return render_to_response('_vendedores.html', {'vendedores':lista})

def productos_de_granjero(request):
    lista = obtener_productos(request.user)
    return render_to_response('')
