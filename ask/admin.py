from django.contrib import admin
from .models import Profile, Tag, UniversalQuestion, UniversalQuestionLike

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(UniversalQuestion)
admin.site.register(UniversalQuestionLike)

# Register your models here.
