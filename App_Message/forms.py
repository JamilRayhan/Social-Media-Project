from django import forms

class MessageSendForm(forms.Form):
    content = forms.CharField(label='Message', widget=forms.Textarea)

class MessageReplyForm(forms.Form):
    content = forms.CharField(label='Reply', widget=forms.Textarea)
