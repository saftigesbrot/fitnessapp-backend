from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user_id = request.query_params.get('id')
    if not user_id:
        return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
