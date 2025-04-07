
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
    st.subheader("Titular A")
    a_cat_a = st.number_input("Rendimento Categoria A", key="a_cat_a")
    a_cat_b = st.number_input("Rendimento Categoria B", key="a_cat_b")
    a_outras = st.number_input("Outros Rendimentos", key="a_outras")
    a_ret = st.number_input("Retenção na Fonte", key="a_ret")
    a_ss = st.number_input("Segurança Social", key="a_ss")
    a_saude = st.number_input("Despesas de Saúde", key="a_saude")
    a_edu = st.number_input("Despesas de Educação", key="a_edu")
    a_hab = st.number_input("Despesas de Habitação", key="a_hab")

with col2:
    st.subheader("Titular B")
    b_cat_a = st.number_input("Rendimento Categoria A", key="b_cat_a")
    b_cat_b = st.number_input("Rendimento Categoria B", key="b_cat_b")
    b_outras = st.number_input("Outros Rendimentos", key="b_outras")
    b_ret = st.number_input("Retenção na Fonte", key="b_ret")
    b_ss = st.number_input("Segurança Social", key="b_ss")
    b_saude = st.number_input("Despesas de Saúde", key="b_saude")
    b_edu = st.number_input("Despesas de Educação", key="b_edu")
    b_hab = st.number_input("Despesas de Habitação", key="b_hab")

st.header("3. Resultado da Simulação")

def calcular_irs(rendimento, ss, despesas):
    deducao_especifica = min(4462.15, ss)
    rendimento_coletavel = max(0, rendimento - deducao_especifica)
    coleta = rendimento_coletavel * 0.23  # simplificação
    deducoes = min(600, sum(despesas))
    coleta_liquida = max(0, coleta - deducoes)
    return rendimento_coletavel, coleta_liquida

# Cálculos para cada titular
rendimento_a = a_cat_a + a_cat_b + a_outras
despesas_a = [a_saude, a_edu, a_hab]
rc_a, cl_a = calcular_irs(rendimento_a, a_ss, despesas_a)

rendimento_b = b_cat_a + b_cat_b + b_outras
despesas_b = [b_saude, b_edu, b_hab]
rc_b, cl_b = calcular_irs(rendimento_b, b_ss, despesas_b)

# Coletas e Retenções
ret_total = a_ret + b_ret
cl_total = cl_a + cl_b
saldo_sep = ret_total - cl_total

# Regime conjunto
rc_conj, cl_conj = calcular_irs(rendimento_a + rendimento_b, a_ss + b_ss, despesas_a + despesas_b)
saldo_conj = ret_total - cl_conj

# Apresentar resultados
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

# Recomendação
melhor = "Conjunta" if saldo_conj > saldo_sep else "Separada"
st.success(f"💡 A tributação mais vantajosa é: **{melhor}**")
