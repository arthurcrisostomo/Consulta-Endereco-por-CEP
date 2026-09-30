# > Importa Tkinter
from tkinter import *

# > Importa modulo ttk que contem o Treeview
from tkinter import ttk

# > Importa filedialog para abrir caixa de seleção e selecionar o arquivo especifico
from tkinter import filedialog

# > Importa modulo webdriver do selenium para controlar o navegador
from selenium import webdriver

# > Importa a classe TimeoutException para tratar erros apos acabar o tempo determinado no WebDriverWait
from selenium.common import TimeoutException

# > Importa classe By para localizar elementos na pagina
from selenium.webdriver.common.by import By

# > Importa classe WebDriverWait para aguardar um elemento aparecer na pagina com base em uma condição pré-pronta
from selenium.webdriver.support.ui import WebDriverWait

# > Importa modulo expected_conditions que contem condições pré-prontas para ser utilizado junto com o WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# > Importa Options para definir parametros adicionais de inicialização para o navegador
from selenium.webdriver.chrome.options import Options

# > Importa os para interagir com o SO
import os

def obter_caminho_historico():
    # > Define o nome do arquivo a ser encontrado
    nome_arquivo = 'historico.txt'

    # > Retorna o diretorio do usuario
    caminho_save_data = os.path.join(os.path.expanduser('~'), nome_arquivo)

    # > Forma o caminho completo usando join, porque independente do sistema que o codigo esta rodando, o join automaticamente detecta se deve usar / ou \
    return caminho_save_data

def ver_integridade_arquivo(treeview):
    # > Obtem o caminho do arquivo que armazena o historico de consultas
    caminho_completo = obter_caminho_historico()

    # > Verifica se o caminho completo do arquivo existe
    if os.path.exists(caminho_completo):

        # > Caso exista chama a função responsável por carregar as informações do arquivo para o Treeview
        carregar_arquivo_treeview(caminho_completo, treeview)

    # > Caso não tenha cria o arquivo que armazena o historico de consultas
    else:
        criar_arquivo_historico()

def criar_arquivo_historico():
    # > Coleta o caminho onde o arquivo que armazena o historico vai ser criado
    caminho_save_data = obter_caminho_historico()

    # > Cria o arquivo que armazena as consultas
    # with > Garante o fechamento correto do arquivo
    # a > Cria o arquivo caso não exista
    # enconding = Define o tipo de codificação como utf-8 para carregar caracteres e simbolos especificos
    with open(caminho_save_data, 'a', encoding='utf-8') as _:
        pass

def selecionar_arquivo_ceps(entry_caminho):
    # > Abre a caixa de dialogo para selecionar o arquivo e retorna o endereço para a variavel
    caminho_arquivo = filedialog.askopenfilename()

    # > Deleta o texto da posição 0 ate o final
    entry_caminho.delete(0, END)

    # > Insere o texto do caminho_arquivo na posição 0
    entry_caminho.insert(0, caminho_arquivo)

def ler_ceps(caminho_arquivo_ceps):
    # with > Garante o fechamento correto do arquivo
    # caminho_arquivo > Caminho do arquivo txt
    # r > Parametro apenas para leitura do arquivo
    # encoding > Define o tipo de codificação para leitura de caracteres especiais
    # readlines > Retorna cada linha do arquivo em uma lista
    with open(caminho_arquivo_ceps, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()

    # > Retorna o conteudo para quem chamou
    return conteudo

def buscar_endereco(conteudo_arquivo):

    # > Instancia a classe Options para a variavel opcoes na qual vai armazenar os parametros adicionais de inicialização
    opcoes = Options()

    # > Adiciona o parametro --headless=new na qual vai fazer o navegador ser executado em segundo plano
    opcoes.add_argument('--headless=new')

    # > Abre uma janela do nav Chrome usando os parametros adicionais armazenados na variavel opcoes e atribui a pagina a variavel navegador
    navegador = webdriver.Chrome(options=opcoes)

    # > Dicionario que vai armazenar todos os dicionarios que contem os dados de cep
    dict_dados = {}

    # > Itera sobre item da lista que foi
    for cep_linha in conteudo_arquivo:
        try:
            # get > Acessa a pagina web especificada
            navegador.get(f'https://buscacep.com.br/cep/{cep_linha}')

            # WebdriverWait > Aguarda um elemento com base em uma condição
            # navegador > Variavel que armazena a janela do navegador
            # 20 > Espera por ate 20s
            # until > Verifica a cada 0.5s
            # ec > Contem Condiçoes pré-prontas
            # presence_of_element_located > Verifica se o elemento existeno DOM da pagina
            elemento_logradouro = WebDriverWait(navegador, 20).until(
                ec.presence_of_element_located((By.XPATH, '//div[dt="Logradouro"]/dd'))
            )
            elemento_cidade = WebDriverWait(navegador, 20).until(
                ec.presence_of_element_located((By.XPATH, '//div[dt="Cidade"]/dd'))
            )
            elemento_bairro = WebDriverWait(navegador, 20).until(
                ec.presence_of_element_located((By.XPATH, '//div[dt="Bairro"]/dd'))
            )
            elemento_estado = WebDriverWait(navegador, 20).until(
                ec.presence_of_element_located((By.XPATH, '//div[dt="Estado"]/dd'))
            )
            elemento_cep = WebDriverWait(navegador, 20).until(
                ec.presence_of_element_located((By.XPATH, '//div[dt="CEP"]/dd'))
            )

            # text > Pega apenas o texto de cada elemento e armazena na variavel respectiva
            logradouro = elemento_logradouro.text
            cidade = elemento_cidade.text
            bairro = elemento_bairro.text
            estado = elemento_estado.text
            cep = elemento_cep.text

            # > Cria um dicionario com o nome do CEP atual padronizando com
            dict_dados[cep] = {}

            # > Cria uma chave-valor dentro do dict interno: [nome do elemento] = valor do elemento
            dict_dados[cep]['logradouro'] = logradouro
            dict_dados[cep]['cidade'] = cidade
            dict_dados[cep]['bairro'] = bairro
            dict_dados[cep]['estado'] = estado
            dict_dados[cep]['cep'] = cep

        except TimeoutException:
            continue

    # > Retorna o dicionario que tem todas as informações de cada cep de forma organizada
    return dict_dados

def add_info_arquivo_save(dados):

    # > Chama a função responsável por coletar o caminho do arquivo no usuario da pessoa atual
    caminho_save_data = obter_caminho_historico()

    # > Itera sobre cada chave cep do dicionario dados que contem os dados de cada cep
    for chave_cep in dados:
        rua = dados[chave_cep]['logradouro']
        cidade = dados[chave_cep]['cidade']
        bairro = dados[chave_cep]['bairro']
        estado = dados[chave_cep]['estado']
        cep = dados[chave_cep]['cep']

        # with > Garante o fechamento correto do arquivo
        # caminho_completo > Caminho completo do arquivo que vai ser aberto
        # a > Vai adicionar no arquivo
        # encoding > Define o tipo de codificação como utf-8 para ler simbolos e caracteres especificos
        with open(caminho_save_data, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'{rua},{cidade},{bairro},{estado},{cep}\n')

def carregar_arquivo_treeview(caminho_save_data, treeview):

    id_linhas = treeview.get_children()

    for id_linha in id_linhas:
        treeview.delete(id_linha)

    # with > Garante o fechamento correto do arquivo
    # caminho_completo > Caminho completo do arquivo que vai ser aberto
    # r > Parametro apenas de Leitura
    # encoding > Define o tipo de codificação como utf-8 para ler simbolos e caracteres especificos
    with open(caminho_save_data, 'r', encoding='utf-8') as arquivo:

        # > Itera sobre cada linha do arquivo
        for linha in arquivo:

            # > Transforma a linha string completa para valor individual em uma lista
            valores = linha.split(',')
            treeview.insert('', END, values=valores)

def controller(entry_caminho, treeview):

    # > Obtem o caminho do arquivo que armazena o historico de consultas
    caminho_save_data = obter_caminho_historico()

    # > Coleta o caminho do arquivo que contem os ceps
    caminho_arquivo_ceps = entry_caminho.get()

    # > Chama a função responsável por ler e retornar cada linha do arquivo em uma lista e armazena na variavel conteudo_arquivo
    lista_ceps = ler_ceps(caminho_arquivo_ceps)

    # > Chama a função responsável por fazer a busca de informações de todos os ceps que existem dentro da variavel conteudo_arquivo, retornando um dicionario com os dados separado por cep e armazenando na variavel dict_ceps
    dict_ceps = buscar_endereco(lista_ceps)

    # > Adiciona as informações no arquivo save que contem o historico de pesquisas
    add_info_arquivo_save(dict_ceps)

    # > Atualiza o treeview com as novas informações e passa pra função carregar_arquivo_treeview o caminho do arquivo que armazena o historico de consultas
    carregar_arquivo_treeview(caminho_save_data, treeview)

def main():

    # > Instancia a classe tk e armazena a janela na variavel
    janela = Tk()

    # > Define o titulo da janela
    janela.title('Selecionar Arquivo Busca cep adiciona no treeview')

    # > Define o tamanho da janela
    janela.geometry('1000x400')

    ########## LABEL ##########
    label_caminho = Label(
        text='Caminho:',
        font='Arial 17'
    )
    label_caminho.grid(row=0, column=0)
    ###########################

    ########## ENTRY ##########
    entry_caminho = Entry(
        font='Arial 17',
        width=29
    )
    entry_caminho.grid(row=0, column=1, sticky='ns')
    ###########################

    ########## BUTTON ##########
    # command > chama a função responsável por selecionar o arquivo e passa função a variavel entry_caminho
    button_selecionar = Button(
        text='Selecionar Arquivo',
        font='Arial 17',
        bg='gray',
        fg='white',
        command=lambda: selecionar_arquivo_ceps(entry_caminho)
    )
    button_selecionar.grid(row=0, column=2)

    button_iniciar = Button(
        text='Iniciar',
        font='Arial 17',
        bg='black',
        fg='white',
        command=lambda: controller(entry_caminho, treeview)
    )
    button_iniciar.grid(row=0, column=3)
    ############################

    # > Cria uma instancia da classe Style na variavel estilo_treeview que vai armazenar as configurações de cores, fontes, temas, etc
    estilo_treeview = ttk.Style()

    # theme use > Temas pré-definidos que mudam a aparencia geral dos widgets (clam, alt, default, classic)
    estilo_treeview.theme_use('alt')

    estilo_treeview.configure('.', font='Arial 15')

    # > Define uma lista para ser usada como ID e como texto de cada coluna do Treeview
    id_colunas = ['Rua', 'Cidade', 'Bairro', 'Estado', 'CEP']

    treeview = ttk.Treeview(
        # > Define o ID de cada coluna do treeview
        columns=id_colunas,

        # > Remove a coluna extra reservada para arvores/hierarquias
        show='headings'
    )

    # > Itera sobre cada id da lista id_colunas
    for idd in id_colunas:

        # > Localiza a coluna do treeview pelo id atual e insere o texto do id
        treeview.heading(idd, text=idd)

    # > Define a posição do treeview e a largura que o widget vai ocupar
    treeview.grid(row=1, column=0, columnspan=4)

    # > Chama a função responsável por verificar a integridade do arquivo e passa o treeview para a função
    ver_integridade_arquivo(treeview)

    # > Deixa a jenela principal sempre aberta
    janela.mainloop()

if __name__ == '__main__':
    main()
