
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include

urlpatterns = [

    path('admin/', admin.site.urls),    
    path('api/', include(('api.crm.router', 'api'), namespace='api')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
