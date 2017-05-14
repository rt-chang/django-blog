from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('author', 'text',)


class ContactForm(forms.Form):
	contact_name = forms.CharField(required=True, label='Your Name')
	contact_email = forms.EmailField(required=True, label='Your Email')
	subject = forms.CharField(max_length=100)
	message = forms.CharField(required=True, widget=forms.Textarea)
