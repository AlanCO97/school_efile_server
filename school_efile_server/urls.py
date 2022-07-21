from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import  static
from school_efile_server.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('auth.urls'), name='auth'),
    path('api/v1/efileConfig/', include('school_config.urls'), name='efileConfig'),
    path('api/v1/efile/', include('efile.urls'), name='efile')
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
