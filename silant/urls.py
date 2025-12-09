from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from machines.api import MachineViewSet, machine_search
from maintenance.api import MaintenanceViewSet
from claims.api import ClaimViewSet

from machines.views import MachineDetailView, machine_search_view


router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machines')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'claims', ClaimViewSet, basename='claims')


schema_view = get_schema_view(
   openapi.Info(
      title="Silant API",
      default_version='v1',
      description="Документация API для проекта СИЛАНТ",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),

   path("", include("machines.urls")),
   path('reference/', include('references.urls')),
   path('maintenance/', include('maintenance.urls')),
   path('claims/', include('claims.urls')), 

   path('api/', include(router.urls)),
   path('api/search/', machine_search, name='machine-search'),
   path('api-auth/', include('rest_framework.urls')),

   path("accounts/", include("allauth.urls")),

   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


handler403 = "silant.views.custom_403"
handler404 = "silant.views.custom_404"
handler500 = "silant.views.custom_500"




