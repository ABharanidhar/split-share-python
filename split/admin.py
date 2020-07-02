from django.contrib import admin

# Register your models here.
from split.models import GroupDetail, PersonDetail, ShareDetail, ResultDetail

admin.site.register(GroupDetail),
admin.site.register(PersonDetail),
admin.site.register(ShareDetail),
admin.site.register(ResultDetail),
