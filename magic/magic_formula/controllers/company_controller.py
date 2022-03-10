import requests
import pandas as pd
from ..utils.company import setor
from ..models import Company

def getCompany(setor="zero",n=10):
  try:
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get('https://fundamentus.com.br/resultado.php', headers=agent)
  except Exception as e:
    return False

  df = pd.read_html(res.content)[0]

  for coluna in list(df):
    if coluna != 'Papel':
      df[coluna] = df[coluna].astype(str).str.replace('.','')
      df[coluna] = df[coluna].astype(str).str.replace(',','.')
      df[coluna] = df[coluna].astype(str).str.rstrip('%').astype('float')/100

  df.drop(df[df['Liq.2meses'] < 1.0e6].index, inplace = True)
  df.drop(df[df['EV/EBIT']<=0].index, inplace = True)
  
  ranking = pd.DataFrame()
  ranking['pos'] = range(1,len(df))
  ranking['EV/EBIT'] = df.sort_values(by=['EV/EBIT'])['Papel'][:len(df)-1].values 
  ranking['ROIC'] = df.sort_values(by=['ROIC'],ascending=False)['Papel'][:len(df)-1].values

  a = ranking.pivot_table(columns='EV/EBIT',values='pos')
  b = ranking.pivot_table(columns='ROIC',values='pos')

  t = pd.concat([a,b])
  rank = t.dropna(axis=1).sum().sort_values().reset_index()

  rank.columns = ['sigla', 'posicao']

  ev = []

  roic = []

  nome = []

  s = []

  for index, row in rank.iterrows():
    ev.append( df[df['Papel'] == row['sigla']]['EV/EBIT'].values[0] )
    roic.append( str(round(df[df['Papel'] == row['sigla']]['ROIC'].values[0]*100.0,2))+"%" )
    
    company = Company.objects.get(sigla=row['sigla'])
    nome.append(company.nome)
    s.append(company.setor)

  rank['setor'] = s

  rank['nome'] = nome

  rank['ev'] = ev

  rank['roic'] = roic

  if setor != "zero": 
    
    rank = rank[rank['setor']==setor]

    rank = rank.iloc[:n,:]

    return rank.to_dict('records'), Company.objects.order_by('setor').exclude(setor='nan').values('setor').distinct()
  
  rank = rank.iloc[:n,:]

  return rank.to_dict('records'), Company.objects.order_by('setor').exclude(setor='nan').values('setor').distinct()


def storeAllCompanies():

  try:
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get('https://fundamentus.com.br/resultado.php', headers=agent)
  except Exception as e:
    return False

  df = pd.read_html(res.content)[0]

  for coluna in list(df):
    if coluna != 'Papel':
      df[coluna] = df[coluna].astype(str).str.replace('.','')
      df[coluna] = df[coluna].astype(str).str.replace(',','.')
      df[coluna] = df[coluna].astype(str).str.rstrip('%').astype('float')/100


  for index, row in df.iterrows():
    a,b = setor(row['Papel'])
    company = Company(nome=a,sigla=row['Papel'],setor=b)
    company.save()

  return True