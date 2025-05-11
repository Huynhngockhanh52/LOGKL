from django.contrib import admin
from .models import Dataset, LogConfig, RegexPattern, SizeLog

# Register your models here.
admin.site.register(Dataset)
admin.site.register(LogConfig)
admin.site.register(RegexPattern)
admin.site.register(SizeLog)