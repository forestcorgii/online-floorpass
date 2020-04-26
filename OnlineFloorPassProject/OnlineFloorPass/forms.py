from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class LogForm(forms.Form):
    employee_id = forms.CharField(
        label='Employee ID', max_length=4, widget=forms.TextInput)
