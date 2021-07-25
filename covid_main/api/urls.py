from django.urls import path, include
from .views import CountryListAPI, CovidDataAPI, RegisterAPIView, LoginAPIView, AuthUserAPIView, \
    UserSearchFilterAPIView, UpdateUserAPIView

# all url routes

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('user/', AuthUserAPIView.as_view(), name="user"),
    path('filter/', UserSearchFilterAPIView.as_view(), name="user-filter"),
    path('users/update/<int:pk>', UpdateUserAPIView.as_view(), name="update"),
    path('country_list/', CountryListAPI.as_view()),
    path('covid_api/', CovidDataAPI.as_view()),
]
