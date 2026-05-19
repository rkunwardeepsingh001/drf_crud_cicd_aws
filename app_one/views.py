from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item
from .serializers import ItemSerializer

class RegisterAPI(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPI(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(): 
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']

      user = authenticate(username=username, password=password)

      if user:
    #     return Response({"message": "Login successful", "username": username})
    #   else:
    #     return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
          "message": "Login successful",
          "refresh": str(refresh),
          "access": str(refresh.access_token)
          }, status=200)
      return Response({"error": "Invalid credentials"}, status=401)
    return Response(serializer.errors, status=400)
  
  
class ItemListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]  # JWT protected

    def get(self, request):
        items = Item.objects.filter(user=request.user)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Item.objects.get(pk=pk, user=user)
        except Item.DoesNotExist:
            return None

    def get(self, request, pk):
        item = self.get_object(pk, request.user)
        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk, request.user)
        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk, request.user)
        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)