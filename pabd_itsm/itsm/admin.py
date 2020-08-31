from django.contrib import admin

# Register your models here.
from .models import ITSM_User, AssetStatus, Asset_type,Gender,User_type,Field_type,Name,Priority,Business_unit,Status,Classification,Sr_pattern,Pattern_row,Asset,Service_request,Work_journal,Communication_journal
#Person

admin.site.register(Asset_type)
admin.site.register(AssetStatus)
admin.site.register(Gender)
admin.site.register(User_type)
admin.site.register(Field_type)
admin.site.register(Name)
admin.site.register(Priority)
admin.site.register(Business_unit)
admin.site.register(Status)
admin.site.register(Classification)
admin.site.register(Sr_pattern)
admin.site.register(Pattern_row)
#admin.site.register(Person)
admin.site.register(Asset)
admin.site.register(Service_request)
admin.site.register(Work_journal)
admin.site.register(Communication_journal)
admin.site.register(ITSM_User)
