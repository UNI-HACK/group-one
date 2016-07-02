from facturacion import models
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

# internas
def obtener_ordenes(user):
    if user.usuario.tipo == 'Vendedor':
        return models.Factura.objects.filter(vendedor=user.usuario) 
    else:
        return models.Factura.objects.filter(comprador=user.usuario)

def obtener_productos(user):
    if user.usuario.tipo == 'Vendedor':
        return models.Producto.objects.filter(vendedor=user.usuario) 
    else:
        return models.Producto.objects.filter(activo=True)

# de URL
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
	file = ''
	if request.user.usuario.tipo == 'Vendedor':
		file = 'granjero_productos.html'
	else:
		file = 'comprador_productos.html'
	return render_to_response(file, {'productos':lista})

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
    return render_to_response('granjero_productos.html', {'productos':lista})

def granjero_producto(request, id):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))
    # esta podria ser, una createView y UpdateVIew de vistas genericas

def granjero_agregar(request):
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))
    # esta podria ser, una createView y UpdateVIew de vistas genericas

def granjero_ordenes(request):
    lista =obtener_ordenes().filter(entregado=False)
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))

def granjero_ordenes_historial(request):
    lista = obtener_ordenes()
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))

def granjero_orden(request, id):
    item = obtener_ordenes().get(pk=id)
    return render_to_response('...html', {'productos':'lista'}, context_instance=RequestContext(request))
    
def comprador_producto(request, id):
    item = obtener_productos().get(pk=id)
    return render_to_response('...html', {'producto':'item'}, context_instance=RequestContext(request))

def granjeros(request):
    lista = models.Usuario.objects.all()
    return render_to_response('vendedores.html', {'vendedores',lista})

def productos_de_granjero(request):
    lista = obtener_productos(request.user)
    return render_to_response('')
