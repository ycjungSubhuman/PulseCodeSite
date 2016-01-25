from django.contrib import admin
from posting.models import Post, Track, Journal, Creator, Member, Team, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Track)
admin.site.register(Journal)
admin.site.register(Creator)
admin.site.register(Member)
admin.site.register(Team)
admin.site.register(Tag)
