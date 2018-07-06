from django import forms
from .models import CandidateModel, InterviewerModel, QueryRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget


class QueryForm(forms.ModelForm):
    
    class Meta:
        model = QueryRequest
        fields = ('query_type', 'candidate', 'interviewer')
        labels = {
        'query_type': 'Query type',
        'candidate': 'Candidate email',
        'interviewer': 'Interviewer'
        }

class CandidateForm(forms.Form):
    # these fields should be added to the HTML page
    # dynamically which is very easier with a Js-based
    # framework. Otherwise the add_field button should
    # reload the template with more fields_number
    from_date = forms.DateField(widget=AdminDateWidget())
    to_date = forms.DateField(widget=AdminDateWidget())


class InterviewerForm(forms.Form):
    from_date = forms.DateField(widget=AdminDateWidget())
    to_date = forms.DateField(widget=AdminDateWidget())

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user