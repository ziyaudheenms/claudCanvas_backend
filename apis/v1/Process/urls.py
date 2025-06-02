from django.urls import path,include
from . import views
from .views import create_checkout_session,stripe_webhook
urlpatterns = [
    
   path("Process/verify/",views.VerifyUser),
   path("Process/Image/bgRemove/",views.RemoveBackground),
   path("Process/Image/bgRemove/",views.RemoveBackground),
   path("Process/Image/Upscale/",views.UpscaleImage),
   path("Process/Image/GenerativeFill/",views.GenerativeFill),
   path("Process/Image/CotentAwareCrop/",views.GenerativeImageCrop),
   path("Process/Image/OptimizeImage/",views.OptimizeImage),
   path("Process/Image/GenerativeRecolor/",views.ItemRecolor),
   path("Process/Image/bgGenerativeChange/",views.ReplaveGenerativeBackground),
   path("Process/Image/bgReplace/",views.GeneRativeReplace),
   path("Process/Image/GenerativeRemove/",views.GenerativeRemover),
   path("view/myImages/",views.ViewMyImages),
   path("view/myVideos/",views.ViewMyVideos),
   path("view/myImages/<int:pk>/",views.ViewMySingleImage),
   path("view/myVideo/<int:pk>/",views.ViewMySingleVideo),
   path("view/MyProfile/",views.ViewMyProfile),
   path("Process/MakePreview/",views.VideoPreviewGenerator),
   path("Process/OptimizeVideo/",views.VideoOptimizer),
   path('create-checkout-session/basic_plan/', create_checkout_session),
   path('webhooks/stripe/', stripe_webhook),
   path('Process/Image/ContentAwareCrop/', views.ContentAwareCrop),
   path('Process/Image/GenerateImage/', views.GenerateImage),
   path('Process/Image/delete/', views.DeleteImage),
   path('Process/Video/delete/', views.DeleteVideo),

]
