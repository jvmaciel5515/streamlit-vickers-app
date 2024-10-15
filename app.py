import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Criação de cabeçalho
st.title("Aplicativo de Dureza Vickers")

# Número de áreas
num_areas = st.number_input("Quantas áreas você deseja calcular?", min_value=1)

# Dicionário para armazenar áreas
areas = {}
for i in range(int(num_areas)):
    nome_area = st.text_input(f"Digite o nome da Área {i + 1}: ")
    areas[nome_area] = {"medias": [], "hvs": [], "profundidade": None}  # Adiciona profundidade ao dicionário

# Valor da carga
valor_parametro = st.number_input("Digite o valor da carga (ex: 0.5): ", value=0.0)

# Número de medições
n = st.number_input("Quantas medições você deseja calcular para cada área?", min_value=1)

# Coletar dados para cada área
for area in areas.keys():
    st.subheader(f"Área: {area}")
    
    # Solicitar profundidade uma vez por área
    profundidade = st.number_input(f"Digite a profundidade para a área {area} (em um): ", value=0.0, key=f"profundidade_{area}")
    areas[area]["profundidade"] = profundidade  # Armazenar a profundidade

    for i in range(int(n)):
        st.text(f"Medição {i + 1}:")
        
        # Permitir números negativos e decimais para as medições
        d1 = st.number_input(f"Digite a MEDIDA 1 (Medição {i + 1}): ", value=0.0, key=f"medida1_{area}_{i}")
        d2 = st.number_input(f"Digite a MEDIDA 2 (Medição {i + 1}): ", value=0.0, key=f"medida2_{area}_{i}")

        # Cálculo da média
        media = (d1 + d2) / 2
        areas[area]["medias"].append(media)

        # Cálculo de HV
        if media != 0:  # Verificar se a média é diferente de zero
            HV = 1.8544 * valor_parametro / (media / 2000) ** 2
            areas[area]["hvs"].append(HV)
            st.write(f"O resultado para a medição {i + 1} na área {area} é HV = {HV:.2f} com profundidade = {profundidade:.2f} mm")
        else:
            st.error("A média deve ser diferente de zero para calcular HV.")

# Gerar listas para profundidades e valores HV
profundidades = []
valores_hv = []
medias_hv = {}
for area in areas.values():
    profundidades.append(area["profundidade"])  # Profundidade única por área
    if area["hvs"]:  # Se houver valores de HV
        medias_hv[area["profundidade"]] = np.mean(area["hvs"])  # Média dos HVs por área
        valores_hv.append(np.mean(area["hvs"]))  # Adiciona média HV
    else:
        valores_hv.append(0)  # Se não houver valores, adiciona zero

# Gerar gráfico HV vs. Profundidade (gráfico de linha)
if len(profundidades) == len(valores_hv) and len(valores_hv) > 0:  # Verificar se as listas têm o mesmo tamanho
    plt.figure(figsize=(10, 6))
    plt.plot(profundidades, valores_hv, marker='o', linestyle='-', color='b', alpha=0.7)  # Gráfico de linha
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Média Dureza Vickers (HV)")
    plt.title("Média Dureza Vickers em relação à Profundidade")
    plt.grid()
    st.pyplot(plt)
else:
    st.warning("Nenhum valor de HV disponível para plotar.")

# Gerar gráfico HV vs. Área
if medias_hv:
    plt.figure(figsize=(10, 6))
    areas_names = list(areas.keys())
    hv_values = [medias_hv[areas[area]["profundidade"]] for area in areas_names]

    plt.bar(areas_names, hv_values, alpha=0.7, color='b')
    plt.xlabel("Área")
    plt.ylabel("Média Dureza Vickers (HV)")
    plt.title("Média Dureza Vickers por Área")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    st.pyplot(plt)
else:
    st.warning("Nenhuma média HV disponível para o gráfico por área.")





