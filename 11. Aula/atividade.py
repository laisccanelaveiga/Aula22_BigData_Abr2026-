#Verificando informações de roubo de carro pelo ponto de vista das cidades

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

#Preparando DADOS
try:
    print("Obtendo dados...")
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    #utf-8, iso-8859-1, latin1, cp1252
    df_ocorrecias = pd.read_csv(ENDERECO_DADOS, sep=";", encoding='iso-8859-1')
   
    #deliminitando variáveis
    df_roubo_veiculo = df_ocorrecias[['munic','roubo_veiculo']]
    
    #totalizando os roubos (agrupando por município)
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    
    #manter organizado dos maior pro menor
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo',ascending=False)
    
    # print(df_roubo_veiculo.head(10))

    
except Exception as e:
    print(f'Erro ao obter dados: {e}')

#MEDIDAS - KPI
try:
    # print("===Calculando as Medidas===")
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo)/mediana_roubo_veiculo)
  
    # distancia ate 10% distribuição tem tendencia simetrica / 
    # até 25% a tendencia a distribuição apresentam uma certa assimetria - assimetria moderada - certa dispersão.... extremos estão influenciando no resultado
    # média deve ser descartada / dados assimetricos

    # print(f'\nMedidas de Tendência Central')
    # print("-"*30)
    # print(f'Média: {media_roubo_veiculo:.0f}\nMediana: {mediana_roubo_veiculo:.0f}')
    # print(f'Distância: {distancia:.0%}')


    #50% das cidades do estado teve roubos abaixo de 256 de 2003 até agora
    #o fato da media estar mto maior que a mediana é uma tendência que os extremos estão mto distantes
    #os dados não são simetricos e não tem padrão, são mto diversificados - dados assimétricos
    #nesse caso a média não poderá ser usada como medida de referência.

except Exception as e:
    print(f'Erro ao processar dados: {e}')

#
try:
    # print('\n===Processando os quartis===')

    q1 = np.quantile(array_roubo_veiculo,.25)
    q3 = np.quantile(array_roubo_veiculo,.75)
    
    # print(f'Quartis')
    # print("-"*30)
    # print(f'Q1: {q1:.0f}')
    # print(f'Mediana: {mediana_roubo_veiculo:.0f}')
    # print(f'Q3: {q3:.0f}')
    
    # 25% dos casos de roubo nos municipios do estado do RJ tem números até 48
    # 25% dos casos de roubo nos municipios do estado do RJ tiveram roubos acima de 1017
    
    #municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    # print(f'\nMunicipios com menor índice de roubo')
    # print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=False))

    # print(f'\nMunicipios com Maior índice de roubo')
    # print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter medidas descritivas: {e}')


try:
    # print('\n===Medidas de Dispersão===')
    # amplitude_total = (maximo - minimo)
    # Resultado mais próximo do mínimo indica baixa dispersão
    # Resultado zero indica que todos os dados são iguais
    # Resultado mais próximo do máximo indica alta dispesão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    # print(f'Maior Valor: {maximo}')
    # print(f'Menor Valor: {minimo}')
    # print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular dispersão: {e}')

# IQR = Intervalo Interquartil
try:
    # print('\n===Calculando Outliers===')
    # iqr - é a amplitude dos dados mais centrais (50% entre 25% e 75%) de qq conjunto de dados
    # iqr = q3 - q1
    # mesmo ponto de observação da amplitude
    # ele ignora os extremos 
    # maximo e minimo estão fora do intervalo interquartil
    # não sofrem interferência
    # quanto mais próximo de q1 mais homogêneos são os dados
    # quanto mais próximo de q3, menos homog~eneos são os dados
    iqr = q3 - q1

    # limite inferior:
    # é uma medida que vai identificar como outliers, os valores abaixo dele
    limite_inferior = q1 - (1.5 * iqr)

    # limite superior
    # é uma medida que vai identificar como outliers, os valores acima dele
    limite_superior = q3 + (1.5 * iqr)

    # print(f'Limite Inferior: {limite_inferior}')
    # print(f'Limite Superior: {limite_superior}')
    # print(f'IQR: {iqr}')

    print(f'\n===Medidas===')
    print(f'Menor Valor: {minimo}')
    print(f'Limite Inferior: {limite_inferior:.0f}')
    print(f'Q1: {q1:.0f}')
    print(f'Mediana: {mediana_roubo_veiculo:.0f}')
    print(f'Q3: {q3:.0f}')
    print(f'Limite Superior: {limite_superior:.0f}')
    print(f'Maior Valor: {maximo}')
    print(f'IQR: {iqr}')


except Exception as e:
    print(f'Erro ao calcular outliers: {e}')


try:
    # outliers superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
    # outliers superiores
    df_roubo_veiculo_outliers_inferior = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print(f'\n===Municípios - Outliers Inferiores===')
    print("="*40)
    if len(df_roubo_veiculo_outliers_inferior) == 0:
        print("Não existe Outliers Inferiores")
    else:
        print(df_roubo_veiculo_outliers_inferior.sort_values(by='roubo_veiculo', ascending=False))



    print(f'\n===Municípios - Outliers Superiores===')
    print("="*40)
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print("Não existe Outliers Superiores")
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))


#
except Exception as e:
    print(f'Erro ao calcular Outliers: {e}') 


# para ter outliers tem que ser acima do mínimo . no caso limite inferior não tem outliers
    
try:
# Indica como os dados estão distribuidos en torno de um valor central
# Usada para descrever o grau de simetria ou assimetria de uma distribuição.
# Valores estão equilibrados ?
# Existe uma quantidade de observações de registros maiores ou menores ?
# O peso da distribuição está mais para qual lado ? "p/ os mais baixos ou mais altos?"
# Interpretação:
    
    # Assimetria > 1: Assimetria Positiva Alta
        # Calda longa a direita
        # Valores muito altos puxando a média para cima
        # Tendência de que a média seja maior que a mediana
    
    # Assimetria entre 0.5 e 1: Assimetria Positiva Moderada
        # Calda a direita
        # Valores altos puxando a média para cima mas, é menos acentuada.

    # Assimetria entre -0.5 e 0.5: Distribuição Aproximadamente Simétrica
        # Os dados estão equilibrados em torno da média
        # Média e mediana estarão muito próximas
    
    # Assimetria entre -0.5 e -1: Assimetria Negativa Moderada
        # Calda a esquerda
        # Valores baixos puxando a média para baixo mas, é menos acentuada.

    # Assimetria < -1: Assimetria Negativa Alta
        # Calda longa a esquerdo
        # Valores muito baixos puxando a média para baixo
        # Tendência de que a média seja menor que a mediana

    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()
    print(f'\n===Assimetria===')
    print("="*40)
    print(f'Assimetria: {assimetria:.0f}')


except Exception as e:
    print(f'Erro ao calcular a distribuição: {e}')

try:
    #Curtose
    # Medida que descreve o formato da distribuição 
    # Ajuda a entender se os valores estão espalhados ou mais póximos da média
    # Ajuda a entender se existe outliers 
    # Curtose alta: geralmente temos muitos valores distribuidos em torno da média e,
    # alguns outros muito distantes dela
    # Curtose baixa: os dados tendem a estar distribuídos ao longo do conjunto

    # Interpretação segundo Fisher (PANDAS):
        # Resultado = 0 (Mesocúrtica) --------- Pearson - 3
        # Distribuição Normal
        # Concentração dos dados moderada no centro
        # Outliers são raros, mas podem aparecer
        
        # Resultado < 1 (Platicúrtica) ---------- Pearson < 3
        # Pico achatado
        # Dados mais afastados (espalhados)
        # Poucos extremos, pode haver outliers

        # Resultado > 1 (Leptocúrtica) -------- Pearson > 3
        # Pico mais alto
        # Muitos valores próximos a média
        # Outliers são bem comuns e fortes
        # Caldas mais pesadas
    
    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()
    print(f'\n===Curtose===')
    print("="*40)
    print(f'Curtose: {curtose:.0f}')
     

except Exception as e:
    print(f'Erro ao calcular Curtose: {e}')


try:
    # Medidas de Variabilidade dos dados
    # ----------------------------------
    # Variância 
    # Medida para verificar a dispersão dos dadas
    # Observa-se em relação à média:
        # É a média dos quadrados das diferenças entre cada valor e a média
        # O resultado da variância esá elevado ao quadrado
    # Interpretação:
        # Quanto maior a variância maior o afastamentodos dos valores em relação a média, indicando alta dispersão
        # Quanto menor a variância menor o afastamentodos dos valores em relação a média
    variancia = np.var(array_roubo_veiculo)
    
    # Distancia entre a média e a variância 
    # Até 10% - Baixa Dispersão em relação a Média
    # Entre 10% e 25% - Dispersão Moderada em relação a Média
    # Maior 25% - Alta Dispersão em relação a Média
    distancia_variancia = variancia / (media_roubo_veiculo**2) 
    
    # Desvio Padrão
    # É a raiz quadrada da variância
    # O desvio padrão também é observado em relação a média
    # É a normalização da variância, ou seja, trago o número para a realidade, sem estar elevado ao quadrado
    # Usado para apresentar o quanto os dados podem estar afastados em relação a média (Tanto pra mais quanto pra menos) 
    desvio_padrao = np.std(array_roubo_veiculo)
    
    # Coeficiente de Variação
    # É a magnitude do desvio padrão em relação a média
    coef_variacao = desvio_padrao / media_roubo_veiculo

    print(f'\n===Calculando a Variabilidade dos Dados===')
    print("="*40)
    print(f'Variância: {variancia:.0f}')
    print(f'Distância entre Média e Variância: {distancia_variancia:.0%}')
    print(f'Desvio Padrão: {desvio_padrao:.0f}')
    print(f'Coeficiente de Variação: {coef_variacao:.0%}')
    
    
    print(f'\n')
        
except Exception as e:
    print(f'Erro ao calcular variabilidade dos dados: {e}')

try:
    
    plt.subplots(2,2, figsize=(16,10))
    plt.suptitle('Roubo de Veículos por Município', fontsize=16, fontweight='bold')
    

    # Posição 1 - BoxPlot
    plt.subplot(2, 2, 1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title('BoxPlot - Roubo Veículo')


    # Posição 2 - Medidas
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo:.0f}',fontsize=9)
    plt.text(0.1, 0.8, f'Distância: {distancia:.0%}',fontsize=9)
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.0f}',fontsize=9, color="red")
    plt.text(0.1, 0.6, f'Mínimo: {minimo:.0f}',fontsize=9)
    plt.text(0.1, 0.5, f'Q1: {q1:.0f}',fontsize=9)
    plt.text(0.1, 0.4, f'Mediana: {mediana_roubo_veiculo:.0f}',fontsize=9)
    plt.text(0.1, 0.3, f'Q3: {q3:.0f}',fontsize=9)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior:.0f}',fontsize=9)
    plt.text(0.1, 0.1, f'Máximo: {maximo:.0f}',fontsize=9)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude:.0f}',fontsize=9)
    plt.text(0.5, 0.9, f'Assimetria: {assimetria:.0f}',fontsize=9)
    plt.text(0.5, 0.8, f'Curtose: {curtose:.0f}',fontsize=9)
    plt.text(0.5, 0.7, f'Variância: {variancia:.0f}',fontsize=9)
    plt.text(0.5, 0.6, f'Distância Variância: {distancia_variancia:.0%}',fontsize=9)
    plt.text(0.5, 0.5, f'Desvio Padrão: {desvio_padrao:.0f}',fontsize=9)
    plt.text(0.5, 0.4, f'Coeficiente de Variação: {coef_variacao:.0%}',fontsize=9)
    plt.axis('off')
    plt.title('Resumo Estatístico')


    # Posição 3 - Outliers Superiores
    plt.subplot(2, 2, 3)
    df_roubo_veiculo_outliers_superiores = (
        df_roubo_veiculo_outliers_superiores
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=False)
    )
    plt.bar(
        df_roubo_veiculo_outliers_superiores['munic'], #str.slice(0,10) Corta p texto
        df_roubo_veiculo_outliers_superiores['roubo_veiculo']
    )
    plt.xticks(rotation=45, ha='right') #rotaciona o texto do eixo x

    deslocamento = max(df_roubo_veiculo_outliers_superiores['roubo_veiculo']) * 0.01
    for i, valor in enumerate(df_roubo_veiculo_outliers_superiores['roubo_veiculo']):
            plt.text(
                i, #posição Y
                valor + deslocamento, #posição X
                f'{valor:,}',
                ha='center'
            )
    plt.title('Municípios c/ Outliers Superiores')


    # Posição 4 - Gráfico de Frequência (Histograma)
    plt.subplot(2, 2, 4)
    plt.hist(array_roubo_veiculo, bins=100)
    plt.axvline(media_roubo_veiculo, color='green', linewidth=2)
    plt.axvline(mediana_roubo_veiculo, color='orange', linewidth=2)

    plt.tight_layout() # Ajusta o layout

    plt.show()
     
except Exception as e:
    print(f"Erro ao gerar o gráfico: {e}")


