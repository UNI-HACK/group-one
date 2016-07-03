"""flashsale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import DetailView, CreateView, UpdateView
from facturacion import views, models

from rest_framework import renderers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'producto', views.ProductoViewSet)
router.register(r'factura', views.FacturaViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^iniciar$', views.iniciar_sesion),
    url(r'^salir$', views.cerrar_session),
    url(r'^registro$', views.registro), #falta
    url(r'^clave$', views.cambiar_clave), #falta
    url(r'^$', views.index),
    url(r'^busqueda$', views.busqueda), #falta
    url(r'^categorias$', views.categorias),
    url(r'^categorias/(\d)$', views.categoria),
    url(r'^productos/(\d)$', views.producto), #falta
    url(r'^productos/editar/(\d)$', views.editar_producto), #falta
    url(r'^productos/nuevo$', views.nuevo_producto),

    url(r'^ordenes$', views.ordenes),
    url(r'^ordenes/(\d)$', views.orden), #falta
    url(r'^ordenes/historial$', views.ordenes_historial),
    url(r'^granjeros$', views.granjeros), #falta
    url(r'^granjeros/(\d)$', views.productos_de_granjero), #falta

    #API
    url(r'^api/', include(router.urls)),
    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
