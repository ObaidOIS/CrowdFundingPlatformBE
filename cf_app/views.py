from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.urls import reverse




@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list'),
        'campaigns': reverse('campaign-list'),
        'register': reverse('register'),
        'login ': reverse('token_obtain_pair'),
    })

User = get_user_model()

@api_view(['POST'])
def register(request):
    """
    API endpoint for user registration.
    """
    print(request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    print(serializer)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "User created successfully",
            "data": serializer.data
        })
    print(serializer.errors)
    return Response({
        "status": "error",
        "message": serializer.errors
        
    })

@api_view(["POST"])
def blacklistToken(request):
    print(request.data)
    try:
        refresh_token = request.data["refresh"]
        print(refresh_token)
        # blacklist_token(refresh_token)
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        print(e)
        return Response(status=400, data={"message": "Invalid token"})
    return Response(status=200, data={"message": "Logout successful"})



class UserList(generics.ListAPIView):
    """
    API endpoint to list all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     """
#     API endpoint to retrieve user details.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class CampaignList(generics.ListCreateAPIView):
    """
    API endpoint to list all campaigns or create a new campaign.
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     API endpoint to retrieve, update, or delete a campaign.
#     """
#     queryset = Campaign.objects.all()
#     serializer_class = CampaignSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class ContributionList(generics.ListCreateAPIView):
#     """
#     API endpoint to list all contributions or create a new contribution.
#     """
#     queryset = Contribution.objects.all()
#     serializer_class = ContributionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         campaign = get_object_or_404(Campaign, pk=self.kwargs.get('campaign_pk'))
#         serializer.save(contributor=self.request.user.contributor, campaign=campaign)

# class ContributionDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     API endpoint to retrieve, update, or delete a contribution.
#     """
#     queryset = Contribution.objects.all()
#     serializer_class = ContributionSerializer
#     permission_classes = [permissions.IsAuthenticated]
