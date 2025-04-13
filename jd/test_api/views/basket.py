from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from test_api.serializers import BasketSerializer
from rest_framework.response import Response
from rest_framework import status

from jd_auth.models import Basket
from parser.models import Product



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def basket_add_view(request):

    data = BasketSerializer(data=request.data)

    if data.is_valid():
        try: 
            basket = Basket.objects.get(user=request.user)
            product = Product.objects.get(id=data.validated_data.get("product_id"))
            basket.products.add(product)

            with open("file.txt", "w+") as file:
                file.write(f"{str(product)}, {str(basket.id)}, {str(request.user)}, {str(basket.products.all())}")

        except Exception as error: 
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response(status=status.HTTP_201_CREATED)



# @api_view(["POST"])
# def basket_add_view(request):

#     data = JSONParser().parse(request)
#     serializer = BasketSerializer(data=data)

#     if serializer.is_valid():
        
#         try:    
#             basket = Basket.objects.get(user__id=serializer.data.get("user_id"))
#             product = Product.objects.get(id=serializer.data.get("product_id"))
#             basket.products.add(product)
#             basket.save()

#         except:
#             return Response("error", status=status.HTTP_404_NOT_FOUND)


#     return Response("good", status=status.HTTP_201_CREATED)

