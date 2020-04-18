from django import forms
from .models import OrderModel


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['fullname'].required = True
        self.fields['mobile'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = False
        self.fields['zip'].required = False

    class Meta:
        model = OrderModel
        fields = {
            'fullname', 'mobile', 'email', 'address', 'city', 'state', 'zip'
        }
