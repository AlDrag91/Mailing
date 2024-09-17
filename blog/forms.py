from django import forms
from blog.models import Blog
from users.forms import FormMixin


class BlogForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'picture', 'is_published')


