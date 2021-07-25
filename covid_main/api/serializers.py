from api.models import User, Country
from rest_framework import serializers


# serializers class to get the serialized objects in JSON format
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'country')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'token')

        read_only_fields = ['token']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ValidateCountryAndDatetime(serializers.Serializer):
    """
      This is used here for validate request data.
    """
    country = serializers.CharField(max_length=2, required=False)
    start_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)
    end_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)
    email = serializers.BooleanField(required=False)

    def validate(self, attrs):
        # To validate the start date.
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("Start date must be before `end_date`.")
        return attrs
