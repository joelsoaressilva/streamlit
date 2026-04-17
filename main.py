import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_excel('data/data-clientes.xlsx') 

df['faturamento'] = df['total_gasto_cliente'] * df['qtd_compras_cliente']

produtoAgrupado = df.groupby('produto')['faturamento'].sum().reset_index()

faturamentoTotal = df['faturamento'].sum()

produtoSelecionado = st.sidebar.selectbox("Escolha o Produto ",(df['produto'].unique()))

produtoAgrupado['destaque'] = produtoAgrupado['produto'].apply(
    lambda x: 'Selecionado' if x == produtoSelecionado else 'Outros'
)

dfFiltrado = df[df['produto'] == produtoSelecionado]

faturamentoProduto = dfFiltrado['faturamento'].sum()

percentualFaturamento = (faturamentoProduto/faturamentoTotal)*100



quantidadeProduto = df.groupby('produto')['qtd_compras_cliente'].sum().reset_index()

quantidadeProduto['escolhido'] = quantidadeProduto['produto'].apply(
    lambda x: 'Selecionado' if x == produtoSelecionado else 'Outros'
)

NumeroVendas = dfFiltrado['qtd_compras_cliente'].sum()
numeroVendasTotal = df['qtd_compras_cliente'].sum()
percentualVendas = (NumeroVendas/numeroVendasTotal)*100


df['data_compra'] = pd.to_datetime(df['data_compra'])
df['mes'] = df['data_compra'].dt.to_period('M').astype(str)
df_mensal = df.groupby(['mes', 'produto'])['qtd_compras_cliente'].sum().reset_index()

df_mensal['escolhido'] = df_mensal['produto'].apply(
    lambda x: 'Selecionado' if x == produtoSelecionado else 'Outros'
)


fig1 = px.bar(
    produtoAgrupado,
    x='produto',
    y='faturamento',
    color='destaque',
    title='Faturamento por Produto',
    color_discrete_map={
        'Selecionado':'#7C3AED',
        'Outros': '#374151'

    }
)

fig2 = px.bar(
    quantidadeProduto,
    x='produto',
    y='qtd_compras_cliente',
    title='Numero de vendas por produto',
    color='escolhido',
    color_discrete_map={
        'Selecionado':'#7C3AED',
        'Outros': '#374151'  
        }
    
)
fig3 = px.line(
    df_mensal,
    x='mes',
    y='qtd_compras_cliente',
    color='escolhido',
    title='Compras por Produto ao Longo do Tempo',
    color_discrete_map={
        'Selecionado':'#7C3AED',
        'Outros': '#374151'

    }
)


fig1.update_layout(showlegend=False)
fig2.update_layout(showlegend=False)
fig3.update_layout(showlegend=False)

st.set_page_config(layout="wide")

st.title('Dashboard de Analise de Vendas')

st.metric(
    label="Faturamento Total",
    value=f"R$ {faturamentoTotal:,.2f}"
)


col1,col2 = st.columns(2)

with col1:
    st.metric(
    label="Faturamento por produto",
    value=f"R$ {faturamentoProduto:,.2f}",
    delta=f"{percentualFaturamento:.1f}% do total"
)
    st.plotly_chart(fig1)
    st.plotly_chart(fig3)
    



with col2:
    st.metric(
    label="Numero de vendas por produto",
    value=NumeroVendas,
    delta=f"{percentualVendas:.1f}% do total"
)
    st.plotly_chart(fig2)


