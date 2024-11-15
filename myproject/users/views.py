from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Дополнительный экшн для регистрации нового пользователя
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        space1 = request.data.get('space1')
        space2 = request.data.get('space2')
        space3 = request.data.get('space3')

        if User.objects.filter(username=username).exists():
            return Response({"detail": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=username, password=password, space1=space1, space2=space2, space3=space3)
        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)

    # Дополнительный экшн для получения данных пользователя по логину
    @action(detail=False, methods=['get'])
    def get_user_data(self, request):
        username = request.query_params.get('username')
        try:
            user = User.objects.get(username=username)
            return Response({
                'username': user.username,
                'password': user.password,
                'space1': user.space1,
                'space2': user.space2,
                'space3': user.space3,
            })
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
