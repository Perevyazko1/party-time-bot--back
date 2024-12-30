from django.contrib import admin
from .models import CustomUser,PartyEvent, Advertising

admin.site.register(CustomUser)
admin.site.register(PartyEvent)
admin.site.register(Advertising)


