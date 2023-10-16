#serializers file
"""Serializers in DRF are used to convert complex data types (such as Django model instances) into Python data types 
that can be easily rendered into JSON, XML, or other content types for APIs. Serializers also provide deserialization, allowing parsed 
data to be converted back into complex types after first validating the incoming data."""
from rest_framework import serializers
from .models import Product
from rest_framework.exceptions import ValidationError

class ProdSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class partialupdateserializer(serializers.Serializer):
    field_to_update=serializers.DictField(child=serializers.CharField())        

#delete particular record
class deleteparticular(serializers.Serializer):
        name=serializers.CharField(max_length=100)

class ProductDynamicUpdateSerializer(serializers.Serializer):
    field_to_update = serializers.CharField()
    new_value = serializers.CharField()