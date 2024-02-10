from django import forms
from webapp.models import Announcements, Comment


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = ('title', 'image', 'description', 'category', 'amount', 'status')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


