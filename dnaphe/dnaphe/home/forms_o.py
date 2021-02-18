
from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_text',)


class LinkPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('topic', 'language', 'title', 'url')
