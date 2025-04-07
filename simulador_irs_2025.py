import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Simulador IRS 2025", layout="wide")
st.title("💰 Simulador de Liquidação de IRS 2025")

# Entradas básicas
st.header("1. Dados Pessoais e Familiares")
estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)"])
regime = st.selectbox("Regime de Tributação", ["Separada", "Conjunta"])
num_dependentes = st.number_input("Número de Dependentes", min_value=0, step=1)

st.header("2. Rendimentos e Despesas dos Titulares")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Titular A - Rendimentos")
    a_cat_a = st.number_input("Rendimento Categoria A", key="a_cat_a")
    a_cat_b = st.number_input("Rendimento Categoria B", key="a_cat_b")
    a_outras = st.number_input("Outros Rendimentos", key="a_outras")
    a_ret = st.number_input("Retenção na Fonte", key="a_ret")
    a_ss = st.number_input("Segurança Social", key="a_ss")

    st.subheader("Titular A - Despesas")
    a_gerais = st.number_input("Despesas Gerais", key="a_gerais")
    a_saude = st.number_input("Saúde", key="a_saude")
    a_edu = st.number_input("Educação", key="a_edu")
    a_imoveis = st.number_input("Imóveis", key="a_imoveis")
    a_lares = st.number_input("Lares", key="a_lares")
    a_fatura = st.number_input("Exigência Fatura", key="a_fatura")
    a_domestico = st.number_input("Trabalho Doméstico", key="a_domestico")

with col2:
    st.subheader("Titular B - Rendimentos")
    b_cat_a = st.number_input("Rendimento Categoria A", key="b_cat_a")
    b_cat_b = st.number_input("Rendimento Categoria B", key="b_cat_b")
    b_outras = st.number_input("Outros Rendimentos", key="b_outras")
    b_ret = st.number_input("Retenção na Fonte", key="b_ret")
    b_ss = st.number_input("Segurança Social", key="b_ss")

    st.subheader("Titular B - Despesas")
    b_gerais = st.number_input("Despesas Gerais", key="b_gerais")
    b_saude = st.number_input("Saúde", key="b_saude")
    b_edu = st.number_input("Educação", key="b_edu")
    b_imoveis = st.number_input("Imóveis", key="b_imoveis")
    b_lares = st.number_input("Lares", key="b_lares")
    b_fatura = st.number_input("Exigência Fatura", key="b_fatura")
    b_domestico = st.number_input("Trabalho Doméstico", key="b_domestico")

st.header("3. Despesas com Dependentes")
despesas_dep = {
    "gerais": 0, "saude": 0, "edu": 0, "imoveis": 0,
    "lares": 0, "fatura": 0, "domestico": 0
}

for i in range(1, int(num_dependentes) + 1):
    with st.expander(f"Dependente {i}"):
        despesas_dep["gerais"] += st.number_input(f"Gerais - Dep {i}", key=f"dep{i}_gerais")
        despesas_dep["saude"] += st.number_input(f"Saúde - Dep {i}", key=f"dep{i}_saude")
        despesas_dep["edu"] += st.number_input(f"Educação - Dep {i}", key=f"dep{i}_edu")
        despesas_dep["imoveis"] += st.number_input(f"Imóveis - Dep {i}", key=f"dep{i}_imoveis")
        despesas_dep["lares"] += st.number_input(f"Lares - Dep {i}", key=f"dep{i}_lares")
        despesas_dep["fatura"] += st.number_input(f"Fatura - Dep {i}", key=f"dep{i}_fatura")
        despesas_dep["domestico"] += st.number_input(f"Doméstico - Dep {i}", key=f"dep{i}_domestico")

def calcular_irs(rend, ss, desp, dep):
    ded_esp = min(4462.15, ss)
    rc = max(0, rend - ded_esp)
    ded = 0
    ded += min(250, desp["gerais"] + dep["gerais"])
    ded += min(1000, (desp["saude"] + dep["saude"]) * 0.15)
    ded += min(800, (desp["edu"] + dep["edu"]) * 0.30)
    ded += min(700, (desp["imoveis"] + dep["imoveis"]) * 0.15)
    ded += min(403.75, (desp["lares"] + dep["lares"]) * 0.25)
    ded += min(250, (desp["fatura"] + dep["fatura"]) * 0.15)
    ded += min(200, (desp["domestico"] + dep["domestico"]) * 0.35)
    coleta = rc * 0.23
    return rc, coleta - ded

# Cálculos
rend_a = a_cat_a + a_cat_b + a_outras
rend_b = b_cat_a + b_cat_b + b_outras
rc_a, cl_a = calcular_irs(rend_a, a_ss, {
    "gerais": a_gerais, "saude": a_saude, "edu": a_edu,
    "imoveis": a_imoveis, "lares": a_lares, "fatura": a_fatura, "domestico": a_domestico
}, despesas_dep)
rc_b, cl_b = calcular_irs(rend_b, b_ss, {
    "gerais": b_gerais, "saude": b_saude, "edu": b_edu,
    "imoveis": b_imoveis, "lares": b_lares, "fatura": b_fatura, "domestico": b_domestico
}, despesas_dep)
ret_total = a_ret + b_ret
cl_sep = cl_a + cl_b
saldo_sep = ret_total - cl_sep

rc_conj, cl_conj = calcular_irs(rend_a + rend_b, a_ss + b_ss, {
    k: a + b for k, a, b in zip(despesas_dep.keys(),
        [a_gerais, a_saude, a_edu, a_imoveis, a_lares, a_fatura, a_domestico],
        [b_gerais, b_saude, b_edu, b_imoveis, b_lares, b_fatura, b_domestico])
}, despesas_dep)
saldo_conj = ret_total - cl_conj

melhor = "Conjunta" if saldo_conj > saldo_sep else "Separada"
st.success(f"💡 Regime mais vantajoso: {melhor}")

# Exportação para Excel
if st.button("📥 Exportar para Excel"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        pd.DataFrame({
            "Campo": ["Estado Civil", "Regime", "Dependentes"],
            "Valor": [estado_civil, regime, num_dependentes]
        }).to_excel(writer, sheet_name="Geral", index=False)

        pd.DataFrame({
            "Titular": ["A"] * 7 + ["B"] * 7,
            "Campo": (["Gerais", "Saúde", "Educação", "Imóveis", "Lares", "Fatura", "Doméstico"])*2,
            "Valor": [a_gerais, a_saude, a_edu, a_imoveis, a_lares, a_fatura, a_domestico,
                      b_gerais, b_saude, b_edu, b_imoveis, b_lares, b_fatura, b_domestico]
        }).to_excel(writer, sheet_name="Despesas Titulares", index=False)

        pd.DataFrame(despesas_dep, index=["Dependentes"]).T.reset_index().rename(
            columns={"index": "Categoria", "Dependentes": "Total (€)"}
        ).to_excel(writer, sheet_name="Despesas Dependentes", index=False)

        pd.DataFrame({
            "Cálculo": ["Rend. Coletável A", "Rend. Coletável B", "Coleta A", "Coleta B",
                        "Coleta Total Separada", "Coleta Conjunta", "Retenção Total",
                        "Saldo Separado", "Saldo Conjunto", "Mais Vantajoso"],
            "Valor (€)": [rc_a, rc_b, cl_a, cl_b, cl_sep, cl_conj, ret_total,
                          saldo_sep, saldo_conj, melhor]
        }).to_excel(writer, sheet_name="Cálculos", index=False)

    st.download_button("📄 Download Excel", data=buffer.getvalue(),
                       file_name="simulador_irs_2025.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
