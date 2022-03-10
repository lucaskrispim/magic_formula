from django import forms
from ..models import Company

class CompanySelecaoForm(forms.Form):

  choices = Company.objects.order_by('setor').exclude(setor='nan').values_list('setor').distinct()

  setor = forms.MultipleChoiceField(choices=choices,required=True)
  quantidade = forms.IntegerField(required=True)
