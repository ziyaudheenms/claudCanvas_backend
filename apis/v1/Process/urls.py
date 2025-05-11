from django.urls import path,include
from . import views
from .views import create_checkout_session_basic_plan
urlpatterns = [
    
   path("Process/verify/",views.VerifyUser),
   path("Process/Image/bgRemove/",views.RemoveBackground),
   path("Process/Image/bgReplace/",views.GeneRativeReplace),
   path("view/myImages/",views.ViewMyImages),
   path("view/myVideos/",views.ViewMyVideos),
   path("view/myImages/<int:pk>/",views.ViewMySingleImage),
   path("view/myVideo/<int:pk>/",views.ViewMySingleVideo),
   path("view/MyProfile/",views.ViewMyProfile),
   path("Process/MakePreview/",views.VideoPreviewGenerator),
    path('create-checkout-session/basic_plan/', create_checkout_session_basic_plan),

]
