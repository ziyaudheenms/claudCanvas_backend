from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer,UserViewMyImagesSerializer,ViewMyImageSinglePageSerializer,ViewUserProfileSerializer,UserViewMyVideosSerializer,ViewMyVideoSinglePageSerializer
from MediaProcess.models import Profile,Image,Video
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from cloudinary import CloudinaryImage,CloudinaryVideo
import stripe
import os
import dotenv
from openai import OpenAI
stripe.api_key = os.getenv('STRIPE_SEQRET_KEY')
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


@api_view(['POST'])
def UpscaleImage(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url = CloudinaryImage(public_id).image(effect="upscale")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]

       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Upscale Image"
        )
       
       return Response({"status_code":5000,"message":"Image Upscaled to perfection","data":transformed_image_url})


@api_view(['POST'])
def ViewMyImages(request):
    requested_user_username = request.data['username']
    requested_user = User.objects.get(username = requested_user_username)
    if Image.objects.filter(user = requested_user).exists():
        images = Image.objects.filter(user = requested_user)
        context={
            "request" : request
        }
        serialised_data = UserViewMyImagesSerializer(instance = images,many=True,context = context) 
        responce_data ={
            "status_code":5000,
            "data":"User Images",
            "message": serialised_data.data,
            
        }
        return Response(responce_data)
    else:
        responce_data ={
            "status_code":5001,
            "data":"sorry,No images found",  
        }
        return Response(responce_data)
    
@api_view(['POST'])
def ViewMySingleImage(request,pk):
    reuested_user_username = request.data['username']
    requested_user = User.objects.get(username = reuested_user_username)
    if Image.objects.filter(user = requested_user).exists():
        if Image.objects.filter(pk = pk).exists():
            instance  = Image.objects.get(pk = pk)
            context={
                "request" : request
            }
            serialized_data = ViewMyImageSinglePageSerializer(instance = instance,context = context)
            responce_data ={
            "status_code":5000,
            "data":serialized_data.data,  
            }
            return Response(responce_data)
        else:
            responce_data ={
                "status_code":5001,
                "data":"sorry,No image found",  
            }
            return Response(responce_data)
    else:
        responce_data ={
            "status_code":5001,
            "data":"sorry,No images found",  
        }
        return Response(responce_data)
            
    

@api_view(['POST'])
def ViewMyProfile(request):
    requested_user_username = request.data["username"]
    requested_user = User.objects.get(username = requested_user_username)
    if Profile.objects.filter(user = requested_user).exists():
        instance = Profile.objects.get(user = requested_user)
        context={
            "request" : request
        }
        serialized_data = ViewUserProfileSerializer(instance = instance,context = context)
        responce_data ={
            "status_code":5000,
            "data":"User Profile",
            "message": serialized_data.data,
            
        }
        return Response(responce_data)
    else:
        responce_data ={
            "status_code":5001,
            "data":"sorry,No images found",  
        }
        return Response(responce_data)
    

@api_view(['POST'])
def VideoPreviewGenerator(request):
   Original_video_url = request.data['video']
   title_of_the_video = request.data['title']
   duration_of_the_video = request.data['duration']
   duration_of_the_video_in_number = int(duration_of_the_video)
   requested_user_username = request.data['username']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 4:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:


       uploaded_video = cloudinary.uploader.upload(Original_video_url, resource_type="video")
       public_id = uploaded_video['public_id']
       final_video_url = CloudinaryVideo(public_id).video(effect=f"preview:duration_{duration_of_the_video_in_number}:max_seg_3")
        

       print(final_video_url)

       soup = BeautifulSoup(final_video_url, 'html.parser')
       sources = soup.find_all('source')
       second_src_url = sources[1]['src']
       print(second_src_url)
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 4)
       


       Video.objects.create(
            user = requested_user,
            title = title_of_the_video,
            video_file = Original_video_url,
            transformed_video_file = second_src_url, 
            process_type = "Video Preview Generator"
        )
       
       return Response({"status_code":5000,"message":"Video Preview Generated","data":second_src_url})
   
@api_view(['POST'])
def ViewMyVideos(request):
    requested_user_username = request.data['username']
    requested_user = User.objects.get(username = requested_user_username)
    if Video.objects.filter(user = requested_user).exists():
        videos = Video.objects.filter(user = requested_user)
        context={
            "request" : request
        }
        serialised_data = UserViewMyVideosSerializer(instance = videos,many=True,context = context) 
        responce_data ={
            "status_code":5000,
            "data":"User videos",
            "message": serialised_data.data,
            
        }
        return Response(responce_data)
    else:
        responce_data ={
            "status_code":5001,
            "data":"sorry,No video found",  
        }
        return Response(responce_data)


@api_view(['POST'])
def ViewMySingleVideo(request,pk):

    reuested_user_username = request.data['username']
    requested_user = User.objects.get(username = reuested_user_username)
    if Video.objects.filter(user = requested_user).exists():
        if Video.objects.filter(pk = pk).exists():
            instance  = Video.objects.get(pk = pk)
            context={
                "request" : request
            }
            serialized_data = ViewMyVideoSinglePageSerializer(instance = instance,context = context)
            responce_data ={
            "status_code":5000,
            "data":serialized_data.data,  
            }
            return Response(responce_data)
        else:
            responce_data ={
                "status_code":5001,
                "data":"sorry,No video found",  
            }
            return Response(responce_data)
    else:
        responce_data ={
            "status_code":5001,
            "data":"sorry,No video found",  
        }
        return Response(responce_data)
    

@api_view(['POST'])
def GeneRativeReplace(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   from_item = request.data['itemToReplace']
   to_item = request.data['replacementItem']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url =CloudinaryImage(public_id).image(effect=f"gen_replace:from_{from_item};to_{to_item}")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Generative Replace"
        )
       
       return Response({"status_code":5000,"message":"Background Removed","data":transformed_image_url})
   

   

@api_view(['POST'])
def GenerativeRemover(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   Item_to_remove = request.data['itemToRemove']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url =CloudinaryImage(public_id).image(effect=f"gen_remove:prompt_{Item_to_remove}")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Generative Remove"
        )
       
       return Response({"status_code":5000,"message":"Generative Remove","data":transformed_image_url})
   
@api_view(['POST'])
def create_checkout_session(request):
    username = request.data['username']
    Pricetype = request.data['Pricetype']
    price_id = os.getenv('BASIC_PLAN')

    if Pricetype == 'basic':
        price_id = os.getenv('BASIC_PLAN')
    elif Pricetype == 'pro':
        price_id = os.getenv('PRO_PLAN')
    else:
        price_id = os.getenv('ALTRA_PRO_PLAN')


    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000/Success',
            cancel_url='http://localhost:3000/Failure',
            metadata={
                'username': username ,
                'priceType' : Pricetype,
            }
        )
    return Response({'sessionId': checkout_session.id})

@csrf_exempt
@api_view(['POST'])  # Accept only POST requests
@permission_classes([AllowAny])  # Allow unauthenticated access for Stripe
def stripe_webhook(request):
    webhook_secret = os.getenv('WEBHOOK_SECRET') # Replace with your real webhook secret

    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.META.get('HTTP_STRIPE_SIGNATURE'),
            webhook_secret
        )
    except Exception as e:
        return HttpResponse(status=400)

    # Handle the checkout session completion
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_name = session.get('metadata', {}).get('username')
        price_type = session.get('metadata', {}).get('priceType')

        if user_name:
            try:
                if price_type == "basic":

                    profile = Profile.objects.get(user__username=user_name)
                    profile.credits += 20
                    profile.save()
                elif price_type == "pro":
                    profile = Profile.objects.get(user__username=user_name)
                    profile.credits += 100
                    profile.save()
                else:
                    profile = Profile.objects.get(user__username=user_name)
                    profile.credits += 500
                    profile.save()
            except Profile.DoesNotExist:
                pass  # Log this if needed

    return HttpResponse(status=200)


@api_view(['POST'])
def ReplaveGenerativeBackground(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   prompt_of_image = request.data['prompt']
   requested_user_username = request.data['username']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url = CloudinaryImage(public_id).image(effect=f"gen_background_replace:prompt_&{prompt_of_image}")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)
       


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Generative replace of background"
        )
       
       return Response({"status_code":5000,"message":"Background Removed","data":transformed_image_url})



@api_view(['POST'])
def ContentAwareCrop(request):
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
   


@api_view(['POST'])
def GenerativeFill(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   Aspect_ratio_of_the_image = request.data['ratio']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url =CloudinaryImage(public_id).image(aspect_ratio=Aspect_ratio_of_the_image, gravity="center", background="gen_fill", crop="pad")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Generative Fill"
        )
       
       return Response({"status_code":5000,"message":"Generative fill applied","data":transformed_image_url})
   
@api_view(['POST'])
def ItemRecolor(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   item_of_the_image_to_recolor = request.data['ItemRecolor']
   color_to_be_used_there = request.data['color']
   
   clean_color = color_to_be_used_there[1:]
   low_case_clean_color = clean_color.lower()
   requested_user = User.objects.get(username = requested_user_username)
   print(clean_color)
   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url =CloudinaryImage(public_id).image(effect=f"gen_recolor:prompt_{item_of_the_image_to_recolor};to-color_{clean_color};multiple_true")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Generative Recolor"
        )
       
       return Response({"status_code":5000,"message":"Generative Recolor applied","data":transformed_image_url})
   

   
@api_view(['POST'])
def GenerativeImageCrop(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   height_and_width_of_the_image = request.data['ratio']
   height,width = height_and_width_of_the_image.split(":")
   requested_user = User.objects.get(username = requested_user_username)
   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url = CloudinaryImage(public_id).image(gravity="auto", height=height, width=width, crop="fill")

       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Content Aware Crop"
        )
       
       return Response({"status_code":5000,"message":"croped image successfully","data":transformed_image_url})
   

   
@api_view(['POST'])
def OptimizeImage(request):
   Original_image_url = request.data['image']
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   width_of_the_image = request.data['ratio']
   quality_of_the_image = request.data['quality']

   if quality_of_the_image == "35":
       quality_of_the_image = 35
   elif quality_of_the_image == "auto":
       quality_of_the_image = "auto"
   else:
       quality_of_the_image = "auto:best"

   width_of_the_image_in_numer = int(width_of_the_image)
   requested_user = User.objects.get(username = requested_user_username)
   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 2:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
       


       uploaded_image = cloudinary.uploader.upload(Original_image_url)
       public_id = uploaded_image['public_id']
       final_iamge_url = CloudinaryImage(public_id).image(transformation=[
            {'width': width_of_the_image_in_numer, 'crop': "scale"},
            {'quality': quality_of_the_image},
            {'fetch_format': "auto"}
        ])
       start_pos = final_iamge_url.find('src="') + len('src="')
       end_pos = final_iamge_url.find('"', start_pos)
       transformed_image_url = final_iamge_url[start_pos:end_pos]
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 2)


       Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = Original_image_url,
            processed_image = transformed_image_url, 
            process_type = "Image Optimization"
        )
       
       return Response({"status_code":5000,"message":"Image optimized successfully","data":transformed_image_url})
   
@api_view(['POST'])
def VideoOptimizer(request):
   Original_video_url = request.data['video']
   title_of_the_video = request.data['title']
   width_of_the_video = request.data['ratio']
   quality_of_the_video = request.data['quality']  
   width_of_the_video_number = int(width_of_the_video)
   requested_user_username = request.data['username']
   requested_user = User.objects.get(username = requested_user_username)


   if quality_of_the_video == "35":
       quality_of_the_video = 35
   elif quality_of_the_video == "auto":
       quality_of_the_video = "auto"
   else:
       quality_of_the_video = "auto:best"

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 4:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:


       uploaded_video = cloudinary.uploader.upload(Original_video_url, resource_type="video")
       public_id = uploaded_video['public_id']
       final_video_url = CloudinaryVideo(public_id).video(transformation=[
           {'width': width_of_the_video_number, 'crop': "scale"},
           {'quality': quality_of_the_video},
           {'fetch_format': "auto"}
       ])

       print(final_video_url)

       soup = BeautifulSoup(final_video_url, 'html.parser')
       sources = soup.find_all('source')
       second_src_url = sources[1]['src']
       print(second_src_url)
       Profile.objects.filter(user = requested_user).update(credits = Available_credits - 4)
       


       Video.objects.create(
            user = requested_user,
            title = title_of_the_video,
            video_file = Original_video_url,
            transformed_video_file = second_src_url, 
            process_type = "Video Optimizer"
        )
       
       return Response({"status_code":5000,"message":"Video Optimized Successfully","data":second_src_url})
   


@api_view(['POST'])
def GenerateImage(request):
   title_of_the_image = request.data['title']
   requested_user_username = request.data['username']
   prompt_of_the_image = request.data['prompt']
   requested_user = User.objects.get(username = requested_user_username)

   Available_credits = Profile.objects.get(user = requested_user).credits
   if Available_credits <= 6:
       return Response({"status_code": 5002, "message": "Insufficient credits"})
   else:
        client = OpenAI(
            base_url="https://api.studio.nebius.com/v1/",
            api_key=os.getenv("NEBIUS_API_KEY")
        )
        response = client.images.generate(
            model="black-forest-labs/flux-dev",
            response_format="url",
            extra_body={
                "response_extension": "png",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 28,
                "negative_prompt": "",
                "seed": -1
            },
            prompt=prompt_of_the_image
        )
        print(response.data[0].url)
       
        Profile.objects.filter(user = requested_user).update(credits = Available_credits - 6)
        Image.objects.create(
            user = requested_user,
            title = title_of_the_image,
            image_file = 'https://th.bing.com/th/id/OIP.kf23wlD2Crw8b424CqnfhAHaDq?w=349&h=172&c=7&r=0&o=7&cb=iwp2&dpr=1.3&pid=1.7&rm=3',
            processed_image = response.data[0].url, 
            process_type = "Image Generation"
        )
       
        return Response({"status_code":5000,"message":"Generated Image","data":response.data[0].url})


@api_view(['POST'])
def DeleteImage(request,pk):
    requested_user_username = request.data['username']
    requested_user = User.objects.get(username = requested_user_username)
    if Image.objects.filter(user=requested_user).exists():
        if Image.objects.filter(pk=pk).exists():
         # Delete the image from Cloudinary
            image_instance = Image.objects.get(pk=pk)
            image_instance.delete()
        
            return Response({"status_code": 5000, "message": "Image deleted successfully"})
        else:
            return Response({"status_code": 5001, "message": "Image not got deleted"})
    else:
         return Response({"status_code": 5001, "message": "User not found"})
    
@api_view(['POST'])
def DeleteVideo(request,pk):
     
     requested_user_username = request.data['username']
     requested_user = User.objects.get(username = requested_user_username)
     if Video.objects.filter(user=requested_user).exists():
        
        if Video.objects.filter(pk=pk).exists():
         # Delete the video from Cloudinary
            video_instance = Video.objects.get(pk=pk)
            video_instance.delete()

            return Response({"status_code": 5000, "message": "Video deleted successfully"})
        else:
            
            return Response({"status_code": 5001, "message": "Video not got deleted"})
     else:
         return Response({"status_code": 5001, "message": "User not found"})