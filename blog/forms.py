from django import forms
from django.db.models import TextField, fields 
from .models import Blog 

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=200)
    e_from = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())
