from django import forms

from devices.models import Racer, Rig


class RigUpdateForm(forms.ModelForm):
    class Meta:
        model = Rig
        fields = ['display_name', 'assigned_racer', 'current_game', 'game_detection_mode']
        widgets = {
            'display_name': forms.TextInput(attrs={'placeholder': 'Ferrari Simulator 01'}),
            'assigned_racer': forms.Select(attrs={'class': 'select'}),
            'current_game': forms.TextInput(attrs={'placeholder': 'F1 25'}),
            'game_detection_mode': forms.Select(attrs={'class': 'select'}),
        }


class RacerForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['name', 'short_name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Lohith'}),
            'short_name': forms.TextInput(attrs={'placeholder': 'LOH'}),
        }
