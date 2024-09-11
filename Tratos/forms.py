from django.forms import ModelForm
from .models import Trato

class TratoForm(ModelForm):
    class Meta:
        model = Trato
        fields = ['cod','partida','valor']
        
