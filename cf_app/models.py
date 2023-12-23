from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Additional fields for user registration and login
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    phone_num = models.CharField(max_length=12, blank=True)
    CNIC = models.CharField(max_length=13, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)


class Contributor(models.Model):
    name = models.CharField(max_length=255, blank=True)
    wallet_address = models.CharField(max_length=42)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    funding_goal = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    contributors = models.ManyToManyField(Contributor, through='Contribution', related_name='contributed_campaigns')

    def __str__(self):
        return self.title

    @property
    def total_contributions(self):
        return self.contributions.aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def is_fully_funded(self):
        return self.total_contributions >= self.funding_goal

class Contribution(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor.name} contributed {self.amount} to {self.campaign.title}"

class Token(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    token_price = models.DecimalField(max_digits=10, decimal_places=2)
    token_address = models.CharField(max_length=42)  # Ethereum address where the tokens will be stored

    def __str__(self):
        return f"{self.campaign.title} - Token"
