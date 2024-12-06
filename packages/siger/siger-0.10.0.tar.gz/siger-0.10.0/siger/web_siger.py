""" WEB SIGER"""
import os
import time
import zipfile
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from .import_siger import ImportSIGER

class WebSIGER(ImportSIGER):
    """
    Classe para interação automatizada com o sistema SIGER via interface web.

    Esta classe oferece métodos para automatizar a interação com o sistema SIGER por meio de uma interface web. Ela inclui funcionalidades para login, importação, escorregamento, exclusão e zeramento de arquivos.

    Atributos
    ----------
    url_siger : str
        A URL de acesso ao sistema SIGER.

    usuario : str
        O nome de usuário para login no sistema SIGER.

    senha : str
        A senha de usuário para login no sistema SIGER.

    Métodos
    -------
    carrega_siger(df_arquivos, cd)
        Realiza o carregamento de arquivos no sistema SIGER conforme especificado em um DataFrame.

    __inic_navegador(cd)
        Inicializa o navegador Chrome para interação com o sistema SIGER.

    __login_siger(navegador, user, key)
        Realiza o login no sistema SIGER por meio do navegador.

    __imp_arquivo_siger(navegador, file, commentary)
        Importa um arquivo para o sistema SIGER por meio do navegador.

    __esc_arquivo_siger(navegador, file, commentary)
        Realiza o escorregamento de obras no sistema SIGER por meio do navegador.

    __del_arquivo_siger(navegador, file, commentary)
        Exclui um arquivo do sistema SIGER por meio do navegador.

    __zer_arquivo_siger(navegador)
        Zera equipamentos no sistema SIGER por meio do navegador.
    """
    ###================================================================================================================
    ###
    ### CÓDIGOS DE INICIALIZAÇÃO
    ###
    ###================================================================================================================
    def __init__(self, url_siger, usuario, senha):
        """
        Inicializa um objeto da classe WebSIGER.

        Parameters
        ----------
        url_siger : str
            URL de conexão com o sistema SIGER.
        usuario : str
            Nome de usuário para autenticação no sistema SIGER.
        senha : str
            Senha para autenticação no sistema SIGER.

        Returns
        -------
        None

        Notes
        -----
        Este método inicializa um objeto VisualizaSIGER para uso no módulo. Ele herda todas as funções da classe ImportSIGER para serem utilizadas neste módulo.

        Examples
        --------
        >>> visualizador = VisualizaSIGER('https://exemplo.com/siger', 'usuario', 'senha')
        """
        # Pegando todas as funções da Import_SIGER para uso nesse módulo
        super().__init__(url_siger, usuario, senha)

    ###================================================================================================================
    ###
    ### FUNÇÕES AUXILIARES
    ###
    ###================================================================================================================
    def __inic_navegador(self, cd, path_download=""):
        """
        Inicia o navegador Chrome para navegação automatizada.

        Parâmetros
        ----------
        cd : str
            O caminho para o arquivo executável do ChromeDriver.

        Retorna
        -------
        navegador : selenium.webdriver.Chrome
            Uma instância do navegador Chrome configurada para navegação automatizada.

        Notas
        -----
        Este método inicializa um navegador Chrome utilizando o ChromeDriver, permitindo a navegação automatizada em páginas da web.
        O navegador é maximizado e a URL especificada ao inicializar a classe VisualizaSIGER é aberta.

        Dependências
        ------------
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - webdriver.ChromeOptions: Classe para configurar as opções do navegador Chrome.
        """
        # Inicializa o navegador
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        if path_download != "":
            chrome_options.add_experimental_option("prefs", {"download.default_directory": path_download,
                                                             "download.prompt_for_download": False,
                                                             "download.directory_upgrade": True})
            # chrome_options.add_experimental_option("download.default_directory", path_download)
            # chrome_options.add_experimental_option("download.prompt_for_download", False)
            # chrome_options.add_experimental_option("download.directory_upgrade", True)
        navegador = webdriver.Chrome(executable_path=cd, options=chrome_options)
        # service = Service(executable_path=cd)
        # navegador = webdriver.Chrome(service=service, options=chrome_options)

        navegador.maximize_window()
        navegador.get(self.url)

        return navegador

    def __login_siger(self, navegador, user, key):
        """
        Realiza o login no sistema SIGER.

        Parâmetros
        ----------
        navegador : selenium.webdriver.Chrome
            O navegador Chrome inicializado para navegação automatizada.
        user : str
            O nome de usuário para fazer login no sistema SIGER.
        key : str
            A senha associada ao nome de usuário para fazer login no sistema SIGER.

        Retorno
        -------
        None

        Notas
        -----
        Este método automatiza o processo de login no sistema SIGER. Utiliza os elementos HTML da página de login para preencher o nome de usuário e a senha e, em seguida, clica no botão de login.

        Dependências
        ------------
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - webdriver.By: Módulo que contém métodos para localizar elementos por vários meios, como ID, XPath, etc.
        """
        # LOGIN
        username = navegador.find_element(By.ID, "Username")
        password = navegador.find_element(By.ID,"Password")
        username.send_keys(user)
        password.send_keys(key)
        xpath = '/html/body/div[3]/main/section/div/div/div/div[2]/div/div/section/form/div[4]/button'
        navegador.find_element(By.XPATH,xpath).click()

    def __imp_arquivo_siger(self, navegador, file, commentary):
        """
        Realiza a importação de um arquivo no sistema SIGER.

        Parâmetros
        ----------
        navegador : selenium.webdriver.Chrome
            O navegador Chrome inicializado para navegação automatizada.
        file : str
            O caminho completo para o arquivo que será importado no sistema SIGER.
        commentary : str
            Um comentário opcional que será adicionado durante a importação do arquivo.

        Retorno
        -------
        bool
            Retorna True se ocorrer um erro durante a importação do arquivo e False caso contrário.

        Notas
        -----
        Este método automatiza o processo de importação de arquivos no sistema SIGER. Ele navega pela interface do usuário, seleciona a opção de importação, escolhe os parâmetros necessários, seleciona o arquivo a ser importado, adiciona um comentário e, em seguida, submete o formulário para iniciar a importação. Após a importação, verifica se ocorreu algum erro durante o processo.

        Dependências
        ------------
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - webdriver.By: Módulo que contém métodos para localizar elementos por vários meios, como ID, XPath, etc.
        - time.sleep: Função utilizada para pausar a execução por um determinado período de tempo.
        """
        ## Acessando a Importação
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Carimbos
        xpath = '//*[@id="PossuiCarimboData"]'
        navegador.find_element(By.XPATH,xpath).click()
        xpath = '//*[@id="PossuiCarimboEstado"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="ComentarioArquivo"]'
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Clicando em Submeter
        xpath = '//*[@id="submeterbtn"]'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                return True
        ### Checando se deu erro-2!
        xpath = '/html/body/div[3]/div[2]/strong'
        try:
            err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
            if err_msg:
                text_msg = navegador.find_element(By.XPATH,xpath).text
                if text_msg == "Não é possível realizar essa operação, verifique os erros abaixo." or text_msg =='×\nAlgo inesperado aconteceu!':
                    return True
        except:
            pass

        return False

    def __del_arquivo_siger(self, navegador, file, commentary):
        """
        Realiza a exclusão de um arquivo no sistema SIGER.

        Parâmetros
        ----------
        navegador : selenium.webdriver.Chrome
            O navegador Chrome inicializado para navegação automatizada.
        file : str
            O caminho completo para o arquivo que será excluído do sistema SIGER.
        commentary : str
            Um comentário opcional que será adicionado durante a exclusão do arquivo.

        Retorno
        -------
        bool
            Retorna True se ocorrer um erro durante a exclusão do arquivo e False caso contrário.

        Notas
        -----
        Este método automatiza o processo de exclusão de arquivos no sistema SIGER. Ele navega pela interface do usuário, seleciona a opção de exclusão, escolhe os parâmetros necessários, seleciona o arquivo a ser excluído, adiciona um comentário, confirma a exclusão e, em seguida, verifica se ocorreu algum erro durante o processo.

        Dependências
        ------------
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - webdriver.By: Módulo que contém métodos para localizar elementos por vários meios, como ID, XPath, etc.
        - time.sleep: Função utilizada para pausar a execução por um determinado período de tempo.
        """
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="ComentarioArquivo"]'
        navegador.find_element(By.XPATH,xpath).clear()
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Marcando carimbo remoção fisica
        time.sleep(self.delay_prop)
        xpath = '//*[@id="Carga"]/div/div[1]/div[3]/div/div/div/div/div/label[2]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Clicando em Submeter
        xpath = '//*[@id="submeterbtn"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Confirmando
        time.sleep(1)
        xpath = '//*[@id="FormModalConfirmacao"]/div/div[2]/input'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                return True
            else:
                # print(f"Mensagem desconhecida ao passar o arquivo: {file}")
                return False
        else:
            return False

    def __esc_arquivo_siger(self, navegador, file, commentary):
        """
        Realiza a escorregamento de obras no sistema SIGER.

        Parâmetros
        ----------
        navegador : selenium.webdriver.Chrome
            O navegador Chrome inicializado para navegação automatizada.
        file : str
            O caminho completo para o arquivo que será utilizado para o escorregamento de obras no sistema SIGER.
        commentary : str
            Um comentário opcional que será adicionado durante o escorregamento de obras.

        Retorno
        -------
        bool
            Retorna True se ocorrer um erro durante o escorregamento de obras e False caso contrário.

        Notas
        -----
        Este método automatiza o processo de escorregamento de obras no sistema SIGER. Ele navega pela interface do usuário, seleciona a opção de escorregamento de obras, escolhe os parâmetros necessários, seleciona o arquivo a ser utilizado, adiciona um comentário, submete o processo e, em seguida, verifica se ocorreu algum erro durante o processo.

        Dependências
        ------------
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - webdriver.By: Módulo que contém métodos para localizar elementos por vários meios, como ID, XPath, etc.
        - time.sleep: Função utilizada para pausar a execução por um determinado período de tempo.
        """
        ## Acessando a Tela de Escorregamento
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe ESCORREGAMENTO DE OBRAS
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[2]/a'
        navegador.find_element(By.XPATH,xpath).click()
        #
        ## Selecionado opções na Tela de Escorregamento
        ### Marca Opção Possui carimbo de data e obra
        xpath = '//*[@id="PossuiCarimboDataEObra"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="Comentario"]'
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file.replace("\\","/"))
        ### Clicando em Submeter
        xpath = '/html/body/div[3]/main/div/div/form/div/div[2]/button'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                return True
            else:
                # print(f"Mensagem desconhecida ao passar o arquivo: {file}")
                return False
        else:
            return False

    def __zer_arquivo_siger(self, navegador):
        """
        Realiza a exclusão de todos os equipamentos no sistema SIGER.

        Parâmetros
        ----------
        navegador : selenium.webdriver.Chrome
            O navegador Chrome inicializado para navegação automatizada.

        Notas
        -----
        Este método automatiza o processo de exclusão de todos os equipamentos no sistema SIGER. Ele navega pela interface do usuário, seleciona a opção de exclusão de equipamentos, e em seguida, confirma a operação.

        Dependências
        ------------
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - webdriver.By: Módulo que contém métodos para localizar elementos por vários meios, como ID, XPath, etc.
        """
        ## Acessando a Importação
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Apagar Equipamentos
        xpath = '//*[@id="Carga"]/div/form/button'
        navegador.find_element(By.XPATH,xpath).click()

    def __comp_caso_siger(self, navegador, arquivo, data, path_filtro, show_config):
         # Acessando o menu de comparação
        ### Escolhe REDE
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[2]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Comparação de Caso
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[2]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        #
        ## Selecionado opções na Tela de Escorregamento
        ### Marca Opção CONFIGURAÇÕES
        if show_config:
            xpath = '//*[@id="filtro"]/summary'
            navegador.find_element(By.XPATH,xpath).click()
        ### Passando arquivo de filtro
        xpath = '//*[@id="ArquivosFiltro"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(path_filtro)
        ### Clicando em Importar
        xpath = '//*[@id="filtro"]/div[12]/div/input'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Definindo a data
        xpath = '//*[@id="Data"]'
        if isinstance(data, datetime.datetime):
            data_adj = data.strftime('%d/%m/%Y')
        else:
            data_adj = data
        navegador.find_element(By.XPATH,xpath).send_keys(data_adj)
        ### Passando arquivo de comparação
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(arquivo)
        ### Clicando em Importar
        xpath = '/html/body/div[3]/main/div/div/form/div/div[2]/button'
        navegador.find_element(By.XPATH,xpath).click()

    ###================================================================================================================
    ###
    ### CARREGAMENTO DOS ARQUIVOS
    ###
    ###================================================================================================================
    def carrega_siger(self, df_arquivos, cd):
        """
        Realiza o carregamento de arquivos no sistema SIGER.

        Parâmetros
        ----------
        df_arquivos : pandas.DataFrame
            Um DataFrame contendo informações sobre os arquivos a serem carregados no sistema SIGER. Deve conter as colunas "diretorio", "operacao" e "ignorar".

        cd : str
            O caminho para o executável do navegador Chrome.

        Retorno
        -------
        bool
            Retorna True se todos os arquivos foram carregados com sucesso. Retorna False se ocorrer algum erro durante o processo.

        Notas
        -----
        Este método automatiza o processo de carregamento de arquivos no sistema SIGER. Ele inicializa o navegador, faz login no sistema, e realiza as operações de importação, escorregamento, exclusão ou zeramento de arquivos, conforme especificado no DataFrame de entrada.

        O parâmetro "df_arquivos" deve ser um DataFrame com as seguintes colunas:
            - "diretorio": O caminho completo para o arquivo a ser carregado.
            - "operacao": A operação a ser realizada com o arquivo ("imp" para importação, "esc" para escorregamento, "del" para exclusão, "zer" para zeramento).
            - "ignorar": Um indicador (0 ou 1) para indicar se o arquivo deve ser ignorado durante o carregamento.

        Dependências
        ------------
        - pandas.DataFrame: Estrutura de dados para armazenar os dados dos arquivos a serem carregados.
        - selenium.webdriver.Chrome: Classe que representa o navegador Chrome.
        - os.path.basename: Função para obter o nome do arquivo a partir de um caminho completo.
        - self.__inic_navegador: Método interno para inicializar o navegador Chrome.
        - self.__login_siger: Método interno para fazer login no sistema SIGER.
        - self.__imp_arquivo_siger: Método interno para importar arquivos no sistema SIGER.
        - self.__esc_arquivo_siger: Método interno para realizar escorregamento de obras no sistema SIGER.
        - self.__del_arquivo_siger: Método interno para excluir arquivos no sistema SIGER.
        - self.__zer_arquivo_siger: Método interno para zerar equipamentos no sistema SIGER.
        """
        # Parte 1 - Inicializa o navegador
        navegador = self.__inic_navegador(cd)

        # Parte 2 - Faz o login no sistema
        self.__login_siger(navegador, self.user, self.password)

        # Parte 3 - Realiza os carregamentos previstos no df
        for _, row in df_arquivos.iterrows():
            if str(row["ignorar"]) == "0":
                flag_error = True
                nome_arquivo = os.path.basename(row["diretorio"])
                time.sleep(1)

                if row["operacao"] == "imp":
                    flag_error = self.__imp_arquivo_siger(navegador, row["diretorio"], nome_arquivo)

                elif row["operacao"] == "esc":
                    flag_error = self.__esc_arquivo_siger(navegador, row["diretorio"], nome_arquivo)

                elif row["operacao"] == "del":
                    flag_error = self.__del_arquivo_siger(navegador, row["diretorio"], nome_arquivo)

                elif row["operacao"] == "zer":
                    user_confirmation = input("Are you certain? (s/n): ")
                    if user_confirmation.lower() == "s":
                        self.__zer_arquivo_siger(navegador)
                        flag_error = False

                # Verifica erros
                if flag_error:
                    print(f"Erro ao carregar o arquivo {row['diretorio']}! Favor checar")
                    return False

        return True

    def compara_caso_siger(self, path_filtro, path_cd, df_arquivos, path_download):
        # Parte 1 - Inicializa o navegador
        navegador = self.__inic_navegador(path_cd, path_download)

        # Parte 2 - Faz o login no sistema
        self.__login_siger(navegador, self.user, self.password)

        # Parte 3 - Limpa zips do diretório
        arquivos_download = os.listdir(path_download)
        for item in arquivos_download:
            if item.endswith(".zip"):
                os.remove(os.path.join(path_download, item))

        # Parte 4 - Comparação SIGER
        for index, row in df_arquivos.iterrows():
            if str(row["ignorar"]) == "0":
                nome_arquivo = row["diretorio"][row["diretorio"].rfind("/")+1:-4]
                flag_error = True
                if index == 0:
                    flag_error = self.__comp_caso_siger(navegador, row["diretorio"], row["data"], path_filtro, True)
                else:
                    flag_error = self.__comp_caso_siger(navegador, row["diretorio"], row["data"], path_filtro, False)

                # Verifica erros
                if flag_error:
                    print(f"Erro ao comparar o arquivo {row['diretorio']}! Favor checar")
                    return False
                else:
                    # Deixa pasta bonitinha pós comparação
                    time.sleep(3)
                    try:
                        arquivo_zip_original = path_download + "ComparacaoSiger.zip"
                        arquivo_zip_novo = path_download + f"ComparacaoSiger_{nome_arquivo}.zip"
                        # Passo 1 - Renomear arquivo baixado do SIGER
                        os.rename(arquivo_zip_original, arquivo_zip_novo)
                        # Passo 2 - Extrair arquivo zip modificado
                        time.sleep(3)
                        pasta_zip = arquivo_zip_novo.split('.zip')[0]
                        with zipfile.ZipFile(arquivo_zip_novo, 'r') as zip_ref:
                            zip_ref.extractall(pasta_zip)
                    except:
                        pass
        return True
