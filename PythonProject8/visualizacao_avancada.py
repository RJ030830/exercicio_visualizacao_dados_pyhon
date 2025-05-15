import pandas as pd
import plotly.express as px
from dash import Dash, dcc, Input, Output, html

df = pd.read_csv("ecommerce_estatistica (1).csv")
lista_marca = df['Marca'].unique()
options = [{'label': nome, 'value': nome} for nome in lista_marca]

def criacao_grafico(lista_marca):
    filtro_marca = df[df['Marca'].isin(lista_marca)]

    fig1 = px.pie(filtro_marca,
                  names='Marca',
                  color='Marca',
                  hole=0.25,
                  color_discrete_sequence=px.colors.sequential.Rainbow)

    df_corr = df[['Preço', 'Nota', 'Qtd_Vendidos_Cod']].corr()

    fig2 = px.imshow(
        df_corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='Viridis',
        title="Heatmap de correlação")

    fig3 = px.bar(df,
                  x='Temporada',
                  title='Contagem de Vendas por Temporada',
                  color='Temporada')

    fig4 = px.density_heatmap(df,
                              'Nota',
                              'Qtd_Vendidos_Cod',
                              color_continuous_scale=px.colors.sequential.Electric_r)
    return fig1, fig2, fig3, fig4


def criar_app():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Dashboard Dinâmico"),
        html.Br(),
        html.H2("Porcentagem de Vendas por Marca"),
        dcc.Checklist(
            id='id_lista_marca',
            options=options,
            value=[lista_marca[0]],
        ),
        dcc.Graph(id='id_grafico_pie'),
        html.Br(),
        html.H2("Heatmap"),
        dcc.Graph(id='id_grafico_heatmap'),
        html.Br(),
        html.H2("Gráfico de Barra"),
        dcc.Graph(id='id_grafico_barra'),
        html.Br(),
        html.H2("Gráfico de Densidade"),
        dcc.Graph(id='id_grafico_density'),
    ])
    return app

if __name__ == '__main__':
    ap = criar_app()

    @ap.callback(
        [
            Output('id_grafico_pie', 'figure'),
            Output('id_grafico_heatmap', 'figure'),
            Output('id_grafico_barra', 'figure'),
            Output('id_grafico_density', 'figure')
         ],
        [Input('id_lista_marca', 'value')]
    )
    def atualizar_grafico(lista_marca):
        fig1, fig2, fig3, fig4 = criacao_grafico(lista_marca)
        return [fig1,fig2,fig3,fig4]
    ap.run(debug=True, port=8050)