from django.contrib import admin
from kitaplar.models import Kitap, Yorum
# Register your models here.

admin.site.register(Kitap)
admin.site.register(Yorum)
