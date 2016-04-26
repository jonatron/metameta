from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import BaseCar, HondaCar, FordCar


class BaseCarForm(ModelForm):

    def clean_colour(self):
        colour = self.cleaned_data['colour']
        if colour.lower() == 'yellow':
            raise ValidationError('Yellow Car!')
        return colour

    class Meta:
        model = BaseCar
        fields = ['colour', 'model']
