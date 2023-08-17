from rest_framework import serializers
from .models import Poll



class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['email', 'question', 'first_choice', 'second_choice', 'third_choice', 'verification_code_expires']