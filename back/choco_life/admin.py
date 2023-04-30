from django.contrib import admin
from choco_life.models import EventCategory, Company, Event, Certificate, UserCertificate

# Register your models here.

admin.site.register(EventCategory)
admin.site.register(Company)
admin.site.register(Event)
admin.site.register(Certificate)
admin.site.register(UserCertificate)