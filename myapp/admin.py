from django.contrib import admin
from myapp.models import  signup,watchcart,watchstock,watchsales,watchsalessub

# Register your models here.
class signupadmin(admin.ModelAdmin):
    list_display = ['id','name','email','phone','uname','pas']

class menuAdmin(admin.ModelAdmin):
    list_display = ('wname','price','qty','photo')
class cartAdmin(admin.ModelAdmin):
    list_display = ('slno','pname','rate','qty','total','userid')

class salesAdmin(admin.ModelAdmin):
    list_display = ('salesno','salesdate','userid','uname','shipment','phone','cardno','total','status')

class salessubAdmin(admin.ModelAdmin):
    list_display = ('salesno','slno','pname','rate','qty','total')

class watchstockAdmin(admin.ModelAdmin):
    list_display = ('id','wname','price','qty','photo')



admin.site.register(watchstock,watchstockAdmin)
admin.site.register(signup,signupadmin)
admin.site.register(watchcart,cartAdmin)
admin.site.register(watchsales,salesAdmin)
admin.site.register(watchsalessub,salessubAdmin)