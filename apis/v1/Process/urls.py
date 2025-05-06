from django.urls import path,include
from . import views
urlpatterns = [
    
   path("Process/verify/",views.VerifyUser),
   path("Process/Image/bgRemove/",views.RemoveBackground),

]
