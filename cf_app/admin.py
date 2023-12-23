from django.contrib import admin
from .models import User, Campaign, Contribution, Contributor

admin.site.site_header = "Crowd Funding Platform Admin"
admin.site.site_title = "Crowd Funding Platform Admin Portal"
admin.site.index_title = "Welcome to Crowd Funding Platform Admin Portal"

admin.site.register(User)
admin.site.register(Campaign)
admin.site.register(Contribution)
admin.site.register(Contributor)
