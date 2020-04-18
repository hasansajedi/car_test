from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include(('app.urls', 'app'), namespace='app')),
]
urlpatterns += staticfiles_urlpatterns()
