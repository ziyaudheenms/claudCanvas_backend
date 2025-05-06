from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer
from MediaProcess.models import Profile,Image

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from cloudinary import CloudinaryImage

cloudinary.config( 
    cloud_name = "dqakrlfun", 
    api_key = "785428453549811", 
    api_secret = "86PwAetw5I4qqTMdXssARavmiaU", # Click 'View API Keys' above to copy your API secret
    secure=True
)

@api_view(['POST'])
def VerifyUser(request):
    print(request)
    requested_user = request.data['username']
    if User.objects.filter(username = requested_user).exists():
        context={
        "request" : request
    }
        serialised_data = UserSerializer(instance = request.user,many=False,context = context  ) 
        responce_data ={
        "status_code":5000,
        "data":"User Verified",
        "message": serialised_data.data,
        
    }
        return Response(responce_data)
    else:
        responce_data ={
        "status_code":5001,
        "data":"User Not Verified"
    }
        return Response(responce_data)
    


@api_view(['POST'])
def RemoveBackground(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url = CloudinaryImage(public_id).image(effect="background_removal")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]



       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Background Removal"
        )
       
       return Response({"status_code":5000,"message":"Background Removed","data":transformed_image_url})


