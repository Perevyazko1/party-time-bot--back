from django.contrib import admin
from .models import CustomUser,PartyEvent, Advertising, UserCabinet, UserDate

admin.site.register(CustomUser)
admin.site.register(PartyEvent)
admin.site.register(Advertising)
admin.site.register(UserCabinet)
admin.site.register(UserDate)


