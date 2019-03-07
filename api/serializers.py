from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Resume, UserProfile



class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = ('file', 'page_count', 'created', 'updated', 'user')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        # read_only_fields = ('username', )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="api:userprofile-detail")

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
fields = '__all__'