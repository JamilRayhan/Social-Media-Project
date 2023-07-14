from django import forms

class MessageSendForm(forms.Form):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 1,  # Adjust the number of rows as needed
            'cols': 35,  # Adjust the number of columns as needed
            'placeholder': 'Enter your message...',
            'class': 'form-control'  # Add any additional CSS classes for styling
        })
    )

class MessageReplyForm(forms.Form):
    content = forms.CharField(
        label='Send Message',
        widget=forms.Textarea(attrs={
            'rows': 1,  # Adjust the number of rows as needed
            'cols': 35,  # Adjust the number of columns as needed
            'placeholder': 'Enter your message...',
            'class': 'form-control'  # Add any additional CSS classes for styling
        })
    )
