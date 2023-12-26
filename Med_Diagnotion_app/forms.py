from django import forms
from .models import CustomUser


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'country', 'birthday', 'occupation', 'mobile_phone']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Add any additional customizations if needed
