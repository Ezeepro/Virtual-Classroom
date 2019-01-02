from django.contrib import admin
from .models import CoursePack, Podcast, Video, Pdf
# Register your models here.

admin.site.register(CoursePack)
admin.site.register(Podcast)
admin.site.register(Video)
admin.site.register(Pdf)