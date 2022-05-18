from django.shortcuts import render,redirect
from ..controllers.company_controller import getCompany,storeAllCompanies
from ..forms import CompanySelecaoForm
from ..utils import indicators

# Create your views here.
def index(request):
  if request.method == 'GET':
    companies,sectors = getCompany()

    companies = indicators(companies)

    context = {
      'sectors': sectors,
      'companies': companies
    }

    return render(request, 'index.html',context)

  elif request.method == 'POST':

    form = CompanySelecaoForm(request.POST)
    setor = form.data['setor']
    quantidade = form.data['quantidade']

    if setor and quantidade:
      companies,sectors = getCompany(setor,int(quantidade))
    elif form.data['setor']:
      companies,sectors = getCompany(setor)
    else:
      companies,sectors = getCompany()
      
    companies = indicators(companies)
    
    context = {
      'sectors': sectors,
      'companies': companies
    }

    return render(request, 'index.html',context)


def refreshcompanies(request):
  
  response = storeAllCompanies()

  return redirect('index')



# def create(request):

#   if request.method == 'GET':
#     form = UserForm()

#     context = {
#       'form': form,
#     }

#     return render(request, 'criar.html',context=context)
#   else:
#     form = UserForm(request.POST)
#     if form.is_valid():
#       form.save()
#       return redirect(index)
