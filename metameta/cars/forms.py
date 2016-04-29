from django.core.exceptions import ValidationError
from django.db.models.fields import IntegerField
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


# How do we automatically create this form?
class HondaForm(BaseCarForm):

    def clean_cupholders(self):
        cupholders = self.cleaned_data['cupholders']

        if cupholders % 3 == 0:
            raise ValidationError('What? No!')

        return cupholders

    class Meta:
        model = HondaCar
        fields = ['colour', 'model', 'cupholders']


# We can change the Meta fields and model dynamically

parent_inner_meta = BaseCarForm.Meta
inner_meta_attrs = {
    'model': HondaCar,
    'fields': parent_inner_meta.fields + ['cupholders']
}
new_inner_meta = type(
    'Meta',
    (parent_inner_meta, object),
    inner_meta_attrs
)

FirstCrazyForm = type(
    'FirstCrazyForm',
    (BaseCarForm, ),
    {
        'Meta': new_inner_meta
    }
)


# But how do we automatically not allow multiples of three on all integerfields?


class SecondCrazyForm(ModelForm):

    # you can dynamically create clean_{field} methods
    # but in python it's hacky to find out the name of the current function
    def clean(self, *args, **kwargs):
        cleaned_data = super(SecondCrazyForm, self).clean(*args, **kwargs)

        # import pdb; pdb.set_trace()
        # self._meta = <django.forms.models.ModelFormOptions object>
        model = self._meta.model
        # model._meta = <Options for HondaCar>
        fields = model._meta.get_fields()
        integer_fields = [
            field for field in fields
            if isinstance(field, IntegerField)
        ]
        for integer_field in integer_fields:
            clean_value = cleaned_data.get(integer_field.name)
            if clean_value and clean_value % 3 == 0:
                # add_error added in 1.7 :)
                self.add_error(integer_field.name, 'What? No!')
                # raise ValidationError('What? No!')
        # Filter get_fields with these flags (True/False):
        # f.auto_created - reverse relations and generic relations
        # f.concrete - basically not relationships eg CharField, IntegerField etc
        # f.is_relation
        # f.one_to_one
        # f.many_to_one
        # f.one_to_many
        # Something to note - if you have a custom M2M 'through' table, you get
        # the relationships to that on both models

        return cleaned_data

    class Meta:
        model = HondaCar
        fields = ['colour', 'model', 'cupholders']

# further metaclass reading:
# https://github.com/django/django/blob/c339a5a6f72690cd90d5a653dc108fbb60274a20/django/db/models/base.py#L67

# Exercise for reader:
# Create a form factory that does something crazy
