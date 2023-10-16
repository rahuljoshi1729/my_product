from django.urls import path
from productcatalog import views

urlpatterns=[
    path('',views.my_view,name="my_page"),
    path('product_list/',views.productlist.as_view(),name='product_list'),
    path('product_create/',views.ProductCreate.as_view(), name='product-create'),
    path('product_del/', views.delete_all_record.as_view(), name='delete-all-products'),
    path('product_detail/<int:PID>/',views.productdetail.as_view(),name='product-detail'),  #url parameter
    path('product_replace/<int:PID>/',views.productreplace.as_view(),name='product-replace'),
    path('product_update/<int:PID>/',views.PartialUpdateView.as_view(),name='field-update'),
    path('products_spec_del/<str:name>/',views.deleterecord.as_view(),name="specific-delete"),
    path('product/expensive/',views.expensiveproduct.as_view(),name='expensive-products'),
    path('product/not_available/',views.zeroinventory.as_view(),name='zero-inventory'),
    path('product/buy/',views.buyproduct.as_view(),name='buy-product'),
   # path('product/update/<int:PID>/',views.ProductDynamicUpdateView.as_view,name='update'),
]

