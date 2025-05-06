from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from MediaProcess.models import Profile
User = get_user_model()


@api_view(['POST'])
def Create_user(request):
    email = request.data['email']
    username = request.data['username']
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    password = request.data['password']
    if not User.objects.filter(username  = username).exists():
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )

        responce_data={
            "status_code" :5000,
            "maessage" : "user created successfully"
        }

        return Response(responce_data)
    else:
        responce_data={
            "status_code" :5001,
            "maessage" :"user already exisists"
        }

        return Response(responce_data)




@api_view(["POST"])
@permission_classes([AllowAny])  # Adjust if using token auth
def sync_user(request):
    data = request.data
    email = data.get("email")
    username = data.get("username") or data.get("id")

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(
        email=email,
        defaults={"username": username, "is_active": True}
    )

    if created:
        user = User.objects.get(email=email)
        # Automatically create a profile for the new user
        Profile.objects.create(user=user)
    else:
        # Optionally update username if user already exists
        user.username = username
        user.save()

    return Response({"message": "User synced"}, status=status.HTTP_200_OK)
