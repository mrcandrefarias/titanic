# -*- coding: utf-8 -*-
"""
Suporte a unicode nos textos e labels.
"""
from __future__ import unicode_literals
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os, sys

titanic_df       = pd.read_csv('../data/titanic.csv')

#Passageiros sobreviventes - Survived igual 1
sobreviventes    = titanic_df[titanic_df.Survived==1]

#retorna os Passageiros que não sobreviventes- Survived igual 1
naosobreviventes = titanic_df[titanic_df.Survived==0]

def numeros_gerais(sobreviventes, naosobreviventes):
    """ Calcula as informações gerais sobre a base de dados do titanic
    Args:
        sobreviventes (pandas.DataFrame): DataFrame contendo os sobreviventes do navio
        naosobreviventes(pandas.DataFrame): DataFrame contendo os não sobreviventes do navio
    Returns:
        dictionary - contendo o total de pessoas da base dados, os sobreviventes e Não sobreviventes.
        exemplo: {'Total de pessoas':20, 'Sobreviventes':8, 'Não Sobreviventes': 12}
    """
    numero_sobreviventes    = len(sobreviventes)
    numero_naosobreviventes = len(naosobreviventes)
    numero_total            = numero_sobreviventes + numero_naosobreviventes
    taxa_sobreviventes   = ( 1. * numero_sobreviventes / numero_total ) * 100
    taxa_naosobreviventes   = ( 1. * numero_naosobreviventes / numero_total ) * 100

    print("Total de pessoas: %i" % numero_total)
    print("Sobreviventes: %i(%.1f%%)" \
            % (numero_sobreviventes, taxa_sobreviventes) \
        )
    print("Não Sobreviventes: %i(%.1f%%)" \
            % (numero_naosobreviventes, taxa_naosobreviventes) \
        )

    numeros_gerais= {'Total de pessoas':numero_total, \
            'Sobreviventes':numero_sobreviventes, 'Não Sobreviventes': numero_naosobreviventes}
    return numeros_gerais

def plot_numeros_gerais(numeros_gerais):
    """ Gera um gráfico de barras com as informações gerais da base de dados do titanic
    Args:
        numeros_gerais (dictionary): Um dicionario - contendo informações gerais da base de dados.
        exemplo: {'Total de pessoas':20, 'Sobreviventes':8, 'Não Sobreviventes': 12}
    """
    plt.bar(range(len(numeros_gerais)), numeros_gerais.values(), color=['b', 'r','g'], align='center')
    plt.xticks(range(len(numeros_gerais)), numeros_gerais.keys())

    # Configuracao da legenda
    plt.legend(handles=[ mpatches.Patch(color='b', label='Total de pessoas'), \
                         mpatches.Patch(color='r', label='Não Sobreviventes'), \
                         mpatches.Patch(color='g', label='Sobreviventes')])

    plt.title("Informações Gerais")
    plt.ylabel('Quantidade de pessoas')
    plt.show()
    sns.plt.show()

def idade_media(sobreviventes, naosobreviventes):
    """ Calcula a média de idade geral, média de idade dos sobreviventes
        e media de idade dos não sobreviventes.
        Args:
            sobreviventes (pandas.DataFrame): DataFrame contendo os sobreviventes.
            naosobreviventes(pandas.DataFrame): DataFrame contendo os não sobreviventes.
    """

    ## A função dropna elimina os valores nulos
    ## http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html
    idades_sobreviventes    = sobreviventes['Age'].dropna().values
    idades_naosobreviventes = naosobreviventes['Age'].dropna().values

    idades_nulas_sobreviventes = len(sobreviventes) - len(idades_sobreviventes)
    idades_nulas_naosobreviventes = len(naosobreviventes) - len(idades_naosobreviventes)

    media_sobreviventes    = idades_sobreviventes.mean()
    media_naosobreviventes = idades_naosobreviventes.mean()
    media_tripulantes      = (media_sobreviventes + media_naosobreviventes)/2
    print("Media de idade dos passageiros: %i" % media_tripulantes)
    print("Media de idade dos sobreviventes: %i" % media_sobreviventes)
    print("Media de idade dos nao sobreviventes: %i" % media_naosobreviventes)

    print("Idades desconhecidas para os sobreviventes: %i(%.1f%%)" \
        % (idades_nulas_sobreviventes, ( 1. * idades_nulas_sobreviventes / len(idades_sobreviventes) ) * 100 ) )
    print("Idades desconhecidas para os nao sobreviventes: %i(%.1f%%)" \
        % (idades_nulas_naosobreviventes, ( 1. * idades_nulas_naosobreviventes / len(idades_naosobreviventes) ) * 100 ) )

def plot_tripulantes_classe(tripulantes_classe, title):
    """ Gera um gráfico de pizza, com os tripulantes do navio
        agrupados por classe de embarque
    Args:
        tripulantes_classe (pandas.core.groupby.DataFrameGroupBy): DataFrameGroupBy contendo os tripulantes
        agrupados por classe de embarque.
        title(string) - Título a ser exibido no gráfico.
    """
    primeira_classe  = tripulantes_classe.get_group(1)['PassengerId'].count()
    segunda_classe = tripulantes_classe.get_group(2)['PassengerId'].count()
    terceira_classe = tripulantes_classe.get_group(3)['PassengerId'].count()
    print("%s,primeira classe: %i, segunda classe: %i, terceira classe: %i," % \
             ( title, primeira_classe, segunda_classe, terceira_classe) \
         )

    labels    = 'Primeira Classe', 'Segunda Classe', 'Terceira Classe'

    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    ax1.pie( (primeira_classe, segunda_classe, terceira_classe), labels=labels,  autopct='%1.1f%%',startangle=90)
    plt.legend(labels, loc="best")
    ax1.axis('equal')
    sns.plt.show()

def plot_passageiros_sexo(quantidadeHomens, quantidadeMulheres, title):
    """ Gera um gráfico de barras, agrupado por sexo
    Args:
        quantidadeHomens (int): Quantidade de Homens
        quantidadeMulheres (int): Quantidade de Mulheres
        title(string) - Título a ser exibido no gráfico.
    """
    plt.bar( range(2), \
            [quantidadeHomens, quantidadeMulheres],\
             color=['b', 'r'], \
             align='center')
    plt.xticks( range(2), ['Homens', 'Mulheres'])

    # Configuracao da legenda
    plt.legend(handles=[ mpatches.Patch(color='b', label='Homens'), \
                         mpatches.Patch(color='r', label='Mulheres')])

    plt.title(title)
    plt.ylabel('Quantidade de pessoas')
    plt.show()
    sns.plt.show()
    tx_masculino = ( 1. * quantidadeHomens / (quantidadeHomens + quantidadeMulheres) ) * 100
    tx_feminino  = ( 1. * quantidadeMulheres / (quantidadeHomens + quantidadeMulheres) ) * 100
    print("%s masculino: %i(%.1f%%)" % \
             ( title, quantidadeHomens, tx_masculino) \
         )
    print("%s feminino: %i(%.1f%%)" % \
             ( title, quantidadeMulheres, tx_feminino) \
         )

def taxa_mulheres_classe(groupMulheresClasse, groupSobreviventesMulheresClasse):
    """ Calcula a proporção e número de mulheres, conforme a classe e embarque,
        primeira, segunda e terceira classe e gera um grafico de barras com essas
        informações
        Args:
            groupMulheresClasse (pandas.core.groupby.DataFrameGroupBy): DataFrameGroupBy contendo as
            mulheres da embarcação, agrupadas por classe de embarque.
            groupSobreviventesMulheresClasse(pandas.core.groupby.DataFrameGroupBy): DataFrameGroupBy contendo as
            mulheres sobreviventes da embarcação, agrupadas por classe de embarque.
    """
    primeiraClasse = groupSobreviventesMulheresClasse.get_group(1)['PassengerId'].count()
    txprimeiraClasse = ( 1. *  primeiraClasse\
                         / groupMulheresClasse.get_group(1)['PassengerId'].count() ) * 100
    segundaClasse    = groupSobreviventesMulheresClasse.get_group(2)['PassengerId'].count()
    txsegundaClasse  = ( 1. * segundaClasse \
                         / groupMulheresClasse.get_group(2)['PassengerId'].count() ) * 100
    terceiraClasse   = groupSobreviventesMulheresClasse.get_group(2)['PassengerId'].count()
    txterceiraClasse = ( 1. * terceiraClasse \
                         / groupMulheresClasse.get_group(3)['PassengerId'].count() ) * 100
    print("Sobreviventes femininas na primeira classe: %i(%1.f%%)" % (primeiraClasse, txprimeiraClasse))
    print("Sobreviventes femininas na segunda classe: %i(%1.f%%)" % (segundaClasse, txsegundaClasse))
    print("Sobreviventes femininas na terceira classe: %i(%1.f%%)" % (terceiraClasse, txterceiraClasse))

    tripulantes = (groupMulheresClasse.get_group(1)['PassengerId'].count(),
                   groupMulheresClasse.get_group(2)['PassengerId'].count(),
                   groupMulheresClasse.get_group(3)['PassengerId'].count())
    ind = np.arange(3)
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tripulantes, width, color='b')
    sobreviventes = (primeiraClasse, segundaClasse, terceiraClasse)
    rects2 = ax.bar(ind + width, sobreviventes, width, color='g')
    ax.set_ylabel('Sobreviventes')
    ax.set_title('Sobreviventes agrupados por sexo e classe de embarque')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('Primeira Classe', 'Segunda Classe', 'Terceira Classe'))
    ax.legend((rects1[0], rects2[0]), ('Passageiras mulheres', 'Sobreviventes mulheres'))
    sns.plt.show()

numeros_gerais = numeros_gerais(sobreviventes, naosobreviventes)
plot_numeros_gerais(numeros_gerais)

idade_media(sobreviventes, naosobreviventes)

plot_tripulantes_classe( titanic_df.groupby('Pclass'), 'Passageiros agrupados por classe de embarque')
plot_tripulantes_classe( sobreviventes.groupby('Pclass'), 'Sobreviventes agrupados por classe de embarque')

passageiros_sexo = titanic_df.groupby('Sex')
#print_group_sex(passageiros_sexo, 'Passageiros')
plot_passageiros_sexo( passageiros_sexo.get_group('male')['PassengerId'].count(), \
                       passageiros_sexo.get_group('female')['PassengerId'].count(), \
                       'Passageiros agrupados por sexo')

sobreviventes_sexo = sobreviventes.groupby('Sex')
#print_group_sex(sobreviventes_sexo, 'Sobreviventes')
plot_passageiros_sexo( sobreviventes_sexo.get_group('male')['PassengerId'].count(), \
                       sobreviventes_sexo.get_group('female')['PassengerId'].count(), \
                      'Sobreviventes agrupados por sexo')

taxa_mulheres_classe( titanic_df[titanic_df.Sex=='female'].groupby(['Pclass']), \
                      sobreviventes[sobreviventes.Sex=='female'].groupby(['Pclass']) )
