from django.forms import ModelForm
from .models import Poll

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['email', 'question', 'first_choice', 'second_choice', 'third_choice']
