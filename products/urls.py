from django.urls import path
from . import views

urlpatterns = [
    # Endpoint for retrieving the list of products or adding a new product.
    # GET: Returns a list of all products.
    # POST: Creates a new product with the provided data.
    path('products/', views.products_list, name='products-list'),
    
    # Endpoint for CRUD operations on a specific product identified by 'pk'.
    # GET: Returns the details of a specific product.
    # PUT: Updates an existing product with the provided data.
    # DELETE: Deletes a specific product.
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
]
