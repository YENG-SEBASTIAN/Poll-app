from django.db import models
import string
import random


class Poll(models.Model):
    email = models.EmailField(unique=True)
    question = models.TextField()
    first_choice = models.CharField(max_length=30)
    second_choice = models.CharField(max_length=30)
    third_choice = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    isOpen = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_expires = models.DateTimeField(blank=True, null=True)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

    def generate_verification_code(self):
        chars = string.digits
        return ''.join(random.choices(chars, k=6))
    
    def __str__(self):
        return self.email