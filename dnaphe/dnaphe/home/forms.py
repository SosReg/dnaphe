from django import forms
from pagedown.widgets import PagedownWidget

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)


class LinkPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('topic', 'language', 'title', 'url')


class TextPostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Post
        fields = ['topic', 'language', 'title', 'content']


class PostUpdateForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Post
        fields = ['topic', 'language', 'title',  'content', 'url']