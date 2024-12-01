from django.contrib import admin
from .models import CustomUser,DateEvent,PartyEvent, Advertising

admin.site.register(CustomUser)
admin.site.register(DateEvent)
admin.site.register(PartyEvent)
admin.site.register(Advertising)


