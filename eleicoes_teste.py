#==================================================
# Comparação cotação dólar e resultado das eleições
#==================================================
import pandas as pd
from matplotlib import dates, pyplot as plt
import numpy as np
from datetime import datetime as dt

author = "Farias, M. G. Luís"

#ler .csv dos dados das pesquisas e cotação do dolar no ultimo mês
cotacao = pd.read_csv('USD_BRL.csv')
datafolha = pd.read_csv('datafolha.csv')
ibope = pd.read_csv('ibope.csv')

#Adcionando os dados do Dataframe às arrays
bolsonaro_df = np.array([x for x in datafolha[datafolha['candidato'] == 'Bolsonaro']['intencao']])
bolsonaro_ib = np.array([x for x in ibope[ibope['candidato'] == 'Bolsonaro']['intencao']])
haddad_df = np.array([x for x in datafolha[datafolha['candidato'] == 'Haddad']['intencao']])
haddad_ib = np.array([x for x in ibope[ibope['candidato'] == 'Haddad']['intencao']])
ciro_df = np.array([x for x in datafolha[datafolha['candidato'] == 'Ciro']['intencao']])
ciro_ib = np.array([x for x in ibope[ibope['candidato'] == 'Ciro']['intencao']])
cotacao_val = np.array([float(x.replace(',','.')) for x in cotacao['Último']],dtype = 'float64')

#Criando uma nova array com as datas e fazendo uma melhor formatação das mesmas
data_df = datafolha['data'].unique()
data_df = [dt.strptime(d, '%d/%m') for d in data_df]
data_df = dates.date2num(data_df)
data_ib = ibope['data'].unique()
data_ib = [dt.strptime(d, '%d/%m') for d in data_ib]
xaxis = dates.date2num(data_ib) #Usado como parametro para a formatação das datas no gráfico
data_cot = np.array([x[:5] for x in cotacao['Data']][::-1])
data_cot = [dt.strptime(d, '%d.%m') for d in data_cot]
data_cot = dates.date2num(data_cot)

#Definindo plotagem das pesquisas
fig, ax = plt.subplots(2, sharex = True)
sam1 = ax[0].plot(data_df, bolsonaro_df, '^-', color = 'green')
sam4 = ax[0].plot(data_ib, bolsonaro_ib, 'o-', color = 'green')
sam2 = ax[0].plot(data_df, haddad_df, '^-', color = 'red')
ax[0].plot(data_ib, haddad_ib, 'o-', color = 'red')
sam3 = ax[0].plot(data_df, ciro_df, '^-', color = 'yellow')
ax[0].plot(data_ib, ciro_ib, 'o-', color = 'yellow')

#Plotagem da cotação
ax[1].plot(data_cot, cotacao_val, '->', color = 'grey')

## Adicionando anotações na cotação
dif = 0 #auxiliar para ajudar na troca de cores nas anotações
for i,j in zip(data_cot, cotacao_val):
    if j > dif:
        dif = j
        ax[1].annotate(str(j)[:4],xy = (i,j), color = 'green')
    elif j <= dif:
        dif = j
        ax[1].annotate(str(j)[:4],xy = (i,j), color = 'red')

#Definindo as legendas legenda
leg2 = ax[0].legend((sam1[0],sam4[0]),('Datafolha', 'Ibope'), loc = 1)
ax[0].legend((sam1[0],sam2[0],sam3[0]),('Bolsonaro', 'Haddad', 'Ciro'), loc = 2)

#Aqui é ajustado o formato da data na plotagem
dateForm = dates.DateFormatter('%d\n%m')
ax[1].xaxis.set_major_formatter(dateForm)
plt.xticks(np.unique(np.append(data_df, xaxis)))

ax[0].add_artist(leg2)

plt.show()
