import requests

from django.conf import settings
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import response, status, permissions, generics, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions

from api.serializers import RegisterSerializer, LoginSerializer, CountrySerializer, \
    ValidateCountryAndDatetime
from api.models import User, Country
from api.tasks import email_image
from utils import get_data_with_date_range


class AuthUserAPIView(GenericAPIView):
    """
    This API is to authenticate the user to get his registration/profile details
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):
    """
    This is the view created for the registration of user with exclusion of authentication
    Note: username and email id must be unique
    """
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    """
    Login view is created so that user can login with email and password
    after login with correct credentials user will get his details with covid_app token
    """
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(email=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, Try again"}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUserAPIView(generics.UpdateAPIView):
    """
    This API will enable the registered user to change his details with valid covid_app token
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "user updated successfully", 'user': serializer.data})

            else:
                return Response({"message": "failed", "details": serializer.errors})
        else:
            raise exceptions.AuthenticationFailed('Invalid Token or user id')


class UserSearchFilterAPIView(generics.ListCreateAPIView):
    """
    This API will be used by Admin user to search the details of users
    Right now filter fields are email and username
    you can search by any word
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']


class CountryListAPI(ListAPIView):
    """
        This API is used to list all countries
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CovidDataAPI(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ValidateCountryAndDatetime

    def post(self, request, *args, **kwargs):
        try:
            params = {'include': 'timeline'}
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            email = request.data.get('email')
            country = request.data.get('country')
            param_validation = ValidateCountryAndDatetime(data=request.data)
            param_validation.is_valid(raise_exception=True)
            if country:
                url = settings.COVID_API_BASE_URL.format("/countries/{0}".format(country))
            else:
                url = settings.COVID_API_BASE_URL.format("/countries/{0}".format(request.user.country.code))
            response = requests.get(url, params=params)

            response_json = response.json()
            if not response.ok:
                return Response({"message": "error in API calling."}, status=status.HTTP_400_BAD_REQUEST)
            date_filtered_timeline = get_data_with_date_range(start_date, end_date,
                                                              response_json.get('data').get('timeline'))
            response_json['data']['timeline'] = date_filtered_timeline
            if email:
                email_image(date_filtered_timeline, request.user.email, request.user.username)

            return Response(response_json, status=status.HTTP_200_OK)
        except Country.DoesNotExist:
            return Response({"message": "Country details not found."}, status=status.HTTP_404_NOT_FOUND)
        except APIException as e:
            raise e
        except Exception:
            return Response({"message": "Unknown Server error. "}, status=status.HTTP_400_BAD_REQUEST)