from django.contrib import admin
from django.urls import path, include
from myapp.views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('', include('myapp.include_urls.sign_urls')),
    path('product/', include('myapp.include_urls.interact_urls')),
    path('return/', include('myapp.include_urls.return_urls')),
]
