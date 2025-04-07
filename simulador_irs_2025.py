import streamlit as st

st.set_page_config(page_title="Simulador IRS 2025", layout="wide")
st.title("💰 Simulador de Liquidação de IRS 2025")

# Entradas básicas
st.header("1. Dados Pessoais e Familiares")
estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)"])
regime = st.selectbox("Regime de Tributação", ["Separada", "Conjunta"])
num_dependentes = st.number_input("Número de Dependentes", min_value=0, step=1)

st.header("2. Rendimentos e Retenções")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Titular A - Rendimentos")
    a_cat_a = st.number_input("Rendimento Categoria A", key="a_cat_a")
    a_cat_b = st.number_input("Rendimento Categoria B", key="a_cat_b")
    a_outras = st.number_input("Outros Rendimentos", key="a_outras")
    a_ret = st.number_input("Retenção na Fonte", key="a_ret")
    a_ss = st.number_input("Segurança Social", key="a_ss")

    st.subheader("Titular A - Despesas Dedutíveis")
    a_gerais = st.number_input("Despesas Gerais Familiares", key="a_gerais")
    a_saude = st.number_input("Saúde e Seguros de Saúde", key="a_saude")
    a_edu = st.number_input("Educação e Formação", key="a_edu")
    a_imoveis = st.number_input("Encargos com Imóveis", key="a_imoveis")
    a_lares = st.number_input("Encargos com Lares", key="a_lares")
    a_fatura = st.number_input("Exigência de Fatura (total)", key="a_fatura")
    a_domestico = st.number_input("Trabalho Doméstico", key="a_domestico")

with col2:
    st.subheader("Titular B - Rendimentos")
    b_cat_a = st.number_input("Rendimento Categoria A", key="b_cat_a")
    b_cat_b = st.number_input("Rendimento Categoria B", key="b_cat_b")
    b_outras = st.number_input("Outros Rendimentos", key="b_outras")
    b_ret = st.number_input("Retenção na Fonte", key="b_ret")
    b_ss = st.number_input("Segurança Social", key="b_ss")

    st.subheader("Titular B - Despesas Dedutíveis")
    b_gerais = st.number_input("Despesas Gerais Familiares", key="b_gerais")
    b_saude = st.number_input("Saúde e Seguros de Saúde", key="b_saude")
    b_edu = st.number_input("Educação e Formação", key="b_edu")
    b_imoveis = st.number_input("Encargos com Imóveis", key="b_imoveis")
    b_lares = st.number_input("Encargos com Lares", key="b_lares")
    b_fatura = st.number_input("Exigência de Fatura (total)", key="b_fatura")
    b_domestico = st.number_input("Trabalho Doméstico", key="b_domestico")

st.header("3. Despesas com Dependentes")
dep_saude = st.number_input("Saúde e Seguros de Saúde dos Dependentes")
dep_edu = st.number_input("Educação e Formação dos Dependentes")
dep_lares = st.number_input("Encargos com Lares dos Dependentes")

st.header("4. Resultado da Simulação")

def calcular_irs(rendimento, ss, despesas_dict, ded_dependentes):
    deducao_especifica = min(4462.15, ss)
    rendimento_coletavel = max(0, rendimento - deducao_especifica)

    # Cálculo de deduções com limites
    deducoes = 0
    deducoes += min(250, despesas_dict["gerais"])
    deducoes += min(1000, (despesas_dict["saude"] + ded_dependentes["saude"]) * 0.15)
    deducoes += min(800, (despesas_dict["edu"] + ded_dependentes["edu"]) * 0.30)
    deducoes += min(700, despesas_dict["imoveis"] * 0.15)
    deducoes += min(403.75, (despesas_dict["lares"] + ded_dependentes["lares"]) * 0.25)
    deducoes += min(250, despesas_dict["fatura"] * 0.15)
    deducoes += min(200, despesas_dict["domestico"] * 0.35)

    # Coleta bruta simplificada com taxa média
    coleta = rendimento_coletavel * 0.23
    coleta_liquida = max(0, coleta - deducoes)
    return rendimento_coletavel, coleta_liquida

# Dados Titular A
rendimento_a = a_cat_a + a_cat_b + a_outras
despesas_a = {
    "gerais": a_gerais,
    "saude": a_saude,
    "edu": a_edu,
    "imoveis": a_imoveis,
    "lares": a_lares,
    "fatura": a_fatura,
    "domestico": a_domestico
}

# Dados Titular B
rendimento_b = b_cat_a + b_cat_b + b_outras
despesas_b = {
    "gerais": b_gerais,
    "saude": b_saude,
    "edu": b_edu,
    "imoveis": b_imoveis,
    "lares": b_lares,
    "fatura": b_fatura,
    "domestico": b_domestico
}

# Deduções com dependentes
dep_deducoes = {
    "saude": dep_saude,
    "edu": dep_edu,
    "lares": dep_lares
}

# Separado
rc_a, cl_a = calcular_irs(rendimento_a, a_ss, despesas_a, dep_deducoes)
rc_b, cl_b = calcular_irs(rendimento_b, b_ss, despesas_b, dep_deducoes)
ret_total = a_ret + b_ret
cl_total = cl_a + cl_b
saldo_sep = ret_total - cl_total

# Conjunto
rendimento_total = rendimento_a + rendimento_b
ss_total = a_ss + b_ss
despesas_total = {k: despesas_a[k] + despesas_b[k] for k in despesas_a}
rc_conj, cl_conj = calcular_irs(rendimento_total, ss_total, despesas_total, dep_deducoes)
saldo_conj = ret_total - cl_conj

# Apresentar Resultados
st.subheader("Resultados:")

col1, col2 = st.columns(2)
with col1:
    st.write("**Tributação Separada:**")
    st.metric("Coleta Total", f"{cl_total:,.2f} €")
    st.metric("Retenção Total", f"{ret_total:,.2f} €")
    st.metric("Saldo (a pagar/receber)", f"{saldo_sep:,.2f} €")

with col2:
    st.write("**Tributação Conjunta:**")
    st.metric("Coleta Total", f"{cl_conj:,.2f} €")
    st.metric("Retenção Total", f"{ret_total:,.2f} €")
    st.metric("Saldo (a pagar/receber)", f"{saldo_conj:,.2f} €")

melhor = "Conjunta" if saldo_conj > saldo_sep else "Separada"
st.success(f"💡 A tributação mais vantajosa é: **{melhor}**")
