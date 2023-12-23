from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import register

urlpatterns = [
    path('', api_root),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/logout/", blacklistToken, name="Logout"),
    path('api/register/', register, name='register'),
    path('users/', UserList.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('campaigns/', CampaignList.as_view(), name='campaign-list'),
    # path('campaigns/<int:pk>/', CampaignDetail.as_view(), name='campaign-detail'),
    # path('campaigns/<int:campaign_pk>/contributions/', ContributionList.as_view(), name='contribution-list'),
    # path('campaigns/<int:campaign_pk>/contributions/<int:pk>/', ContributionDetail.as_view(), name='contribution-detail'),
]
