from django import forms
from django.contrib.auth.models import User

from .models import CoursePack, Podcast, Video, Pdf, Evaluation 


class CoursePackForm(forms.ModelForm):

    class Meta:
        model = CoursePack
        fields = ['instructor', 'course_title', 'course_code', 'thumbnail']



class PodcastForm(forms.ModelForm):

    class Meta:
        model = Podcast
        fields = ['material_title', 'material_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EvaluationForm(forms.Form):
        post = forms.CharField()

