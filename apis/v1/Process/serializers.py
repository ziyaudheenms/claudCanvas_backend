from rest_framework import serializers
from django.contrib.auth.models import User
from MediaProcess.models import Profile, Image ,Video
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
       

class UserViewMyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class ViewMyImageSinglePageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = "__all__"
    
    def get_user(self,instance):
        return instance.user.username
    

class ViewMyVideoSinglePageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = "__all__"
    
    def get_user(self,instance):
        return instance.user.username


class ViewUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images_manipulated = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = "__all__"
    
    def get_user(self,instance):
        return instance.user.username
    def get_images_manipulated(self,instance):
        requested_user = instance.user
        images_manipulated = Image.objects.filter(user = requested_user).count()
        return images_manipulated
    # def get_video_manipulated(self,instance):
    #     requested_user = instance.user
    #     video_manipulated = Image.objects.filter(user = requested_user).count()
    #     return video_manipulated


class UserViewMyVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
