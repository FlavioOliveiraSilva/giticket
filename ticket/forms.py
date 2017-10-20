from django import forms
from .models import TicketRequest


class TicketForm(forms.ModelForm):

    class Meta:
        model = TicketRequest
        fields = ('title', 'application', 'type', 'description',)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'titleclass'})
        self.fields['title'].label = "Name of your ticket/request"
        self.fields['application'].widget.attrs.update({'class': 'applicationclass'})
        self.fields['type'].widget.attrs.update({'class': 'typerequestclass'})
        self.fields['type'].label = "Category of this request"
        self.fields['description'].widget.attrs.update({'class': 'ticketdescriptionclass'})




