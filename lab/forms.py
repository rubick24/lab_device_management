from django import forms

class ApplyForm(forms.Form):
    applicant = forms.CharField(label='applicant', max_length=256)
    name = forms.CharField(label='name',max_length=256)
    device_type = forms.CharField(label='device_type', max_length=256)
    model = forms.CharField(label='model', max_length=256)
    unit_price = forms.DecimalField(label='unit_price',max_digits=10, decimal_places=1)
    count = forms.IntegerField(label='count',min_value=1)
    reason = forms.CharField(label='reason', max_length=512)
    manufacturer = forms.CharField(label='manufacturer',max_length=256)
    
class RepairForm(forms.Form):
    # device_id = forms.IntegerField(min_value=1)
    price = forms.DecimalField(label='price',max_digits=12, decimal_places=1)
    person_in_charge = forms.CharField(label='person_in_charge',max_length=256)
    repair_manufacturer = forms.CharField(label='repair_manufacturer',max_length=256)

class ScrapForm(forms.Form):
    reason = forms.CharField(label='reason',max_length=512)

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=128)
    password = forms.CharField(label='password', max_length=32)
    email = forms.EmailField(label='email')

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=128)
    password = forms.CharField(label='password', max_length=32)