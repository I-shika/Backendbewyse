from django.urls import path
from .views import Signin, ViewProfile, Register, EditProfile

urlpatterns = [
    path('register/', Register),
    path('login/', Signin),
    path('profile/view',ViewProfile),
    path('profile/edit',EditProfile),

    
]