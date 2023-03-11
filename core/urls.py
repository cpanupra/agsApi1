
from django.urls import path
from .views import Api_Ore, ApiCategorias, ApiProductos, ApiProductosDetalle, ApiCategoriaProducto, registerProducto, \
    buscaData,AgregarVeterinario,AgusIncaRail

urlpatterns = [
    # se coloca as_view cuando es una vista basada en clase
    path('Api/ApiCategorias/', ApiCategorias.as_view(),name="ApiCategorias"),
    path('Api/ApiProductos/', ApiProductos.as_view(), name="ApiProductos"),
    path('Api/ApiProductosDetalle/', ApiProductosDetalle.as_view(), name="ApiProductosDetalle"),
    path('Api/ApiCategoriaProducto/', ApiCategoriaProducto.as_view(), name="ApiCategoriaProducto"),
    path('Api/ApiregisterProducto/', registerProducto.as_view(),name="ApiregisterProducto"),
    path('Api/buscaData/', buscaData.as_view(),name="buscaData"),
    path('Api/addVeterinario/', AgregarVeterinario.as_view(),name="addVeterinario"),
    path('Api/AgusIncaRail/', AgusIncaRail.as_view(),name="AgusIncaRail"),
    path('', Api_Ore,name="Api_ore"),
]