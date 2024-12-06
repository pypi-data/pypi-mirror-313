import os
import datetime
import pandas as pd
import numpy as np
from win32com.client import DispatchEx
from siger import ImportSIGER

class VerificaSIGER(ImportSIGER):
    """
    Classe que herda funcionalidades de ImportSIGER e adiciona métodos para verificação e comparação de bases do SIGER.

    Principais Métodos:
    --------
    compare_bases_siger(self, path_siger, dic_dfs_1, dic_dfs_2):
        Realiza a comparação entre duas bases do SIGER e gera arquivos Excel com as diferenças encontradas.

    verifica_carregamento(self, path_decks="", df_robras_original=""):
        Analisa o carregamento automático dos 7 arquivos do SIGER e gera um relatório com as verificações realizadas.
    """

    ###================================================================================================================
    ###
    ### CÓDIGOS DE INICIALIZAÇÃO
    ###
    ###================================================================================================================
    def __init__(self, url_siger, usuario, senha):
        """
        Inicializa um objeto da classe com as informações necessárias para acesso ao SIGER.

        Parameters:
        -----------
        url_siger : str
            URL de acesso ao sistema SIGER.
        usuario : str
            Nome de usuário para autenticação no SIGER.
        senha : str
            Senha de usuário para autenticação no SIGER.
        """
        # Pegando todas as funções da Import_SIGER para uso nesse módulo
        super().__init__(url_siger, usuario, senha)

    ###================================================================================================================
    ###
    ### VERIFICAÇÕES PRÉ CARREGAMENTO - DECKS INDIVIDUAIS
    ###
    ###================================================================================================================
    # 01. Verifica erro nas datas
    def __create_dic_erro_data(self, file, df_robras):
        """
        Cria um dicionário de erros relacionados aos dados do arquivo.

        Parameters:
        -----------
        file : str
            Caminho do arquivo contendo os dados a serem verificados.
        df_robras : pandas.DataFrame
            DataFrame contendo os dados das obras do SIGER.

        Returns:
        --------
        list
            Lista de mensagens de erro encontradas durante a validação dos dados.
        """
        errors_file = []
        #
        with open(file, 'r', errors='ignore') as file:
            str_data = file.read()
            list_data = str_data.splitlines()

        # Montando lista com datas no arquivo
        dados_siger_obra = []
        dados_data_siger_obra = []
        dados_estado = ["Pré-Operacional","Carga Inicial","Típico","Como Construído","Acesso","Projeto Básico","Agente Fora da RB"]
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                dados_siger_obra.append(list_data[i][13:])
            elif list_data[i][:13] == "(#SIGER_DATA:":
                dados_data_siger_obra.append(list_data[i][13:].strip())
                if list_data[i+1][:12] != "(#SIGER_EST:":
                    errors_file.append(f"Atenção! Não foi informado o estado da obra {dados_siger_obra[-1]}!")
            elif list_data[i][:12] == "(#SIGER_EST:":
                siger_estado = list_data[i][13:].strip().replace('"','').replace("'","")
                if siger_estado not in dados_estado:
                    errors_file.append(f"Atenção! O estado da obra {dados_siger_obra[-1]} não está preenchido corretamente ({siger_estado})!")

        # Comparando datas com base siger
        if len(dados_siger_obra) == len(dados_data_siger_obra):
            for i in range(len(dados_siger_obra)):
                codigo_obra_arquiv = dados_siger_obra[i].replace('"','')
                #
                # Verificando data em formato errado
                if dados_data_siger_obra[i][:1] == '"':
                    errors_file.append(f"Atenção! A data da obra {codigo_obra_arquiv} está no formato errado! Favor retirar as aspas em: {dados_data_siger_obra[i]}!")

                # Pegando índice de ocorrência
                index_df = df_robras.index[df_robras['Código de Obra']==codigo_obra_arquiv].tolist()

                if len(index_df) > 0:
                    # Data no servidor:
                    data_servidor = df_robras["Data"].iloc[index_df].iloc[0]
                    # Data no arquivo
                    data_arquivo = dados_data_siger_obra[i]
                    #
                    # Comparando datas
                    if data_servidor != data_arquivo:
                        errors_file.append(f"Atenção! A data da obra {codigo_obra_arquiv} foi alterada nesse arquivo de {data_servidor} para {data_arquivo}! Favor concentrar mudanças de datas apenas no arquivo 7!")

        # Comparando cabeçalhos
        return errors_file

    def analyze_datas_from_folder(self, path_decks):
        # Análise deck a deck
        dic_errors = {}
        df_robras = self.get_robras()
        for index, deck in enumerate(path_decks):
            list_error = self.__create_dic_erro_data(deck, df_robras)
            filename = deck[deck.rfind("/")+1:]

            if len(list_error) > 0:
                dic_errors[filename] = list_error

        return dic_errors

    # 02. Verifica erro nos comentários
    def __create_dic_erro_comment(self, file):
        """
        Analisa os dados em cada deck do caminho fornecido e retorna um dicionário de erros.

        Parameters:
        -----------
        path_decks : list
            Lista de caminhos para os decks a serem analisados.

        Returns:
        --------
        dict
            Dicionário onde as chaves são os nomes dos decks e os valores são listas de mensagens de erro encontradas durante a análise.
        """

        errors_file = []
        #
        with open(file, 'r', errors="ignore") as file:
            str_data = file.read()
            list_data = str_data.splitlines()

        # Montando lista com comentários no arquivo
        dados_com = []
        siger_obra = ""
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                if siger_obra == "":
                    siger_obra = list_data[i][13:].strip()
                else:
                    # verifica comentário até então
                    if siger_data_adj > pd.to_datetime("01/10/2023", format="%d/%m/%Y"):
                        if dados_com == "":
                            errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está em branco! Data da obra: {siger_data}")
                        elif len(dados_com) < 11:
                             # Está faltando coisa nos comentários
                            if not siger_obra.upper().replace('"',"").startswith("BASE_"):
                                errors_file.append(f"Atenção! O comentário da obra {siger_obra}, da data {siger_data}, não foi identificado! Favor verificar possível esquecimento!")
                            else:
                                if not any(texto.startswith("(= REGIÃO") for texto in dados_com):
                                    errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente! Não está preenchida/informada a REGIÃO!")
                                if not any(texto.startswith("(= TIPO OBRA") for texto in dados_com):
                                    errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente! Não está preenchida/informada o TIPO OBRA!")

                            # errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente!")
                    # if len(dados_com) < 11:
                    #     # Está faltando coisa nos comentários
                    #     if not siger_obra.upper().replace('"',"").startswith("BASE_"):
                    #         errors_file.append(f"Atenção! O comentário da obra {siger_obra} não foi identificado! Favor verificar possível esquecimento!")
                    # else:
                    #     if not any(texto.startswith("(= REGIÃO") for texto in dados_com):
                    #         errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente! Não está preenchida/informada a REGIÃO!")
                    #     if not any(texto.startswith("(= TIPO OBRA") for texto in dados_com):
                    #         errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente! Não está preenchida/informada o TIPO OBRA!")

                    siger_obra = list_data[i][13:].strip()
                    dados_com = []

            elif list_data[i][:12] == "(#SIGER_COM:":
                dados_com.append(list_data[i][12:])

                if list_data[i].startswith("(#SIGER_COM:(= REGIÃO        :"):
                    regiao_obra = list_data[i].replace("(#SIGER_COM:(= REGIÃO        :","").replace("=)","").strip()
                    if regiao_obra not in ["S+MS", "SECO", "NNE"]:
                        errors_file.append(f"Atenção! A região cadastrada '{regiao_obra}' da obra {siger_obra} é inválida! Favor usar S+MS/SECO/NNE!")

                if ";" in list_data[i]:
                    errors_file.append(f"ERRO! Caracter inválido ';' localizado no campo Comentário da Obra {siger_obra}! Verificar linha:\n {list_data[i]}")
            elif list_data[i][:13] == "(#SIGER_DATA:":
                siger_data = list_data[i][13:].strip()
                siger_data_adj = pd.to_datetime(siger_data, format="%d/%m/%Y")

        # Check final do deck
        # if siger_data_adj > pd.to_datetime("01/10/2023", format="%d/%m/%Y"):
        #     if dados_com == "":
        #         errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está em branco! Data da obra: {siger_data}")
        #     elif len(dados_com) < 11:
        #         errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente!")

        # Comparando cabeçalhos
        return errors_file

    def analyze_comment_from_folder(self, path_decks):
        """
        Analisa comentários de uma pasta contendo vários decks.

        Parâmetros:
        -----------
        path_decks : str
            Caminho para a pasta contendo os decks.

        Retorna:
        --------
        dict
            Um dicionário contendo os erros encontrados nos comentários, indexados pelo nome do arquivo do deck.
        """

        # Análise deck a deck
        dic_errors = {}
        # df_robras = self.get_robras()
        for index, deck in enumerate(path_decks):
            list_error = []
            filename = deck[deck.rfind("/")+1:]
            if filename.startswith("5_") or filename.startswith("6_"):
                list_error = self.__create_dic_erro_comment(deck)

            if len(list_error) > 0:
                dic_errors[filename] = list_error

        return dic_errors

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA COMPARAÇÃO ENTRE BASES DO ARQUIVO 5 e 6
    ###
    ###================================================================================================================
    def download_base_arquivo5(self, path_siger):
        """
        Baixa os arquivos da base de dados 5 do SIGER.

        Parâmetros:
        -----------
        path_siger : str
            Caminho para a pasta onde os arquivos serão salvos.
        """
        dic_dfs = self.get_all_siger_dfs()

        # Salvando arquivos na pasta
        # encoding = "cp1252"
        encoding = "utf-8-sig"
        dic_dfs["barra"].to_csv(path_siger + "/5_barra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cs"].to_csv(path_siger + "/5_cs.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cer"].to_csv(path_siger + "/5_cer.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["linha"].to_csv(path_siger + "/5_linha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["sbarra"].to_csv(path_siger + "/5_sbarra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["slinha"].to_csv(path_siger + "/5_slinha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["trafo"].to_csv(path_siger + "/5_trafo.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["robras"].to_csv(path_siger + "/5_robras.csv", index=False, sep=";", encoding=encoding)
        # dic_dfs["gerador"].to_csv(path_siger + "/5_gerador.csv", index=False, sep=";", encoding=encoding)

        return

    def download_base_arquivo6(self, path_siger):
        """
        Baixa os arquivos da base de dados 6 do SIGER.

        Parâmetros:
        -----------
        path_siger : str
            Caminho para a pasta onde os arquivos serão salvos.
        """
        dic_dfs = self.get_all_siger_dfs()

        # Salvando arquivos na pasta
        # encoding = "cp1252"
        encoding = "utf-8-sig"
        dic_dfs["barra"].to_csv(path_siger + "/6_barra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cs"].to_csv(path_siger + "/6_cs.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cer"].to_csv(path_siger + "/6_cer.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["linha"].to_csv(path_siger + "/6_linha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["sbarra"].to_csv(path_siger + "/6_sbarra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["slinha"].to_csv(path_siger + "/6_slinha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["trafo"].to_csv(path_siger + "/6_trafo.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["robras"].to_csv(path_siger + "/6_robras.csv", index=False, sep=";", encoding=encoding)
        # dic_dfs["gerador"].to_csv(path_siger + "/6_gerador.csv", index=False, sep=";", encoding=encoding)

        return

    def get_code_vba(self):
        """
        Retorna o código VBA para comparar e destacar diferenças em uma tabela.

        Retorna:
        --------
        str
            O código VBA para a macro de comparação.
        """
        vba_code = """
        Sub Macro2()
        '
        ' Macro2 Macro
        '
        '
            Dim table As ListObject
            Dim row As Long, col As Long

            Sheets("Comparacao").Select
            On error resume next
            Set table = ActiveSheet.ListObjects("Table1")
            For row = 1 To table.ListRows.Count
                For col = 1 To table.ListColumns.Count
                    If table.DataBodyRange(row, col) <> table.DataBodyRange(row + 1, col) Then
                        If Mid(table.Range(1, col), 1, 6) = "Estado" Then
                            If table.DataBodyRange(row, col - 1) = 0 And table.DataBodyRange(row + 1, col - 1) = 0 Then
                                table.DataBodyRange(row + 1, col).Interior.ColorIndex = 15
                            ElseIf table.DataBodyRange(row, col - 1) = "" And table.DataBodyRange(row + 1, col - 1) = "" Then
                                table.DataBodyRange(row + 1, col).Interior.ColorIndex = 15
                            Else
                                table.DataBodyRange(row + 1, col).Interior.ColorIndex = 6
                            End If
                        Else
                            table.DataBodyRange(row + 1, col).Interior.ColorIndex = 6
                        End If
                    End If
                Next col
                row = row + 1
            Next row
            On error goto 0
        End Sub
        """
        return vba_code

    def plot_table_excel(self, df, title):
        """
        Plota um dataframe do Pandas em uma planilha do Excel com formatação adicional e executa uma macro VBA para destacar diferenças.

        Parâmetros:
        -----------
        df : pandas.DataFrame
            O dataframe a ser plotado na planilha do Excel.
        title : str
            O título do arquivo Excel que será salvo.

        Nota:
        -----
        Este método pressupõe a existência de uma função `get_code_vba()` na classe que retorna o código VBA necessário para a macro de comparação.
        """

        # Initialize Excel writer
        writer = pd.ExcelWriter(title, engine='xlsxwriter')

        # Write dataframe to excel
        df.to_excel(writer, sheet_name='Comparacao', startrow=1, header=False, index=False)

        # Get worksheet
        worksheet = writer.sheets['Comparacao']

        # Get dataframe shape
        (max_row, max_col) = df.shape

        # Create a list of column headers, to use in add_table()
        column_settings = [{'header': column} for column in df.columns]

        # Add the Excel table structure. Pandas will add the data
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

        # Make the columns wider for clarity
        worksheet.set_column(0, max_col - 1, 12)

        # Save and close the writer
        writer.close()

        # Initialize Excel Application
        xl = DispatchEx("Excel.Application")
        wb = xl.Workbooks.Open(title)

        # Create a new Module and insert the macro code
        vba_code =  self.get_code_vba()
        mod = wb.VBProject.VBComponents.Add(1)
        mod.CodeModule.AddFromString(vba_code)

        # Run the new Macro
        xl.Run("Macro2")

        # Replace .xlsx with .xlsm in the title
        title = title.replace(".xlsx", ".xlsm")
        title = title.replace("/", "\\")

        # Save the workbook and close Excel
        wb.SaveAs(title, FileFormat=52)
        xl.Quit()

    def comp_base_arquivo56(self, path_siger):
        """
        Função avançada para comparar e converter os dataframes das bases de dados 5 e 6 do SIGER em um único dataframe para cada tipo de elemento.

        Parâmetros:
        -----------
        path_siger : str
            Caminho para a pasta onde os arquivos das bases de dados 5 e 6 do SIGER estão localizados.

        Retorna:
        --------
        list
            Uma lista contendo um relatório de comparação para cada tipo de elemento.

        Nota:
        -----
        Este método pressupõe a existência de uma função `plot_table_excel(df, title)` na classe para plotar um dataframe em uma planilha do Excel.
        """
        # encoding = "cp1252"
        encoding = "utf-8-sig"
        dic_dfs = {}
        dic_dfs["barra_5"] = pd.read_csv(path_siger + "/5_barra.csv", sep=";", encoding=encoding).drop(["Conjunto","Fronteira"], axis=1)
        dic_dfs["barra_6"] = pd.read_csv(path_siger + "/6_barra.csv", sep=";", encoding=encoding).drop(["Conjunto","Fronteira"], axis=1)
        dic_dfs["cs_5"] = pd.read_csv(path_siger + "/5_cs.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Disparo","Área"], axis=1)
        dic_dfs["cs_6"] = pd.read_csv(path_siger + "/6_cs.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Disparo","Área"], axis=1)
        dic_dfs["cer_5"] = pd.read_csv(path_siger + "/5_cer.csv", sep=";", encoding=encoding).drop(["Conjunto","Área"], axis=1)
        dic_dfs["cer_6"] = pd.read_csv(path_siger + "/6_cer.csv", sep=";", encoding=encoding).drop(["Conjunto","Área"], axis=1)
        dic_dfs["linha_5"] = pd.read_csv(path_siger + "/5_linha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Reatância (X0 %)","Comprimento (km)","Área","Suscept. (S0 Mvar)", "Terminal De","Estado Terminal De", "Terminal Para", "Estado Terminal Para"], axis=1)
        dic_dfs["linha_6"] = pd.read_csv(path_siger + "/6_linha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Reatância (X0 %)","Comprimento (km)","Área","Suscept. (S0 Mvar)", "Terminal De","Estado Terminal De", "Terminal Para", "Estado Terminal Para"], axis=1)
        dic_dfs["slinha_5"] = pd.read_csv(path_siger + "/5_slinha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Conexão","Resistência Aterramento (%)","Reatância Aterramento (%)","Área"], axis=1)
        dic_dfs["slinha_6"] = pd.read_csv(path_siger + "/6_slinha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Conexão","Resistência Aterramento (%)","Reatância Aterramento (%)","Área"], axis=1)
        dic_dfs["trafo_5"] = pd.read_csv(path_siger + "/5_trafo.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Estado Resistência (R0 %)","Reatância (X0 %)","Estado Reatância (X0 %)","Área","Conexao De","Resistência De","Reatância De","Resistência Para","Reatância Para","Defasamento Conexão","Conexao Para"], axis=1)
        dic_dfs["trafo_6"] = pd.read_csv(path_siger + "/6_trafo.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Estado Resistência (R0 %)","Reatância (X0 %)","Estado Reatância (X0 %)","Área","Conexao De","Resistência De","Reatância De","Resistência Para","Reatância Para","Defasamento Conexão","Conexao Para"], axis=1)
        dic_dfs["sbarra_5"] = pd.read_csv(path_siger + "/5_sbarra.csv", sep=";", encoding=encoding).drop(["Conjunto","Tipo de Conexão","Resistência Seq. Zero (%)","Resistência Aterramento (%)","Reatância Aterramento (%)","Área"], axis=1)
        dic_dfs["sbarra_6"] = pd.read_csv(path_siger + "/6_sbarra.csv", sep=";", encoding=encoding).drop(["Conjunto","Tipo de Conexão","Resistência Seq. Zero (%)","Resistência Aterramento (%)", "Reatância Aterramento (%)","Área"], axis=1)
        # dic_dfs["gerador_5"] = pd.read_csv(path_siger + "/5_gerador.csv", sep=";", encoding=encoding).drop("Conjunto", axis=1)
        # dic_dfs["gerador_6"] = pd.read_csv(path_siger + "/6_gerador.csv", sep=";", encoding=encoding).drop("Conjunto", axis=1)
        dic_dfs["robras_5"] = pd.read_csv(path_siger + "/5_robras.csv", sep=";", encoding=encoding)
        dic_dfs["robras_6"] = pd.read_csv(path_siger + "/6_robras.csv", sep=";", encoding=encoding)
        #
        # Inicia comparação
        dic_dfs["comp_barra"] = self.__generate_df_diffs(dic_dfs["barra_5"], dic_dfs["barra_6"], ['Número', "Código de Obra de Entrada"])
        dic_dfs["comp_cs"] = self.__generate_df_diffs(dic_dfs["cs_5"], dic_dfs["cs_6"], ['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_cer"] = self.__generate_df_diffs(dic_dfs["cer_5"], dic_dfs["cer_6"], ['Número da Barra', "Número", "Código de Obra de Entrada"])
        dic_dfs["comp_linha"] = self.__generate_df_diffs(dic_dfs["linha_5"], dic_dfs["linha_6"], ['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_sbarra"] = self.__generate_df_diffs(dic_dfs["sbarra_5"], dic_dfs["sbarra_6"], ['Número da Barra', "Número", "Código de Obra de Entrada"])
        dic_dfs["comp_slinha"] = self.__generate_df_diffs(dic_dfs["slinha_5"], dic_dfs["slinha_6"], ['Barra De','Barra Para','Número do Circuito', "Número", "Extremidade",  "Código de Obra de Entrada"])
        dic_dfs["comp_trafo"] = self.__generate_df_diffs(dic_dfs["trafo_5"], dic_dfs["trafo_6"], ['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_gerador"] = self.__generate_df_diffs(dic_dfs["gerador_5"], dic_dfs["gerador_6"], ['Número da Barra', 'Número', "Código de Obra de Entrada"])
        dic_dfs["comp_robras"] = self.__generate_df_diffs(dic_dfs["robras_5"], dic_dfs["robras_6"], ['Código de Obra', 'Data', 'Estado', 'Comentário sobre a Obra'])
        #
        # dic_dfs["comp_barra"] = pd.concat([dic_dfs["barra_5"], dic_dfs["barra_6"]]).drop_duplicates(keep=False).sort_values(by=['Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_cs"] = pd.concat([dic_dfs["cs_5"], dic_dfs["cs_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_cer"] = pd.concat([dic_dfs["cer_5"], dic_dfs["cer_6"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', "Número", "Código de Obra de Entrada"])
        # dic_dfs["comp_linha"] = pd.concat([dic_dfs["linha_5"], dic_dfs["linha_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_slinha"] = pd.concat([dic_dfs["slinha_5"], dic_dfs["slinha_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número do Circuito', "Número", "Extremidade",  "Código de Obra de Entrada"])
        # dic_dfs["comp_trafo"] = pd.concat([dic_dfs["trafo_5"], dic_dfs["trafo_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_sbarra"] = pd.concat([dic_dfs["sbarra_5"], dic_dfs["sbarra_6"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', "Número", "Código de Obra de Entrada"])
        #
        # Tratamento devido aos equivalentes
        nomes_equiv = ["EQVDIS", "EQUIV."]
        dic_dfs["comp_sbarra"] = dic_dfs["comp_sbarra"][~dic_dfs["comp_sbarra"]["Nome"].isin(nomes_equiv)]
        dic_dfs["comp_sbarra"] = dic_dfs["comp_sbarra"].drop("Nome", axis=1)
        dic_dfs["comp_sbarra"] = dic_dfs["comp_sbarra"].drop_duplicates(keep=False).reset_index(drop=True)
        #
        # dic_dfs["comp_gerador"] = dic_dfs["comp_gerador"][~dic_dfs["comp_gerador"]["Nome"].isin(nomes_equiv)]
        # dic_dfs["comp_gerador"] = dic_dfs["comp_gerador"].drop("Nome", axis=1)
        # dic_dfs["comp_gerador"] = dic_dfs["comp_gerador"].drop_duplicates(keep=False).reset_index(drop=True)
        #
        # Gera arquivo excel comparação na pasta
        files_siger = os.listdir(path_siger)
        try:
            for item in files_siger:
                if item.endswith(".xlsm") or item.endswith(".xlsx"):
                    os.remove( os.path.join(path_siger, item))
        except:
            pass

        if len(dic_dfs["comp_barra"]) > 0: self.plot_table_excel(dic_dfs["comp_barra"], path_siger + "/comp_barra.xlsx")
        if len(dic_dfs["comp_cs"]) > 0: self.plot_table_excel(dic_dfs["comp_cs"], path_siger + "/comp_cs.xlsx")
        if len(dic_dfs["comp_cer"]) > 0: self.plot_table_excel(dic_dfs["comp_cer"], path_siger + "/comp_cer.xlsx")
        if len(dic_dfs["comp_linha"]) > 0: self.plot_table_excel(dic_dfs["comp_linha"], path_siger + "/comp_linha.xlsx")
        if len(dic_dfs["comp_slinha"]) > 0: self.plot_table_excel(dic_dfs["comp_slinha"], path_siger + "/comp_slinha.xlsx")
        if len(dic_dfs["comp_trafo"]) > 0: self.plot_table_excel(dic_dfs["comp_trafo"], path_siger + "/comp_trafo.xlsx")
        if len(dic_dfs["comp_sbarra"]) > 0: self.plot_table_excel(dic_dfs["comp_sbarra"], path_siger + "/comp_sbarra.xlsx")
        # if len(dic_dfs["comp_gerador"]) > 0: self.plot_table_excel(dic_dfs["comp_gerador"], path_siger + "/comp_gerador.xlsx")
        if len(dic_dfs["comp_robras"]) > 0: self.plot_table_excel(dic_dfs["comp_robras"], path_siger + "/comp_robras.xlsx")

        files_siger = os.listdir(path_siger)
        for item in files_siger:
            if item.endswith(".xlsx"):
                os.remove( os.path.join(path_siger, item))

        list_report = []
        list_report.append("Relatório de Comparação: \n")
        list_report.append("Comparação BARRA: VERIFICAR!" if len(dic_dfs["comp_barra"]) > 0 else "Comparação BARRA: OK!")
        list_report.append("Comparação CS: VERIFICAR!" if len(dic_dfs["comp_cs"]) > 0 else "Comparação CS: OK!")
        list_report.append("Comparação CER: VERIFICAR!" if len(dic_dfs["comp_cer"]) > 0 else "Comparação CER: OK!")
        list_report.append("Comparação LINHA: VERIFICAR!" if len(dic_dfs["comp_linha"]) > 0 else "Comparação LINHA: OK!")
        list_report.append("Comparação SHUNT_LINHA: VERIFICAR!" if len(dic_dfs["comp_slinha"]) > 0 else "Comparação SHUNT_LINHA: OK!")
        list_report.append("Comparação TRANSFORMADOR: VERIFICAR!" if len(dic_dfs["comp_trafo"]) > 0 else "Comparação TRANSFORMADOR: OK!")
        list_report.append("Comparação SHUNT_BARRA: VERIFICAR!" if len(dic_dfs["comp_sbarra"]) > 0 else "Comparação SHUNT_BARRA: OK!")
        # list_report.append("Comparação GERADOR: VERIFICAR!" if len(dic_dfs["comp_gerador"]) > 0 else "Comparação GERADOR: OK!")
        list_report.append("Comparação RELATÓRIO_OBRAS: VERIFICAR!" if len(dic_dfs["comp_robras"]) > 0 else "Comparação RELATÓRIO_OBRAS: OK!")

        return list_report

    ###================================================================================================================
    ###
    ### VERIFICAÇÕES PÓS CARREGAMENTO - INDIVIDUAIS
    ###
    ###================================================================================================================
    # 01. Conjuntos exclusivos
    def __aux_check_exclusives(self, dic_dfs):
        """
        Função auxiliar para verificar equipamentos exclusivos que possuem conjunto diferente de 'Anafas e Anarede' em cada dataframe.

        Parâmetros:
        -----------
        dic_dfs : dict
            Um dicionário contendo dataframes para cada tipo de equipamento.

        Retorna:
        --------
        str
            Uma mensagem indicando os equipamentos exclusivos encontrados ou informando que nenhum foi encontrado.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        list_errors = []
        if len(dic_dfs["barra"][dic_dfs["barra"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Barra")
        if len(dic_dfs["cs"][dic_dfs["cs"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Compensador Série")
        if len(dic_dfs["cer"][dic_dfs["cer"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Compensador Estático")
        if len(dic_dfs["linha"][dic_dfs["linha"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Linha")
        if len(dic_dfs["slinha"][dic_dfs["slinha"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Shunt Linha")
        if len(dic_dfs["trafo"][dic_dfs["trafo"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Transformador")
        #
        # SHUNT DE BARRA é um caso a parte
        if len(dic_dfs["sbarra"][dic_dfs["sbarra"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            flag_sb = False
            # Check 1 - Se existir Shunt só no ANAREDE é erro!
            if len(dic_dfs["sbarra"][dic_dfs["sbarra"]["Conjunto"] == "Anarede"]) > 0:
                list_errors.append("Shunt Barra - FP (atenção!)")
            if len(dic_dfs["sbarra"][dic_dfs["sbarra"]["Conjunto"] == "Anafas"]) > 0:
                list_errors.append("Shunt Barra - CC (esperado!)")

        if len(list_errors) > 0:
            #
            equips = " / ".join(list_errors)
            str_exclusivo = f"Os seguintes equipamentos possuem conjunto diferente de 'Anafas e Anarede': {equips}."
        else:
            str_exclusivo = "Não foram encontrados equipamentos que possuem conjunto diferente de 'Anafas e Anarede'"
        #
        return str_exclusivo

    def check_exclusives(self):
        """
        Função avançada para verificar equipamentos exclusivos que possuem conjunto diferente de 'Anafas e Anarede' em cada dataframe.

        Retorna:
        --------
        str
            Uma mensagem indicando os equipamentos exclusivos encontrados ou informando que nenhum foi encontrado.

        Nota:
        -----
        Este método pressupõe a existência de uma função `__aux_check_exclusives(dic_dfs)` na classe para realizar a verificação interna.
        """

        dic_dfs = self.get_all_siger_dfs()
        str_exclusivo = self.__aux_check_exclusives(dic_dfs)

        return str_exclusivo

    # 02. Estados Múltiplos
    def __aux_check_estados_multiplos(self, df, df_siger):
        """
        Função auxiliar para filtrar o dataframe do SIGER com base em condições específicas.

        Parâmetros:
        -----------
        df : pandas.DataFrame
            O dataframe a ser filtrado.
        df_siger : pandas.DataFrame
            O dataframe do SIGER a ser filtrado.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe do SIGER filtrado de acordo com as condições especificadas.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        condicao = ["Como Construído", "Acesso", "Carga Inicial", "Típico", "Pré-Operacional", "Projeto Básico", "Agente Fora da RB"]
        df = df[~df['Estado'].isin(condicao)]
        df = df[~df["Código de Obra de Entrada"].str.startswith("BASE_")]
        list_obras = df["Código de Obra de Entrada"].to_list()
        df_filtrado = df_siger[df_siger["Código de Obra de Entrada"].isin(list_obras)]
        df_filtrado = df_filtrado.sort_values(by='Código de Obra de Entrada', ascending=False)

        return df_filtrado

    def check_estados_multiplos(self):
        """
        Função avançada para verificar e filtrar os estados múltiplos em um dataframe do SIGER.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe do SIGER filtrado com base nos estados múltiplos.

        Nota:
        -----
        Este método pressupõe a existência de uma função `__aux_check_estados_multiplos(df, df_siger)` na classe para realizar a verificação interna.
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_estado_mult = self.__aux_check_estados_multiplos(df_agg, df_siger)

        return df_estado_mult

    # 03. Datas múltiplas
    def __aux_check_datas_multiplas(self, df):
        """
        Função auxiliar para verificar duplicatas de datas em um dataframe.

        Parâmetros:
        -----------
        df : pandas.DataFrame
            O dataframe a ser verificado.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe contendo apenas as duplicatas de datas.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        df = df[df['Código de Obra de Entrada'].duplicated()]
        df = df[~df['Código de Obra de Entrada'].str.startswith('BASE_')]

        return df

    def check_datas_multiplas(self):
        """
        Função avançada para verificar e retornar duplicatas de datas em um dataframe do SIGER.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe contendo apenas as duplicatas de datas.

        Nota:
        -----
        Este método pressupõe a existência de uma função `__aux_check_datas_multiplas(df)` na classe para realizar a verificação interna.
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_data_mult = self.__aux_check_datas_multiplas(df_agg)

        return df_data_mult

    # 04. Estados Defasados
    def __aux_check_estados_defasados(self, df_agg):
        """
        Função auxiliar para verificar e retornar estados defasados em um dataframe agregado.

        Parâmetros:
        -----------
        df_agg : pandas.DataFrame
            O dataframe agregado a ser verificado.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe contendo apenas os estados defasados.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        current_datetime = datetime.datetime.now()
        day = current_datetime.day
        month = current_datetime.month
        year = current_datetime.year
        today = f"{day:02d}-{month:02d}-{year}"
        df_past = df_agg.copy()
        df_past['Data de Entrada'] = pd.to_datetime(df_past['Data de Entrada'])
        df_past = df_past[df_past['Data de Entrada'] < current_datetime]
        df_past = df_past[~df_past["Código de Obra de Entrada"].str.startswith("BASE_")]
        condicao = ["Como Construído", "Pré-Operacional", "Agente Fora da RB"]
        df_past = df_past[~df_past['Estado'].isin(condicao)]
        df_past = df_past.sort_values(by='Data de Entrada')

        return df_past

    def check_estados_defasados(self):
        """
        Função avançada para verificar e retornar estados defasados em um dataframe do SIGER.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe contendo apenas os estados defasados.

        Nota:
        -----
        Este método pressupõe a existência de uma função `__aux_check_estados_defasados(df_agg)` na classe para realizar a verificação interna.
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_estado_def = self.__aux_check_estados_defasados(df_agg)

        return df_estado_def

    # 05. Nomes repetidos
    def __aux_check_nome_repetidos(self, df_agg):
        """
        Função auxiliar para verificar e retornar nomes de equipamentos repetidos em um dataframe agregado.

        Parâmetros:
        -----------
        df_agg : pandas.DataFrame
            O dataframe agregado a ser verificado.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe contendo apenas os nomes de equipamentos repetidos.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        df_bar = df_agg[["Número", "Nome"]]
        df_bar_dup = df_bar[df_bar.duplicated(subset='Nome', keep=False)].sort_values(by='Número')
        df_bar_uniq = df_bar_dup.drop_duplicates(keep=False).sort_values(by='Nome')
        exceptions = ["NIGUT6-RJ000","NIGUT6-RJ013","NIGUT8-RJ000","NIGUT8-RJ013"]
        df_bar_uniq = df_bar_uniq[~df_bar_uniq['Nome'].isin(exceptions)]

        return df_bar_uniq

    def check_nome_repetidos(self):
        """
        Função avançada para verificar e retornar nomes de equipamentos repetidos em um dataframe do SIGER.

        Retorna:
        --------
        pandas.DataFrame
            Um novo dataframe contendo apenas os nomes de equipamentos repetidos.

        Nota:
        -----
        Este método pressupõe a existência de uma função `__aux_check_nome_repetidos(df_agg)` na classe para realizar a verificação interna.
        """

        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_nom_rep = self.__aux_check_nome_repetidos(df_agg)

        return df_nom_rep

    # 06. Checagem nos comentários
    def __analisa_comentarios_siger(self, dic_decks):
        """
        Função auxiliar para analisar comentários do SIGER e identificar possíveis erros.

        Parâmetros:
        -----------
        dic_decks : dict
            Um dicionário contendo códigos de obra como chaves e comentários do SIGER como valores.

        Retorna:
        --------
        dict
            Um dicionário contendo listas de códigos de obra associados a diferentes tipos de erro nos comentários.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        # Inicializa dicionário para capturar erros
        dic_erro_coment = {"obras_sem_com_empreendedimento": [], "obras_sem_com_tipo_obra": [], "obras_sem_com_regiao": [],
                           "obras_com_vaz_empreendedimento": [], "obras_com_vaz_tipo_obra": [], "obras_com_vaz_regiao": [],
                           "obras_com_erro_tipo": [], "obras_com_erro_regiao": []}

        # Verificação dos erros
        for index, (codigo_obra, comentario) in enumerate(dic_decks.items()):
            # Verifica se não tem comentário
            if isinstance(comentario,float):
                comentario = ""

            if ("(= EMPREENDIMENTO" not in comentario):
                dic_erro_coment["obras_sem_com_empreendedimento"].append(codigo_obra)

            if ("(= TIPO OBRA" not in comentario):
                dic_erro_coment["obras_sem_com_tipo_obra"].append(codigo_obra)

            if ("(= REGIÃO" not in comentario):
                dic_erro_coment["obras_sem_com_regiao"].append(codigo_obra)

            # Verifica empreendimento
            if ("(= EMPREENDIMENTO:                                                                                               =)" in comentario):
                dic_erro_coment["obras_com_vaz_empreendedimento"].append(codigo_obra)

            # # Verifica região
            if ("(= REGIÃO        :                                                                                               =)" in comentario):
                dic_erro_coment["obras_com_vaz_regiao"].append(codigo_obra)

            # Verifica tipo obra
            if ("(= TIPO OBRA     :                                                                                               =)" in comentario):
                dic_erro_coment["obras_com_vaz_tipo_obra"].append(codigo_obra)

            # Coletando dado inserido no campo Tipo Obra
            if comentario.find("(= TIPO OBRA") > 0:
                start_string = comentario.find("(= TIPO OBRA")
                end_string = comentario.find("\r\n", start_string+2)
                tipo_obra = comentario[start_string+12:end_string-2].replace(":","").strip()

                if tipo_obra not in ["TRANSMISSÃO", "TRANSMISSÃO (DIT)", "CONSUMIDOR", "GERAÇÃO - UHE","GERAÇÃO - UTE","GERAÇÃO - UEE","GERAÇÃO - UFV","GERAÇÃO - PCH","DISTRIBUIÇÃO COM IMPACTO SISTÊMICO"]:
                    dic_erro_coment["obras_com_erro_tipo"].append(codigo_obra)

            # Coletando dado inserido no campo Região
            if comentario.find("(= REGIÃO        :") > 0:
                start_string = comentario[comentario.find("(= REGIÃO        :"):]
                end_string = start_string[:start_string.find("\n")].strip()
                regiao = (end_string.replace("(= REGIÃO        :","")).replace("=)","").strip()
                if regiao not in ["S+MS","SECO","NNE"]:
                    dic_erro_coment["obras_com_erro_regiao"].append(codigo_obra)

        return dic_erro_coment

    def __aux_check_comentarios(self, df_robras):
        """
        Função auxiliar para verificar e analisar comentários presentes nos registros de obras do SIGER.

        Parâmetros:
        -----------
        df_robras : DataFrame
            Um DataFrame contendo registros de obras do SIGER.

        Retorna:
        --------
        str
            Uma string contendo um relatório da análise dos comentários dos registros de obras do SIGER.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        # Coletando dicionário com erros nos comentários
        # df_robras = oSIGER.get_robras()
        df_robras['Data'] = pd.to_datetime(df_robras['Data'], format='%d/%m/%Y')
        df_robras = df_robras[df_robras['Data'] >= '2023-10-01']
        dic_decks = df_robras.set_index('Código de Obra')['Comentário sobre a Obra'].to_dict()
        #
        dic_erro_coment = self.__analisa_comentarios_siger(dic_decks)

        # Imprimindo na tela os resultados
        list_report = []
        list_report.append("Análise sobre o campo COMENTÁRIO presente no servidor siger selecionado:\n")
        list_report.append(f"Foram analisados {len(dic_decks)} códigos de obra presentes no servidor, com data de entrada igual ou superior a 01/10/2023. \nSeguem resultados: \n")
        len_errors = sum(len(lst) for lst in dic_erro_coment.values())

        if len_errors == 0:
            list_report.append("- Análise concluída com sucesso sem erros aparentes!")
        else:
            if len(dic_erro_coment["obras_sem_com_empreendedimento"]) > 0:
                list_report.append("- Verificar falta das informações de 'EMPREENDIMENTO' do cabeçalho padrão dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_sem_com_empreendedimento"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_sem_com_regiao"]) > 0:
                list_report.append("- Verificar falta das informações de 'REGIÃO' do cabeçalho padrão dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_sem_com_regiao"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_sem_com_tipo_obra"]) > 0:
                list_report.append("- Verificar falta das informações de 'TIPO OBRA' do cabeçalho padrão dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_sem_com_tipo_obra"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_vaz_empreendedimento"]) > 0:
                list_report.append("- Verificar falta de preenchimento do campo COMENTÁRIO - EMPREENDIMENTO dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_com_vaz_empreendedimento"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_vaz_tipo_obra"]) > 0:
                list_report.append("- Verificar falta de preenchimento do campo COMENTÁRIO - TIPO OBRA dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_com_vaz_tipo_obra"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_vaz_regiao"]) > 0:
                list_report.append("- Verificar falta de preenchimento do campo COMENTÁRIO - REGIÃO dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_com_vaz_regiao"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_erro_tipo"]) > 0:
                list_report.append("- Verificar erro de preenchimento no campo TIPO OBRA dos seguintes códigos de obra. Lembrando que são apenas válidos os seguintes valores ['TRANSMISSÃO','GERAÇÃO - UHE','GERAÇÃO - UTE','GERAÇÃO - UEE','GERAÇÃO - UFV','GERAÇÃO - PCH','DISTRIBUIÇÃO COM IMPACTO SISTÊMICO']:")
                list_report.append("\n".join(dic_erro_coment["obras_com_erro_tipo"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_erro_regiao"]) > 0:
                list_report.append("- Verificar erro de preenchimento no campo REGIÃO dos seguintes códigos de obra. Lembrando que são apenas válidos os seguintes valores ['S+MS','SECO','NNE']:")
                list_report.append("\n".join(dic_erro_coment["obras_com_erro_regiao"]))
                list_report.append("\n")

        return "\n".join(list_report)

    def check_comentarios(self):
        """
        Função para verificar e analisar comentários presentes nos registros de obras do SIGER.

        Retorna um relatório da análise dos comentários dos registros de obras do SIGER.

        Retorna:
        --------
        str
            Uma string contendo um relatório da análise dos comentários dos registros de obras do SIGER.
        """
        # df_robras_mod, dic_dfs = self.get_all_siger_dfs()
        df_robras = self.get_robras()

        str_comentarios = self.__aux_check_comentarios(df_robras)

        return str_comentarios

    # 07. Verifica escorregamento em cascata
    def __check_change_date(self, data_antes, data_depois):
        """
        Função para verificar se houve alteração entre duas datas.

        Parâmetros:
        -----------
        data_antes : str
            Data antes da alteração no formato 'dd/mm/aaaa'.
        data_depois : str
            Data depois da alteração no formato 'dd/mm/aaaa'.

        Retorna:
        --------
        str
            Retorna 'S' se houve alteração entre as datas, caso contrário retorna 'N'.
        """
        if data_antes == data_depois:
            id = "N"
        else:
            id = "S"
        return id

    def check_escorreg_cascata(self, df_robras_antes, df_robras_depois, file_7):
        """
        Função para verificar se houve alterações nas datas das obras entre dois dataframes e em relação a um arquivo.

        Parâmetros:
        -----------
        df_robras_antes : pandas.DataFrame
            DataFrame contendo as informações das obras antes da alteração.
        df_robras_depois : pandas.DataFrame
            DataFrame contendo as informações das obras depois da alteração.
        file_7 : str
            Caminho do arquivo 7.

        Retorna:
        --------
        pandas.DataFrame
            DataFrame contendo as obras que tiveram alterações de data entre os dataframes e em relação ao arquivo 7.
        """
        df_robras_antes = df_robras_antes.rename(columns={"Data": "Data_antes"})
        df_robras_depois = df_robras_depois.rename(columns={"Data": "Data_depois"})
        df_robras_antes['Data_antes'] = pd.to_datetime(df_robras_antes['Data_antes'], format='%d/%m/%Y')
        df_robras_depois['Data_depois'] = pd.to_datetime(df_robras_depois['Data_depois'], format='%Y-%m-%d')
        df_merged = df_robras_antes.merge(df_robras_depois, on=['Código de Obra'], how='inner')
        #
        df_merged["Alterou_Data"] = np.vectorize(self.__check_change_date)(df_merged["Data_antes"], df_merged["Data_depois"])
        df_data_alterada = df_merged[df_merged["Alterou_Data"] == "S"]
        df_data_alterada = df_data_alterada[["Código de Obra", "Data_antes", "Data_depois"]]
        #
        # Levantamento de datas no arquivo 7
        lista_obras_files = []
        lista_datas_files = []
        with open(file_7, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"")
                lista_obras_files.append(siger_obra)
            if list_data[i][:12] == "(#SIGER_ESC:":
                siger_data = list_data[i][12:].replace('"',"")
                lista_datas_files.append(siger_data)
        list_file_7 = [lista_obras_files, lista_datas_files]
        list_file_7 = list(map(list, zip(*list_file_7)))
        df_file7 = pd.DataFrame(list_file_7, columns=['Código de Obra', 'Data_Arquivo_7'])
        df_file7['Data_Arquivo_7'] = pd.to_datetime(df_file7['Data_Arquivo_7'], format='%d/%m/%Y')
        #
        df_data_alterada_file7 = df_data_alterada.merge(df_file7, on=['Código de Obra'], how='inner')
        if len(df_data_alterada_file7) > 0:
            df_data_alterada_file7["Alterou_Data_Arqv7"] = np.vectorize(self.__check_change_date)(df_data_alterada_file7["Data_depois"], df_data_alterada_file7["Data_Arquivo_7"])
            df_data_alterada_file7_mod = df_data_alterada_file7[df_data_alterada_file7["Alterou_Data_Arqv7"] == "S"]
        else:
            df_data_alterada_file7_mod = df_data_alterada_file7.copy()

        return df_data_alterada_file7_mod

    # 08. Verifica apagamento em cascata
    def check_apagamento_cascata(self, df_robras_antes, df_robras_depois, file_1, file_4):
        """
        Função para verificar se houve apagamento em cascata de obras entre dois conjuntos de dados e em relação a dois arquivos.

        Parâmetros:
        -----------
        df_robras_antes : pandas.DataFrame
            DataFrame contendo as informações das obras antes do apagamento.
        df_robras_depois : pandas.DataFrame
            DataFrame contendo as informações das obras depois do apagamento.
        file_1 : str
            Caminho do arquivo 1.
        file_4 : str
            Caminho do arquivo 4.

        Retorna:
        --------
        list
            Lista contendo os códigos de obra que foram apagados em cascata.
        """
        lista_obras_antes = list(df_robras_antes["Código de Obra"].values)
        lista_obras_depois = list(df_robras_depois["Código de Obra"].values)
        lista_obras_removidas = list(set(lista_obras_antes) - set(lista_obras_depois))
        #
        # Buscar nos arquivos 1 e 4 as obras removidas
        lista_obras_files = []
        with open(file_1, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"").strip()
                lista_obras_files.append(siger_obra)
        with open(file_4, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:20] == "(#SIGER_REMOVE_OBRA:":
                siger_obra = list_data[i][20:].replace('"',"").strip()
                if siger_obra != "REMOVE-1":
                    lista_obras_files.append(siger_obra)

        # Compara Arquivos
        lista_obras_removidas_cascata = [x for x in lista_obras_removidas if x not in lista_obras_files]

        return lista_obras_removidas_cascata

    # 09. Verifica obras não presentes no banco, mas que estavam no 5 e 6
    def check_obras_nao_presentes(self, df_robras_depois, file_5, file_6):
        """
        Função para verificar se há obras presentes nos arquivos 5 e 6 que não estão presentes no DataFrame de obras depois do processamento.

        Parâmetros:
        -----------
        df_robras_depois : pandas.DataFrame
            DataFrame contendo as informações das obras depois do processamento.
        file_5 : str
            Caminho do arquivo 5.
        file_6 : str
            Caminho do arquivo 6.

        Retorna:
        --------
        list
            Lista contendo os códigos de obra que estão presentes nos arquivos 5 e 6, mas não estão no DataFrame de obras depois do processamento.
        """
        lista_obras_depois = list(df_robras_depois["Código de Obra"].values)
        #
        # Buscar nos arquivos 1 e 4 as obras removidas
        lista_obras_files = []
        with open(file_5, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"").strip()
                lista_obras_files.append(siger_obra)

        with open(file_6, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"").strip()
                lista_obras_files.append(siger_obra)

        # Juntar listas
        lista_obras_files = list(set(lista_obras_files))
        list_missing_obras = [element for element in lista_obras_files if element.upper() not in lista_obras_depois]

        return list_missing_obras

    ###================================================================================================================
    ###
    ### VERIFICAÇÃO GERAL PÓS CARREGAMENTO
    ###
    ###================================================================================================================
    def verifica_carregamento(self, path_decks="", df_robras_original = ""): #carrega_7_arquivos_gui_pt2
        """
        Analisa o carregamento dos 7 arquivos.

        Parâmetros:
        -----------
        path_decks : str, opcional
            Caminho da pasta contendo os 7 arquivos. (default é "")
        df_robras_original : pandas.DataFrame, opcional
            DataFrame contendo as informações das obras antes do processamento. (default é "")

        Retorna:
        --------
        str
            Relatório contendo as análises realizadas sobre o carregamento dos 7 arquivos.
        """
        # Finalizada a execução do carregamento, verificar o resultado obtido
        dic_dfs = self.get_all_siger_dfs()
        df_robras_mod = dic_dfs["robras"]
        df_siger = self._make_siger_base(dic_dfs)
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        # PARTE 1 - CHECAR CONJUNTO EXCLUSIVO
        str_exclusivo = self.__aux_check_exclusives(dic_dfs)
        #
        # PARTE 2 - CHECAR ESTADOS MÚLTIPLOS
        df_estado_mult = self.__aux_check_estados_multiplos(df_agg, df_siger)
        #
        # PARTE 3 - CHECAR DATAS MÚLTIPLAS
        df_data_mult = self.__aux_check_datas_multiplas(df_agg)
        #
        # PARTE 4 - CHECAR ESTADOS DEFASADOS
        df_estado_def = self.__aux_check_estados_defasados(df_agg)

        # PARTE 5 - CHECAR NOMES DE BARRAS REPETIDAS
        df_barra_nome_repet = self.__aux_check_nome_repetidos(dic_dfs["barra"])

        # PARTE 6 - CHECAGEM COMENTÁRIOS
        str_comentarios = self.__aux_check_comentarios(df_robras_mod)

        # Crie um arquivo de texto para escrever o relatório
        report = []
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report.append("\n" + "#"*88 + "\n")
        report.append(f"# RELATÓRIO DE CARREGAMENTO SIGER - {data_hora}\n\n")

        # Escreva a variável string no arquivo
        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 01 - CONJUNTOS EXCLUSIVOS\n")
        report.append(f"{str_exclusivo}\n\n")

        # Escreva os DataFrames no arquivo
        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 02 - ESTADOS MÚLTIPLOS\n")
        df_estado_mult_mod = df_estado_mult.copy()
        df_estado_mult_mod['Data de Entrada'] = pd.to_datetime(df_estado_mult_mod['Data de Entrada']).dt.strftime('%d/%m/%Y')
        df_estado_mult_mod['Data de Saída'] = pd.to_datetime(df_estado_mult_mod['Data de Saída']).dt.strftime('%d/%m/%Y')
        if len(df_estado_mult_mod) > 0:
            report.append(df_estado_mult_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS OBRAS COM ESTADOS MÚLTIPLOS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 03 - DATAS MÚLTIPLAS\n")
        df_data_mult_mod = df_data_mult.copy()
        df_data_mult_mod['Data de Entrada'] = pd.to_datetime(df_data_mult_mod['Data de Entrada']).dt.strftime('%d/%m/%Y')
        if len(df_data_mult_mod) > 0:
            report.append(df_data_mult_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS OBRAS COM DATAS MÚLTIPLAS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 04 - ESTADOS DEFASADOS\n")
        df_estado_def_mod = df_estado_def.copy()
        df_estado_def_mod['Data de Entrada'] = pd.to_datetime(df_estado_def_mod['Data de Entrada']).dt.strftime('%d/%m/%Y')
        if len(df_estado_def_mod) > 0:
            report.append(df_estado_def_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS OBRAS COM ESTADOS DEFASADOS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 05 - BARRAS COM NOMES REPETIDOS\n")
        df_barra_nome_repet_mod = df_barra_nome_repet.copy()
        if len(df_barra_nome_repet_mod) > 0:
            report.append(df_barra_nome_repet_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS BARRAS COM NOMES REPETIDOS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 06 - PREENCHIMENTO COMENTÁRIOS\n")
        report.append(f"{str_comentarios}\n\n")

        # Coleta lista de decks presentes na pasta
        if path_decks != "":
            decks_siger = []
            for filename in os.listdir(path_decks):
                if filename.endswith(('.pwf', '.alt')) or filename.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_')):
                    decks_siger.append(os.path.join(path_decks, filename))

            # Verifica se estamos com os 7 arquivos para conseguir prosseguir:
            if len(decks_siger) == 7:
                # PARTE 5 - VERIFICAR ESCORREGAMENTOS EM CASCATA
                df_obras_escorregadas_cascata = self.check_escorreg_cascata(df_robras_original, df_robras_mod, decks_siger[6])
                #
                # PARTE 6 - VERIFICAR EXCLUSÕES EM CASCATA
                lista_obras_removidas_cascata = self.check_apagamento_cascata(df_robras_original, df_robras_mod, decks_siger[0], decks_siger[3])

                # PARTE 7 - VERIFICAR FALSAS INCLUSÕES NA BASE
                lista_obras_falso_positivo = self.check_obras_nao_presentes(df_robras_mod, decks_siger[4], decks_siger[5])

                report.append("#"*88 + "\n")
                report.append("# CHECAGEM 07 - OBRAS ESCORREGADAS EM CASCATA\n")
                df_obras_escorregadas_cascata_mod = df_obras_escorregadas_cascata.copy()
                df_obras_escorregadas_cascata_mod['Data_antes'] = pd.to_datetime(df_obras_escorregadas_cascata_mod['Data_antes']).dt.strftime('%d/%m/%Y')
                df_obras_escorregadas_cascata_mod['Data_depois'] = pd.to_datetime(df_obras_escorregadas_cascata_mod['Data_depois']).dt.strftime('%d/%m/%Y')
                df_obras_escorregadas_cascata_mod['Data_Arquivo_7'] = pd.to_datetime(df_obras_escorregadas_cascata_mod['Data_Arquivo_7']).dt.strftime('%d/%m/%Y')
                if len(df_obras_escorregadas_cascata_mod) > 0:
                    report.append(df_obras_escorregadas_cascata_mod.to_string(index=False) + '\n\n')
                else:
                    report.append(" NÃO FORAM ENCONTRADAS OBRAS ESCORREGADAS EM CASCATA!\n")

                report.append("#"*88 + "\n")
                report.append("# CHECAGEM 08 - OBRAS APAGADAS EM CASCATA\n")
                if len(lista_obras_removidas_cascata) > 0:
                    report.append("\n".join(lista_obras_removidas_cascata) + '\n\n')
                else:
                    report.append(" NÃO FORAM ENCONTRADAS OBRAS APAGADAS EM CASCATA!\n")

                report.append("#"*88 + "\n")
                report.append("# CHECAGEM 09 - OBRAS PRESENTES NOS ARQUIVOS 5/6 MAS NÃO INCLUÍDAS NO BANCO\n")
                if len(lista_obras_falso_positivo) > 0:
                    report.append("\n".join(lista_obras_falso_positivo) + '\n\n')
                else:
                    report.append(" NÃO FORAM ENCONTRADAS OBRAS PRESENTES NOS ARQUIVOS 5/6 MAS NÃO INCLUÍDAS NO BANCO!\n")
            else:
                print("Não foi possível localizar os 7 arquivos na pasta informada! Favor conferir se os decks estão na pasta ou se há mais decks que os 7 a serem analisados!")

        str_report = "\n".join(report)
        return str_report

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA COMPARAÇÃO ENTRE DUAS BASES (URLs)
    ###
    ###================================================================================================================
    def __generate_df_diffs(self, df1, df2, list_sort):
        """
        Função auxiliar para montar dataframe comparado.

        Parâmetros:
        -----------
        df1, df2 : Pandas DataFrame
            DataFrames a serem comparados.

        Retorna:
        --------
        df1_comp
            DataFrame com as diferenças.

        Nota:
        -----
        Este método é uma função interna e não deve ser chamado diretamente fora da classe.
        """
        df_comp = pd.concat([df1, df2]).drop_duplicates(keep=False).reset_index(drop=True).reset_index()
        df_comp = df_comp.sort_values(by=list_sort + ["index"])
        df_comp = df_comp.drop(columns=["index"])

        return df_comp

    def compare_bases_siger(self, path_siger, dic_dfs_1, dic_dfs_2):
        """
        Realiza a comparação entre duas bases do SIGER e gera arquivos Excel com as diferenças encontradas.

        Parâmetros:
        -----------
        path_siger : str
            Caminho da pasta onde serão armazenados os arquivos Excel gerados.
        dic_dfs_1 : dict
            Dicionário contendo os DataFrames da primeira base do SIGER.
        dic_dfs_2 : dict
            Dicionário contendo os DataFrames da segunda base do SIGER.

        Retorna:
        --------
        str
            Relatório contendo as diferenças encontradas entre as bases.
        """
        print("PASSO 01 - REALIZANDO COMPARAÇÕES DOS CSVs...")
        dic_dfs = {}
        dic_dfs["comp_robras"] = self.__generate_df_diffs(dic_dfs_1["robras"], dic_dfs_2["robras"], ["Código de Obra"])
        dic_dfs["comp_area"] = self.__generate_df_diffs(dic_dfs_1["area"], dic_dfs_2["area"], ["Número"])
        dic_dfs["comp_glt"] = self.__generate_df_diffs(dic_dfs_1["glt"], dic_dfs_2["glt"], ["Grupo"])
        dic_dfs["comp_gbt"] = self.__generate_df_diffs(dic_dfs_1["gbt"], dic_dfs_2["gbt"], ["Grupo"])
        #
        dic_dfs["comp_barra"] = self.__generate_df_diffs(dic_dfs_1["barra"].drop(columns=["Identificação"]), dic_dfs_2["barra"].drop(columns=["Identificação"]), ['Número', "Código de Obra de Entrada"])
        dic_dfs["comp_cs"] = self.__generate_df_diffs(dic_dfs_1["cs"].drop(columns=["Identificação"]), dic_dfs_2["cs"].drop(columns=["Identificação"]), ['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_cer"] = self.__generate_df_diffs(dic_dfs_1["cer"].drop(columns=["Identificação"]), dic_dfs_2["cer"].drop(columns=["Identificação"]), ['Número da Barra', "Número", "Código de Obra de Entrada"])
        dic_dfs["comp_linha"] = self.__generate_df_diffs(dic_dfs_1["linha"].drop(columns=["Identificação"]), dic_dfs_2["linha"].drop(columns=["Identificação"]), ['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_mutua"] = self.__generate_df_diffs(dic_dfs_1["mutua"].drop(columns=["Identificação"]), dic_dfs_2["mutua"].drop(columns=["Identificação"]), ['Barra De 1','Barra Para 1','Número de Circuito 1', "Barra De 2", "Barra Para 2", "Número de Circuito 2", "% Inicial 1", "% Final 1", "Código de Obra de Entrada"])
        dic_dfs["comp_sbarra"] = self.__generate_df_diffs(dic_dfs_1["sbarra"].drop(columns=["Identificação"]), dic_dfs_2["sbarra"].drop(columns=["Identificação"]), ['Número da Barra', "Número", "Código de Obra de Entrada"])
        dic_dfs["comp_slinha"] = self.__generate_df_diffs(dic_dfs_1["slinha"].drop(columns=["Identificação"]), dic_dfs_2["slinha"].drop(columns=["Identificação"]), ['Barra De','Barra Para','Número do Circuito', "Número", "Extremidade",  "Código de Obra de Entrada"])
        dic_dfs["comp_trafo"] = self.__generate_df_diffs(dic_dfs_1["trafo"].drop(columns=["Identificação"]), dic_dfs_2["trafo"].drop(columns=["Identificação"]), ['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_gerador"] = self.__generate_df_diffs(dic_dfs_1["gerador"].drop(columns=["Identificação"]), dic_dfs_2["gerador"].drop(columns=["Identificação"]), ['Número da Barra', 'Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_barra"] = pd.concat([dic_dfs_1["barra"], dic_dfs_2["barra"]]).drop_duplicates(keep=False).sort_values(by=['Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_cs"] = pd.concat([dic_dfs_1["cs"], dic_dfs_2["cs"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_cer"] = pd.concat([dic_dfs_1["cer"], dic_dfs_2["cer"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', "Número", "Código de Obra de Entrada"])
        # dic_dfs["comp_linha"] = pd.concat([dic_dfs_1["linha"], dic_dfs_2["linha"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_mutua"] = pd.concat([dic_dfs_1["mutua"], dic_dfs_2["mutua"]]).drop_duplicates(keep=False).sort_values(by=['Barra De 1','Barra Para 1','Número de Circuito 1', "Barra De 2", "Barra Para 2", "Número de Circuito 2", "% Inicial 1", "% Final 1", "Código de Obra de Entrada"])
        # dic_dfs["comp_sbarra"] = pd.concat([dic_dfs_1["sbarra"], dic_dfs_2["sbarra"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', "Número", "Código de Obra de Entrada"])
        # dic_dfs["comp_slinha"] = pd.concat([dic_dfs_1["slinha"], dic_dfs_2["slinha"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número do Circuito', "Número", "Extremidade",  "Código de Obra de Entrada"])
        # dic_dfs["comp_trafo"] = pd.concat([dic_dfs_1["trafo"], dic_dfs_2["trafo"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_gerador"] = pd.concat([dic_dfs_1["gerador"], dic_dfs_2["gerador"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', 'Número', "Código de Obra de Entrada"])
        # dic_dfs["comp_robras"] = pd.concat([dic_dfs_1["robras"], dic_dfs_2["robras"]]).drop_duplicates(keep=False).sort_values(by=["Código de Obra"])
        # dic_dfs["comp_area"] = pd.concat([dic_dfs_1["area"], dic_dfs_2["area"]]).drop_duplicates(keep=False).sort_values(by=["Número"])
        # dic_dfs["comp_glt"] = pd.concat([dic_dfs_1["glt"], dic_dfs_2["glt"]]).drop_duplicates(keep=False).sort_values(by=["Grupo"])
        # dic_dfs["comp_gbt"] = pd.concat([dic_dfs_1["gbt"], dic_dfs_2["gbt"]]).drop_duplicates(keep=False).sort_values(by=["Grupo"])

        print("PASSO 02 - LIMPANDO ARQUIVOS EXCEL DA PASTA (.XLSX e .XLSM)")
        files_siger = os.listdir(path_siger)
        try:
            for item in files_siger:
                if item.endswith(".xlsm") or item.endswith(".xlsx"):
                    os.remove( os.path.join(path_siger, item))
        except:
            return (f"Erro ao excluir o arquivo {item}! Favor verificar se o excel não está aberto ou rodando em segundo plano")

        print("PASSO 03 - MONTANDO ARQUIVOS EXCEL FRUTOS DA COMPARAÇÃO")
        if len(dic_dfs["comp_barra"]) > 0:
            self.plot_table_excel(dic_dfs["comp_barra"], path_siger + "/comp_barra.xlsx")
        if len(dic_dfs["comp_cs"]) > 0:
            self.plot_table_excel(dic_dfs["comp_cs"], path_siger + "/comp_cs.xlsx")
        if len(dic_dfs["comp_cer"]) > 0:
            self.plot_table_excel(dic_dfs["comp_cer"], path_siger + "/comp_cer.xlsx")
        if len(dic_dfs["comp_linha"]) > 0:
            self.plot_table_excel(dic_dfs["comp_linha"], path_siger + "/comp_linha.xlsx")
        if len(dic_dfs["comp_mutua"]) > 0:
            self.plot_table_excel(dic_dfs["comp_mutua"], path_siger + "/comp_mutua.xlsx")
        if len(dic_dfs["comp_slinha"]) > 0:
            self.plot_table_excel(dic_dfs["comp_slinha"], path_siger + "/comp_slinha.xlsx")
        if len(dic_dfs["comp_trafo"]) > 0:
            self.plot_table_excel(dic_dfs["comp_trafo"], path_siger + "/comp_trafo.xlsx")
        if len(dic_dfs["comp_sbarra"]) > 0:
            self.plot_table_excel(dic_dfs["comp_sbarra"], path_siger + "/comp_sbarra.xlsx")
        if len(dic_dfs["comp_gerador"]) > 0:
            self.plot_table_excel(dic_dfs["comp_gerador"], path_siger + "/comp_gerador.xlsx")
        if len(dic_dfs["comp_robras"]) > 0:
            self.plot_table_excel(dic_dfs["comp_robras"], path_siger + "/comp_robras.xlsx")
        if len(dic_dfs["comp_area"]) > 0:
            self.plot_table_excel(dic_dfs["comp_area"], path_siger + "/comp_area.xlsx")
        if len(dic_dfs["comp_glt"]) > 0:
            self.plot_table_excel(dic_dfs["comp_glt"], path_siger + "/comp_glt.xlsx")
        if len(dic_dfs["comp_gbt"]) > 0:
            self.plot_table_excel(dic_dfs["comp_gbt"], path_siger + "/comp_gbt.xlsx")

        print("PASSO 04 - LIMPANDO ARQUIVOS .XLSX")
        files_siger = os.listdir(path_siger)
        for item in files_siger:
            if item.endswith(".xlsx"):
                os.remove( os.path.join(path_siger, item))

        print("PASSO 05 - MONTANDO RELATÓRIO DE SAÍDA")
        list_report = []
        list_report.append("Relatório de Comparação: \n")
        list_report.append("Comparação BARRA: VERIFICAR!" if len(dic_dfs["comp_barra"]) > 0 else "Comparação BARRA: OK!")
        list_report.append("Comparação CS: VERIFICAR!" if len(dic_dfs["comp_cs"]) > 0 else "Comparação CS: OK!")
        list_report.append("Comparação CER: VERIFICAR!" if len(dic_dfs["comp_cer"]) > 0 else "Comparação CER: OK!")
        list_report.append("Comparação LINHA: VERIFICAR!" if len(dic_dfs["comp_linha"]) > 0 else "Comparação LINHA: OK!")
        list_report.append("Comparação SHUNT_LINHA: VERIFICAR!" if len(dic_dfs["comp_slinha"]) > 0 else "Comparação SHUNT_LINHA: OK!")
        list_report.append("Comparação TRANSFORMADOR: VERIFICAR!" if len(dic_dfs["comp_trafo"]) > 0 else "Comparação TRANSFORMADOR: OK!")
        list_report.append("Comparação SHUNT_BARRA: VERIFICAR!" if len(dic_dfs["comp_sbarra"]) > 0 else "Comparação SHUNT_BARRA: OK!")
        list_report.append("Comparação GERADOR: VERIFICAR!" if len(dic_dfs["comp_gerador"]) > 0 else "Comparação GERADOR: OK!")
        list_report.append("Comparação ROBRAS: VERIFICAR!" if len(dic_dfs["comp_robras"]) > 0 else "Comparação ROBRAS: OK!")
        list_report.append("Comparação AREA: VERIFICAR!" if len(dic_dfs["comp_area"]) > 0 else "Comparação AREA: OK!")
        list_report.append("Comparação GLT: VERIFICAR!" if len(dic_dfs["comp_glt"]) > 0 else "Comparação GLT: OK!")
        list_report.append("Comparação GBT: VERIFICAR!" if len(dic_dfs["comp_gbt"]) > 0 else "Comparação GBT: OK!")

        return "\n".join(list_report)