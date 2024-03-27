from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def products_list(request):
    """
    Handle GET and POST requests for the product list.
    
    GET: Return a list of all products.
         Response status: 200 OK
         Response format: JSON array of product objects.
    
    POST: Create a new product with provided data.
          Required data: 'name', 'description', 'price', 'stock'
          Response status: 201 Created on successful creation.
                           400 Bad Request if the data is invalid.
          Response format: JSON object of the created product.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Handle GET, PUT, and DELETE requests for a single product.
    
    GET: Retrieve a specific product by its 'pk'.
         Response status: 200 OK if found, 404 Not Found if not found.
         Response format: JSON object of the product.
    
    PUT: Update a specific product with provided data.
         Required data: Any product fields to update.
         Response status: 200 OK on successful update,
                          400 Bad Request if the data is invalid,
                          404 Not Found if the product is not found.
         Response format: JSON object of the updated product.
    
    DELETE: Delete a specific product.
            Response status: 204 No Content on successful deletion,
                             404 Not Found if the product is not found.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
