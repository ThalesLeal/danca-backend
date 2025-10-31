from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Usuários normais só veem seu próprio perfil
        if self.request.user.is_superuser or self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


@api_view(['POST'])
def register(request):
    """Endpoint para registrar novo usuário"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """Retorna os dados do usuário logado"""
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Altera a senha do usuário logado"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.data['old_password']):
            return Response({'error': 'Senha atual incorreta'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response({'message': 'Senha alterada com sucesso'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Atualiza o perfil do usuário logado"""
    serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
