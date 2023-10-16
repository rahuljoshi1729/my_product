from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from productcatalog.models import Product
from productcatalog.serializers import ProdSerializer
from productcatalog.serializers import partialupdateserializer,deleteparticular,ProductDynamicUpdateSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound

def my_view(request):
    return render(request, 'index.html')

#1/products (method: GET): This should retrieve all product records
class productlist(generics.ListAPIView):
    queryset=Product.objects.all()   #to get data from product table defined in model.py
    serializer_class=ProdSerializer   # to call serializer for coverting complex data to simple one




"""a. ProductList: This view extends generics.ListCreateAPIView, which provides a GET (list) and POST (create) 
endpoint for a list of products. It sets the queryset attribute to fetch all products from the Product model and uses the ProductSerializer to serialize the data.
"""


#2/products (method: POST):  This route should create a new product record.
class ProductCreate(generics.CreateAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProdSerializer   


#3/products (method: DELETE): This route should delete all product records.
class delete_all_record(generics.DestroyAPIView): #to delete all the table
    queryset = Product.objects.all()
    serializer_class = ProdSerializer  

    def delete(self, request, *args, **kwargs):
        # Delete all records in the Product model
        Product.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     
  


#4/product (method: GET | use params or query string: PID): This route should fetch the record of a particular product.
class productdetail(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdSerializer
    lookup_field='PID'

#5/product (method: PUT |  use params or query string: PID): This route should replace a product record with another product record.  
class productreplace(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdSerializer
    lookup_field='PID'

#UpdateAPIView: to handle PUT request ,update the fields
#6/product (method: PATCH | use params or query string: PID): This route should update some product record fields.
class PartialUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = partialupdateserializer
    lookup_field = 'PID'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

# 7/product  (method: DELETE | use params or query string: PID): This route should delete the record of a particular product.
class deleterecord(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class:deleteparticular
    lookup_field='name'
    def get_object(self):
        name = self.kwargs['name']  # Get the product name from the URL parameter
        product = self.queryset.filter(name=name).first()
        
        if product:
            return product
        else:
            raise NotFound(detail=f'Product with name "{name}" not found')

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({'message': f'Product with name "{product.name}" deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#8/product/expensive (request method: GET | use query string specifying p): This route should return sorted records of top p products based on price.
class expensiveproduct(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdSerializer
    

    def get_queryset(self):
        p = self.request.query_params.get('p')
        if not p or not p.isdigit():
            p = 10  # Default to 10 if 'p' is not provided or not a valid number
        p = int(p)
        return Product.objects.all().order_by('-price')[:p]  # Sort in descending order and retrieve the top p products
  


#not working had to ask?
    """ def get_p(self):
        p=self.request.query_params.get('p') #getting value of p from url given using query parameter
        if not p or not p.isdigit():
            raise NotFound(detail=f'enter the correct query') #checking if p not given or given is valid or not  
        else:
            p=int(p)
            return Product.objects.all().order_by('-price')[:p] #raising the request    """
    


#9 /product/not_available (request method: GET ): This route should return all the products whose inventory is zero


#In Django and Django Rest Framework, the queryset attribute is a class-level attribute used in views to specify the base set of data that should be queried when the view is accessed.
class zeroinventory(generics.ListAPIView):
    queryset=Product.objects.all()   
    serializer_class=ProdSerializer
    lookup_field='inventory'   


    def null_inventory(self):
        return  Product.objects.filter(inventory=0)
    
    def list(self, request, *args, **kwargs):
        queryset = self.null_inventory()
        if not queryset.exists():
            message = "No products with inventory equal to zero found"
            return Response({'detail': message}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    
# /product/buy (request method: Get | use query string: PID): This route should decrement the inventory of a particular product.
class buyproduct(generics.GenericAPIView):
    serializer_class=ProdSerializer


    def get(self, request):
        pid = request.query_params.get('PID')  #getting pid from url

        try:
            product = Product.objects.get(PID=pid)   #extracting product details from pid
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#raising error if product not found 

#performing action
        if product.inventory > 0:
            product.inventory -= 1
            product.save()
            return Response({'detail': f'Inventory of {product.name} (PID: {pid}) decremented by 1'})
        else:
            return Response({'detail': f'Product is out of stock'}, status=status.HTTP_404_NOT_FOUND)




class ProductDynamicUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDynamicUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            field_to_update = serializer.validated_data.get('field_to_update')
            new_value = serializer.validated_data.get('new_value')

            # Check if the field exists in the product instance
            if hasattr(instance, field_to_update):
                setattr(instance, field_to_update, new_value)
                instance.save()
                return Response({'message': f'{field_to_update} updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f'Field {field_to_update} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)