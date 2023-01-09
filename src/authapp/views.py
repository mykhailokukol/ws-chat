from django.contrib.auth.tokens import default_token_generator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from authapp import models, serializers
from authapp.utils import Pagination


class LoginUserApi(viewsets.ModelViewSet):
    """ Authentication viewset """
    
    queryset = models.User.objects.all()
    serializer_class = serializers.LoginUserSerializer
    
    @action(['post'], detail=False)
    def post(self, request):
        """ SignIn User endpoint """
        
        serializer = serializers.LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        user = models.User.objects.filter(email=data['email'])
        if not user.exists():
            return Response({'error': 'Email or password is invalid'}, status.HTTP_400_BAD_REQUEST)
        user = user.last()
        
        if not user.is_active:
            return Response({'error': 'Your account is inactive'}, status.HTTP_400_BAD_REQUEST)
        
        check_password = user.check_password(data['password'])
        if check_password:
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status.HTTP_201_CREATED)
        return Response({'error': 'Email or password is invalid'}, status.HTTP_400_BAD_REQUEST)
    

class UserViewSet(viewsets.ModelViewSet):
    """ User signup and other viewset """
    
    queryset = models.User.objects.all()
    serializer_class = serializers.SignUpUserSerializer
    token_generator = default_token_generator
    
    def list(self, request):
        """ Returns list of all users """
        
        users = models.User.objects.all().order_by('-id')
        self.pagination_class = Pagination
        response = self.paginate_queryset(users)
        serializer = serializers.UserSerializer(response, many=True)
        return self.get_paginated_response(serializer.data)
        