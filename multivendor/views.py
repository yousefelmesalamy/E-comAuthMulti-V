from django.shortcuts import render
from .serializers import UserSerializer
from .models import USER
from .permissons import UserPermission

from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# import generic class
from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import action


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


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = USER.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [UserPermission]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     # pagination_class = StandardResultsSetPagination
#     filterset_fields = ['id', 'username', 'email', 'is_active', 'is_seller', ]
#
#     search_fields = ['username', 'email', 'is_active', 'is_seller', ]
#
#     lockup_field = 'id'
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         headers = self.get_success_headers(serializer.data)
#         token = Token.objects.get(user=serializer.instance).key
#         return Response({"Response": serializer.data, "token": token}, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()
#
#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}
#
#     def update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return super().update(request, *args, **kwargs)


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
    # pagination_class = StandardResultsSetPagination
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

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = USER.objects.filter(is_seller=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

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
    # pagination_class = StandardResultsSetPagination
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

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = USER.objects.filter(is_seller=False)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = USER.objects.filter(is_seller=False)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = USER.objects.filter(is_seller=False)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = USER.objects.filter(is_seller=False)
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response({"Response": "user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
