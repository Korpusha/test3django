from django.urls import path, re_path
from myapp.views import CreateProduct, UpdateProduct, BuyProduct, CartPage

urlpatterns = [
    path('create/', CreateProduct.as_view(), name='create_product'),
    path('buy/', BuyProduct.as_view(), name='buy_product'),
    re_path(r'^update/(?P<pk>\d+)/$', UpdateProduct.as_view(), name='update_product'),
    path('cart/', CartPage.as_view(), name='cart_product'),
]
