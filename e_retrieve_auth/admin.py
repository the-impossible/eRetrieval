from django.contrib import admin
from e_retrieve_auth.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(PastQuestion)
admin.site.register(Department)
