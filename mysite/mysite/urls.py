from django.contrib import admin
from django.urls import path, include
from myapp.views import HomePage, CreateProduct, UpdateProduct, BuyProduct, \
    ReturnProduct, ReturnPage, DeleteReturnObj

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('', include('myapp.sign_urls.myapp_urls')),
    path('product/', include('myapp.admin_urls.interact_urls')),
    path('return-page/', ReturnPage.as_view(), name='return_page'),
    path('return-success-del/<int:pk>/', DeleteReturnObj.as_view(), name='return_success_del'),
]
