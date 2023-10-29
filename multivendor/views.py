from .serializers import UserSerializer
from .models import USER
from .permissons import UserPermission
from rest_framework import viewsets, filters, status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings


# Create your views here.
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'is_seller': user.is_seller,
            })
        else:
            return Response({"Response": "username or password was incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


class UserGeneric_list(generics.ListCreateAPIView):  # list only API
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class UserSellerViewSet(viewsets.ModelViewSet):
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('id', 'username', 'email', 'is_active', 'is_seller')
    search_fields = ['username', 'email', 'is_active', 'is_seller', ]

    # lockup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.get(user=serializer.instance).key
        return Response({"Response": serializer.data, "token": token}, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = USER.objects.filter(is_seller=True)
        return queryset

    def retrieve(self, request, pk=None):
        queryset = USER.objects.filter(is_seller=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = USER.objects.filter(is_seller=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = USER.objects.filter(is_seller=True)
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response({"Response": "user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserBuyerViewSet(viewsets.ModelViewSet):
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'username', 'email', 'is_active', 'is_seller', ]
    search_fields = ['username', 'email', 'is_active', 'is_seller', ]
    lockup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.get(user=serializer.instance).key
        return Response({"Response": serializer.data, "token": token}, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_superuser:
            queryset = USER.objects.filter(is_seller=False)
        return queryset

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response({"Response": "user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
