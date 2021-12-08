from django.urls import path, re_path
from myapp.views import ReturnProduct, ReturnPage, DeleteReturnObj

urlpatterns = [
    path('', ReturnProduct.as_view(), name='return_'),
    path('page', ReturnPage.as_view(), name='return_page'),
    re_path(r'^success-del/(?P<pk>\d+)/$', DeleteReturnObj.as_view(), name='return_del'),
]
