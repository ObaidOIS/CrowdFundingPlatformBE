from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'phone_num', 'CNIC', 'bio', 'location', 'profile_picture']

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, validators=[validate_password])

#     class Meta:
#         model = User
#         fields = ['username', 'password', 'name', 'email', 'phone_num', 'CNIC', 'bio', 'location', 'profile_picture']
#         # extra_kwargs = {
#         #     'name': {'required': True},
#         #     'email': {'required': True},
#         # }

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'phone_num', 'CNIC', 'profile_picture']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'name', 'wallet_address']

class CampaignSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True)
    contributors_count = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'funding_goal', 'owner', 'contributors', 'contributors_count']
        read_only_fields = ['start_date']

    def get_contributors_count(self, obj):
        return obj.contributors.count()

class ContributionSerializer(serializers.ModelSerializer):
    contributor = ContributorSerializer(read_only=True)

    class Meta:
        model = Contribution
        fields = ['id', 'campaign', 'contributor', 'amount', 'timestamp']
        read_only_fields = ['timestamp']
