from app import app
from flask import render_template, redirect, request, jsonify
from .modelos.modelos import Modelo
from .controlador import Controlador
import pandas as pd
import json
import ast

modelo = None
controlador = None
dados_originais_html = ''
regras_html = ''
regras_destacadas_no_original_html = ''
regra_escolhida_destacada_html = ''

@app.route('/')
def index():
    init()
    return redirect('/menu')

@app.route('/menu')
def menu():
    init()
    return render_template('menu.html')

@app.route('/param_dados')
def param_dados():
    init()
    return render_template('param_dados.html')

@app.route('/param_regras')
def param_regras():
    init()
    return render_template('param_regras.html')

#rota que salva os dados recebidos pelo usuario no menu
@app.route('/param_dados_received', methods=['POST'])
def get_infos():
    global controlador
    global dados_originais_html
    metadata = request.form['metadata']
    origem = request.form['origem']
    destino = request.form['destino']
    dataset = request.files['dataset']
    try:
        data = pd.read_csv(dataset)
    except:
        return render_template('param_dados.html', erro_msg='Erro ao carregar os dados. Verifique se o arquivo está no formato correto e se os campos foram preenchidos corretamente.')

    if metadata not in data.columns or origem not in data.columns or destino not in data.columns:
        return render_template('param_dados.html', erro_msg='Erro ao carregar os dados. Verifique se o arquivo está no formato correto e se os campos foram preenchidos corretamente.')
   
    controlador.set_dados_originais(data, metadata, origem, destino)
    controlador.set_dados_modificados(data, metadata, origem, destino)
    dados_originais_html = data.to_html(classes='table table-striped')

    return render_template('menu.html')

@app.route('/param_regras_received', methods=['POST'])
def get_infos_regras():
    global controlador
    min_rep = request.form['min_rep']
    min_conf = float(request.form['min_conf'])
    janela_tempo = request.form['janela_tempo']

    if min_rep == '' or min_conf == '' or janela_tempo == '':
        return render_template('param_regras.html', erro_msg='Erro ao carregar os dados. Verifique se os campos foram preenchidos corretamente.')
    
    print(min_rep, min_conf, janela_tempo)
    controlador.set_regras_parametros(min_rep, min_conf, janela_tempo)

    return render_template('menu.html')

@app.route('/dados_originais')
def dados_originais():
    global dados_originais_html
    return render_template('dados_originais.html', dados_originais=dados_originais_html)

@app.route('/procurar_regras')
def procurar_regras():
    global controlador
    global regras_html
    regras_result = controlador.get_regras()

    if len(regras_result) == 0:
        return render_template('regras_encontradas.html', erro_msg='Nenhuma regra encontrada. Tente novamente com outros parâmetros.')
    

    try:
        regras_result.drop(columns=['FA', 'FC'], inplace=True)
    except:
        pass

    try:
        regras_result.rename(columns={'FR': 'Frequência'}, inplace=True)
    except:
        pass    

    return render_template('regras_encontradas.html', regras=regras_result)

@app.route('/itemsets_frequentes')
def itemsets_frequentes():
    global controlador
    itemsets, itemsets_tree_view = controlador.get_itemsets()
    print('Itemsets tree view: ', itemsets_tree_view)

    if itemsets_tree_view:
        return render_template('itemsets_treeview.html', tree=itemsets_tree_view)
    
    if itemsets is None:
        return render_template('itemsets_frequentes.html', erro_msg='Nenhum itemset encontrado. Tente novamente com outros parâmetros.')

    return render_template('itemsets_frequentes.html', itemsets=itemsets)

@app.route('/regras_destacadas_no_original')
def regras_destacadas_no_original():
    global controlador
    global regras_destacadas_no_original_html

    regras = controlador.get_regras()
    dados_originais = controlador.get_dados_originais_ordenados()
    antecedente = controlador.modelo.dados_originais.origem
    consequente = controlador.modelo.dados_originais.destino

    if regras is None:
        return render_template('regras_destacadas_no_original.html', erro_msg='Nenhuma regra encontrada. Tente novamente com outros parâmetros.')
    elif dados_originais is None:
        return render_template('regras_destacadas_no_original.html', erro_msg='Erro ao carregar os dados originais. Tente novamente.')
    transacoes_suspeitas = []
    #retirar das regras os pares de antecedente e consequente
    for index, row in regras.iterrows():
        for elementos in row['Antecedente']:
            transacoes_suspeitas.append(elementos)
        transacoes_suspeitas.append(row['Consequente'])

    #retirar os elementos repetidos
    print(transacoes_suspeitas)
    transacoes_suspeitas = list(set(transacoes_suspeitas))
    print('Transações suspeitas unicas:\n')
    print(transacoes_suspeitas)

    #criar um dataframe com os elementos suspeitos

    df_sus = pd.DataFrame(transacoes_suspeitas, columns=[antecedente, consequente])
    print('Dataframe com os elementos suspeitos:\n')
    print(df_sus)
    #criar um dataframe com os dados originais
    df_orig = dados_originais.copy()

    def find_rows_to_highlight(df_orig, df_sus):
        # Lista para armazenar as linhas que devem ser destacadas
        rows_to_highlight = []

        # Iterar sobre cada linha do dataframe original
        for i, row in df_orig.iterrows():
            # Verificar se a linha atual contém algum dos elementos suspeitos
            for j, sus_row in df_sus.iterrows():
                if (row[antecedente] == sus_row[antecedente] and row[consequente] == sus_row[consequente]):
                    rows_to_highlight.append(i)
                    break
        
        return rows_to_highlight

    # Função para gerar a tabela HTML com destaque nas linhas desejadas
    def gerar_tabela_html(df, indices_destacar):
        html = '<table border="1">'
        # Cabeçalho da tabela
        html += '<thead><tr>'
        for col in df.columns:
            html += '<th>{}</th>'.format(col)
        html += '</tr></thead>'
        # Corpo da tabela
        html += '<tbody>'
        for index, row in df.iterrows():
            html += '<tr style="background-color: yellow;">' if index in indices_destacar else '<tr>'
            for value in row:
                html += '<td>{}</td>'.format(value)
            html += '</tr>'
        html += '</tbody></table>'
        return html
    
    rows_to_highlight = find_rows_to_highlight(df_orig, df_sus)
    print('Linhas a serem destacadas:\n')
    print(rows_to_highlight)

    regras_destacadas_no_original_html = gerar_tabela_html(df_orig, rows_to_highlight)
    
    return render_template('regras_destacadas_no_original.html', regras_destacadas_no_original=regras_destacadas_no_original_html)



@app.route('/destacar_regra', methods=['POST'])
def destacar_regra():
    global controlador
    global regra_escolhida_destacada_html
    antecedentes_da_regra = request.form['antecedente']
    consequente_da_regra = request.form['consequente']
    antecedentes_da_regra = ast.literal_eval(antecedentes_da_regra)
    consequente_da_regra = ast.literal_eval(consequente_da_regra)

    dados_originais = controlador.get_dados_originais_ordenados()
    dados_com_cluster = controlador.get_dados_com_cluster()
    print(dados_com_cluster)
    antecedente = controlador.modelo.dados_originais.origem
    consequente = controlador.modelo.dados_originais.destino

    transacoes_suspeitas = []
    for elemento in antecedentes_da_regra:
        print(elemento)
        transacoes_suspeitas.append(elemento)
    transacoes_suspeitas.append(consequente_da_regra)

    # #retirar os elementos repetidos
    print(transacoes_suspeitas)
    transacoes_suspeitas = list(set(transacoes_suspeitas))
    print('Transações suspeitas unicas:\n')
    print(transacoes_suspeitas)

    #criar um dataframe com os elementos suspeitos

    df_sus = pd.DataFrame(transacoes_suspeitas, columns=[antecedente, consequente])
    print('Dataframe com os elementos suspeitos:\n')
    print(df_sus)
    #criar um dataframe com os dados originais
    df_orig = dados_originais.copy()

    def find_rows_to_highlight(df_orig, df_sus):
        # Lista para armazenar as linhas que devem ser destacadas
        rows_to_highlight = []

        # Iterar sobre cada linha do dataframe original
        for i, row in df_orig.iterrows():
            # Verificar se a linha atual contém algum dos elementos suspeitos
            for j, sus_row in df_sus.iterrows():
                if (row[antecedente] == sus_row[antecedente] and row[consequente] == sus_row[consequente]):
                    rows_to_highlight.append(i)
                    break
        
        return rows_to_highlight

    # Função para gerar a tabela HTML com destaque nas linhas desejadas
    def gerar_tabela_html(df, indices_destacar):
        html = '<table border="1">'
        # Cabeçalho da tabela
        html += '<thead><tr>'
        for col in df.columns:
            html += '<th>{}</th>'.format(col)
        html += '</tr></thead>'
        # Corpo da tabela
        html += '<tbody>'
        for index, row in df.iterrows():
            html += '<tr style="background-color: #FFCCCB;">' if index in indices_destacar else '<tr>'
            for value in row:
                html += '<td>{}</td>'.format(value)
            html += '</tr>'
        html += '</tbody></table>'
        return html
    
    rows_to_highlight = find_rows_to_highlight(df_orig, df_sus)
    print('Linhas a serem destacadas:\n')
    print(rows_to_highlight)

    regra_escolhida_destacada_html = gerar_tabela_html(df_orig, rows_to_highlight)

    #retornar sucesso
    return 'Sucesso'

@app.route('/mostrar_regra_escolhida_destacada')
def mostrar_regra_escolhida_destacada():
    global regra_escolhida_destacada_html
    return render_template('regras_destacadas_no_original.html', regras_destacadas_no_original=regra_escolhida_destacada_html)


def init():
    global modelo
    global controlador
    if modelo is None:
        modelo = Modelo()
        if controlador is None:
            controlador = Controlador(modelo)
    elif controlador is None:
        controlador = Controlador(modelo)

    
