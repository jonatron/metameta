import pdb

from django.core.exceptions import ValidationError
from django.db.models.fields import IntegerField
from django.forms.fields import IntegerField as FormIntegerField
from django import forms
from django.forms import ModelForm
from django.forms.models import ModelFormMetaclass

from .models import BaseCar, HondaCar, FordCar


# Zoom using cmd+= or cmd+-
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

        # this a typical client request...
        # and you can't say no because they pay you
        if cupholders % 3 == 0:
            raise ValidationError('What? No!')

        return cupholders

    class Meta:
        model = HondaCar
        fields = ['colour', 'model', 'cupholders']


# We can change the Meta fields and model dynamically

# First replicate the above inner Meta class
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


def clean_function_generator(field_name):
    def clean_field_name(self):
        field_val = self.cleaned_data[field_name]
        if field_val % 3 == 0:
            raise ValidationError('What? No!')
        return field_val

    return clean_field_name

clean_cupholders = clean_function_generator('cupholders')

# Then create a form using that
FirstCrazyForm = type(
    'FirstCrazyForm',
    (BaseCarForm, ),
    {
        'Meta': new_inner_meta,
        'clean_cupholders': clean_cupholders,
    }
)


# But how do we automatically not allow multiples of three on all integerfields?

class NotThreeMultipleIntegerField(FormIntegerField):
    def run_validators(self, value):
        if value % 3 == 0:
            raise ValidationError('U wot m8?')
        return super(NotThreeMultipleIntegerField, self).run_validators(value)


class CustomMeta(ModelFormMetaclass):
    def __new__(cls, name, parents, dct):
        # lets make a standard ModelForm, then make a new form, inheriting from it
        plain_modelform = super(CustomMeta, cls).__new__(cls, name, parents, dct)
        model_fields = plain_modelform._meta.model._meta.get_fields()
        integer_fields = [
            field for field in model_fields
            if isinstance(field, IntegerField)
        ]
        for integer_field in integer_fields:
            dct[integer_field.name] = NotThreeMultipleIntegerField(required=True)
        new_class_with_overrides = type(name, (ModelForm, ), dct)
        return new_class_with_overrides


class CustomMetaForm(ModelForm):
    __metaclass__ = CustomMeta

    class Meta:
        model = HondaCar
        fields = ['colour', 'model', 'cupholders']


# But how do we do that in a different way?


class SecondCrazyForm(ModelForm):

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
                # should've been there forever but nvm
                self.add_error(integer_field.name, 'What? No!')
                # raise ValidationError('What? No!')
        # Filter get_fields with these flags (True/False):
        # f.auto_created - reverse relations (foo_set) and generic relations
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
