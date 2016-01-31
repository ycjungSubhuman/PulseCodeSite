from django.contrib import admin
from posting.models import Post, Track, Journal, Creator, Member, Team, Tag
import os

class TrackAdmin(admin.ModelAdmin):
	# add 'audio_file_player' tag to your admin view
	list_display = ('title', 'audio_file_player')
	actions = ['custom_delete_selected',]


	def custom_delete_selected(self, request, queryset):
		#custom delete code
		n = queryset.count()
		for i in queryset:
			if i.audio_file:
				if os.path.exists(i.audio_file.path):
					os.remove(i.audio_file.path)
				i.delete()
		self.message_user(request, ("Successfully deleted %d audio files.") % n)
	custom_delete_selected.short_description = "Delete selected items"

	def get_actions(self, request):
		actions = super(TrackAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions
 
# Register your models here.
admin.site.register(Post)
admin.site.register(Track, TrackAdmin)
admin.site.register(Journal)
admin.site.register(Creator)
admin.site.register(Member)
admin.site.register(Team)
admin.site.register(Tag)
   