from django import forms
from .models import CustomUser, Thread, Post


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'country', 'birthday', 'occupation', 'mobile_phone']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
