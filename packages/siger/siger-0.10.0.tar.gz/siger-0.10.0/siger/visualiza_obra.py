import pandas as pd
from .import_siger import ImportSIGER

class VisualizaSIGER(ImportSIGER):
    """
    Classe para visualização e geração de relatórios a partir de dados do sistema SIGER.

    Esta classe herda funcionalidades da classe ImportSIGER e adiciona métodos para visualização
    e geração de relatórios sobre os equipamentos e obras registrados no sistema.

    Métodos
    -------
    visualiza_obra(df_siger, codigo_obra_vis)
        Gera um relatório analisando equipamentos e dependências para um projeto de construção (obra) específico.

    get_dependancies(df_siger, df_obra)
        Obtém as dependências de uma obra, incluindo obras dependentes no passado e no futuro.

    Observações
    -----
    Esta classe estende a classe ImportSIGER e adiciona métodos específicos para visualização e geração
    de relatórios sobre os dados importados do sistema SIGER.
    """
    ###================================================================================================================
    ###
    ### CÓDIGOS DE INICIALIZAÇÃO
    ###
    ###================================================================================================================
    def __init__(self, url_siger, usuario, senha):
        """
        Inicializa uma instância de VerificaSIGER.

        Parâmetros:
        -----------
        url_siger : str
            A URL do sistema SIGER.
        usuario : str
            O nome de usuário para acessar o sistema SIGER.
        senha : str
            A senha para acessar o sistema SIGER.
        """
        # Pegando todas as funções da Import_SIGER para uso nesse módulo
        super().__init__(url_siger, usuario, senha)

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA AUXÍLIO NA VISUALIZAÇÃO DO ESCORREGAMENTO
    ###
    ###================================================================================================================
    def __get_dados_lt(self, row):
        """
        Obtém os dados da linha de transmissão (LT) a partir de uma linha do DataFrame.

        Parâmetros:
        -----------
        row : pandas.Series
            Uma linha do DataFrame contendo os dados da linha de transmissão.

        Retorna:
        --------
        tuple
            Uma tupla contendo os seguintes elementos:
            - barra_de : str
                O identificador da barra de origem da LT.
            - barra_para : str
                O identificador da barra de destino da LT.
            - num_circ : str
                O número do circuito da LT.
            - circ1 : str
                O identificador único para o primeiro sentido da LT.
            - circ2 : str
                O identificador único para o segundo sentido da LT.
        """
        barra_de = (row["ID"].split("#"))[1]
        barra_de = "#"+barra_de+"#"
        barra_pa = (row["ID"].split("#"))[3]
        barra_pa = "#"+barra_pa+"#"
        num_circ = (row["ID"].split("$"))[1]
        circ1 = barra_de + "-" + barra_pa + "-$" + num_circ + "$"
        circ2 = barra_pa + "-" + barra_de + "-$" + num_circ + "$"

        return barra_de, barra_pa, num_circ, circ1, circ2

    def __get_dados_lt_2(self, row):
        """
        Obtém os dados da linha de transmissão (LT) a partir de uma linha do DataFrame.

        Parâmetros:
        -----------
        row : pandas.Series
            Uma linha do DataFrame contendo os dados da linha de transmissão.

        Retorna:
        --------
        tuple
            Uma tupla contendo os seguintes elementos:
            - barra_de : str
                O identificador da barra de origem da LT.
            - barra_para : str
                O identificador da barra de destino da LT.
            - num_circ : str
                O número do circuito da LT.
            - circ1 : str
                O identificador único para o primeiro sentido da LT.
            - circ2 : str
                O identificador único para o segundo sentido da LT.
        """
        barra_de = (row["ID"].split("#"))[5]
        barra_de = "#"+barra_de+"#"
        barra_pa = (row["ID"].split("#"))[7]
        barra_pa = "#"+barra_pa+"#"
        num_circ = (row["ID"].split("$"))[7]
        circ1 = barra_de + "-" + barra_pa + "-$" + num_circ + "$"
        circ2 = barra_pa + "-" + barra_de + "-$" + num_circ + "$"

        return barra_de, barra_pa, num_circ, circ1, circ2

    def __dependentes_futuros(self, df_siger, row, tipo):
        """
        Identifica equipamentos dependentes futuros com base em um equipamento específico.

        Parâmetros:
        -----------
        df_siger : pandas.DataFrame
            DataFrame contendo os dados do sistema elétrico do SIGER.
        row : pandas.Series
            Uma linha do DataFrame representando um equipamento do sistema elétrico.
        tipo : str
            O tipo do equipamento ("BR", "CR", "CS", "LT", "MT", "SB", "SL", "TR").

        Retorna:
        --------
        pandas.DataFrame
            DataFrame contendo os equipamentos dependentes futuros do equipamento fornecido, de acordo com o tipo.
        """
        # Filtro de tipo de eqps
        df_temp = df_siger.copy()
        #
        if tipo == "BR":
            barra_de = "#" + (row["ID"].split("#"))[1] + "#"
            df_temp = df_temp[df_temp['ID'].str.contains(barra_de)]
        elif tipo == "CR":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "CS":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "LT":
            _, _, _, circ1, circ2 = self.__get_dados_lt(row)
            df_temp = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
        elif tipo == "MT":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "SB":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "SL":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "TR":
            _, _, _, circ1, circ2 = self.__get_dados_lt(row)
            df_temp = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]

        # Removendo código de obra de entrada atual e saída.....quero somente dependentes indiretos...
        df_temp= df_temp[df_temp['Código de Obra de Entrada'] != row["Código de Obra de Entrada"]]
        df_temp= df_temp[df_temp['Código de Obra de Saída'] != row["Código de Obra de Entrada"]]

        # Garantindo que são obras pais que já existiam antes da entrada desse equipamento
        df_temp = df_temp[df_temp['Data de Entrada'] >= row["Data de Entrada"]]
        # df_temp = df_temp[df_temp['Data de Entrada'] <= row["Data de Saída"]]

        if not df_temp.empty:
            pass

        return df_temp

    def __dependentes_passados(self, df_siger, row, tipo):
        """
        Obtém os equipamentos dependentes passados com relação a um equipamento específico.

        Parâmetros:
        -----------
        df_siger : pandas.DataFrame
            DataFrame contendo os dados do sistema elétrico.
        row : pandas.Series
            Uma linha do DataFrame contendo os dados do equipamento de referência.
        tipo : str
            O tipo de equipamento ('BR', 'CR', 'CS', 'LT', 'MT', 'SB', 'SL', 'TR').

        Retorna:
        --------
        pandas.DataFrame
            Um DataFrame contendo os equipamentos dependentes passados em relação ao equipamento de referência e ao tipo especificado.
        """
        # Filtro de tipo de eqps
        df_temp = df_siger.copy()
        #
        if tipo == "BR":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "CR":
            barra_de = "#" + (row["ID"].split("#"))[1] + "#"
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "BR")]
            #
            df_temp2 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2])
        elif tipo == "CS":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "LT")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp3 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2, df_temp3])
        elif tipo == "LT":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "LT")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp = pd.concat([df_temp1, df_temp2])

        elif tipo == "MT":
            barra_de1, barra_pa1, numcirc1, circ1, circ2 = self.__get_dados_lt(row)
            barra_de2, barra_pa2, numcirc2, circ3, circ4 = self.__get_dados_lt_2(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(barra_de1,regex=False) | df_temp['ID'].str.contains(barra_pa1,regex=False) | df_temp['ID'].str.contains(barra_de2,regex=False) | df_temp['ID'].str.contains(barra_pa2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "BR")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False) | df_temp['ID'].str.contains(circ3,regex=False) | df_temp['ID'].str.contains(circ4,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "LT")]
            #
            df_temp3 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2, df_temp3])

        elif tipo == "SB":
            barra_de = "#" + (row["ID"].split("#"))[1] + "#"
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "BR")]
            #
            df_temp2 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2])

        elif tipo == "SL":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "LT")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp3 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2, df_temp3])

        elif tipo == "TR":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "TR")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp = pd.concat([df_temp1, df_temp2])

        # Removendo código de obra de entrada atual e saída.....quero somente dependentes indiretos...
        df_temp= df_temp[df_temp['Código de Obra de Entrada'] != row["Código de Obra de Entrada"]]
        df_temp= df_temp[df_temp['Código de Obra de Saída'] != row["Código de Obra de Entrada"]]

        # Garantindo que são obras pais que já existiam antes da entrada desse equipamento
        df_temp = df_temp[df_temp['Data de Entrada'] <= row["Data de Entrada"]]
        # df_temp = df_temp[df_temp['Data de Entrada'] <= row["Data de Saída"]]

        if not df_temp.empty:
            pass

        return df_temp

    def get_dependancies(self, df_siger, df_obra):
        """
        Obtém os equipamentos dependentes passados com relação a um equipamento específico.

        Parâmetros:
        -----------
        df_siger : pandas.DataFrame
            DataFrame contendo os dados do sistema elétrico.
        row : pandas.Series
            Uma linha do DataFrame contendo os dados do equipamento de referência.
        tipo : str
            O tipo de equipamento ('BR', 'CR', 'CS', 'LT', 'MT', 'SB', 'SL', 'TR').

        Retorna:
        --------
        pandas.DataFrame
            Um DataFrame contendo os equipamentos dependentes passados em relação ao equipamento de referência e ao tipo especificado.

        Notas:
        --------
        Todos os equipamentos aqui relacionados portanto nascem no mesmo código de obra [A] na data de entrada [I]
                A ideia do escorregamento é mudar a data de entrada [I] para [II], que pode ser anterior ou posterior
                Portanto, a ideia é considerar essa obra como "pai" e buscar todos os possíveis "filhos" dessas obras, assim, eu descubro
        todas as obras dependentes dessa obra. O esquema de paternidade pode ser resumido da seguinte forma
         __________________________________________________________________________________________________________________
        I-- TIPO EQP -- I -- TIPO DE EQP DE OBRAS DEPENDENTES -- I -- CONDIÇÃO DE DATA -- I -- CONDIÇÃO DE CÓDIGO DE OBRA --I
        I-------------------------------------------------------------------------------------------------------------------I
        I  BR           I BR / CR / CS / LT / MT / SB / SL / TR  I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  CR           I CR                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  CS           I CS                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  LT           I CS / LT / MT / SL                      I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  MT           I MT                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  SB           I SB                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  SL           I SL                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I-------------------------------------------------------------------------------------------------------------------I
        I  TR           I TR                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        I___________________________________________________________________________________________________________________I
        """
        # Essa vai ser o núcleo da busca do relatório de dependentes dessa obra - EM PRIMEIRO NÍVEL
        df_dependentes_futuro = pd.DataFrame()
        df_dependentes_passado = pd.DataFrame()
        data_entrada_depend_futuro = ""
        idx_data_futuro = ""
        data_entrada_depend_passado = ""
        idx_data_passado = ""

        for index, row in df_obra.iterrows():
            # Vou preencher o df_temp com obras dependentes do eqp da df_obra analisado
            # Os dados de ROW são da obra pai / os dados de df_temp são das obras dependentes
            df_temp = pd.DataFrame()
            match row["Tipo"]:
                case "BR":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "BR")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "BR")
                case "CR":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "CR")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "CR")
                case "CS":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "CS")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "CS")
                case "LT":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "LT")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "LT")
                case "MT":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "MT")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "MT")
                case "SB":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "SB")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "SB")
                case "SL":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "SL")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "SL")
                case "TR":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "TR")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "TR")
            # Encontrando alguma obra dependente no horizonte futuro
            if not df_temp_futuro.empty:
                df_temp = df_temp_futuro.copy()
                df_temp = df_temp.assign(Tipo_PAI=row["Tipo"])
                df_temp = df_temp.assign(ID_PAI=row["ID"])
                df_temp = df_temp.assign(CO_Entrada_PAI=row["Código de Obra de Entrada"])
                df_temp = df_temp.assign(Data_Entrada_PAI=row["Data de Entrada"])
                #
                df_dependentes_futuro = pd.concat([df_dependentes_futuro, df_temp], ignore_index=True)
                data_entrada_depend_futuro = min(df_dependentes_futuro["Data de Entrada"])
                idx_data_futuro = pd.to_datetime(df_dependentes_futuro["Data de Entrada"]).idxmin()
                #
                df_dependentes_futuro = df_dependentes_futuro.sort_values(by='Data de Entrada', ascending=True)

            # Encontrando alguma obra dependente no horizonte passado
            if not df_temp_passado.empty:
                df_temp = df_temp_passado.copy()
                df_temp = df_temp.assign(Tipo_FILHO=row["Tipo"])
                df_temp = df_temp.assign(ID_FILHO=row["ID"])
                df_temp = df_temp.assign(CO_Entrada_FILHO=row["Código de Obra de Entrada"])
                df_temp = df_temp.assign(Data_Entrada_FILHO=row["Data de Entrada"])
                #
                df_dependentes_passado = pd.concat([df_dependentes_passado, df_temp], ignore_index=True)
                data_entrada_depend_passado = max(df_dependentes_passado["Data de Entrada"])
                idx_data_passado = pd.to_datetime(df_dependentes_passado["Data de Entrada"]).idxmax()
                #
                df_dependentes_passado = df_dependentes_passado.sort_values(by='Data de Entrada', ascending=True)

        return data_entrada_depend_futuro, idx_data_futuro, df_dependentes_futuro, data_entrada_depend_passado, idx_data_passado, df_dependentes_passado

    def visualiza_obra(self, df_siger, codigo_obra_vis):
        """
        Gera um relatório analisando equipamentos e dependências para um projeto de construção (obra) específico.

        Parameters
        ----------
        df_siger : DataFrame
            DataFrame contendo informações sobre equipamentos e obras.
        codigo_obra_vis : str
            Código da obra que será analisada.

        Returns
        -------
        list_report : list
            Lista contendo o relatório gerado.

        Notes
        -----
        O relatório é dividido em várias seções:

        - Equipamentos A Serem Integrados: Lista os equipamentos que serão integrados ao sistema.
        - Equipamentos A Serem Integrados - Dependência Passada: Lista os equipamentos que devem existir antes da integração da obra especificada, incluindo uma observação sobre possíveis mudanças de datas.
        - Equipamentos A Serem Integrados - Dependência Futura: Lista os equipamentos que devem existir após a integração da obra especificada, incluindo uma observação sobre possíveis mudanças de datas.
        - Equipamentos A Serem Excluídos: Lista os equipamentos que serão excluídos do sistema após a integração da obra especificada.
        """
        # Obtendo o dataframe de com equipamentos
        df_siger_principal = df_siger[(df_siger["Código de Obra de Entrada"] == codigo_obra_vis)
                                      |
                                      (df_siger["Código de Obra de Saída"] == codigo_obra_vis)]
        df_siger_principal_ent = df_siger[(df_siger["Código de Obra de Entrada"] == codigo_obra_vis)]

        # Obtendo dados dos dependentes
        if not df_siger_principal_ent.empty:
            data_dep_futuro, idx_futuro, df_dependentes_futuro, data_dep_passado, idx_passado, df_dependentes_passado = self.get_dependancies(df_siger, df_siger_principal_ent)
        else:
            data_dep_futuro, idx_futuro, df_dependentes_futuro, data_dep_passado, idx_passado, df_dependentes_passado = "","","","","",""

        # Ajuste data
        df_siger['Data de Entrada'] = pd.to_datetime(df_siger['Data de Entrada']).dt.strftime('%d/%m/%Y')
        df_siger['Data de Saída'] = pd.to_datetime(df_siger['Data de Saída']).dt.strftime('%d/%m/%Y')

        # Inserções
        df_siger_principal_in = df_siger[(df_siger["Código de Obra de Entrada"] == codigo_obra_vis)]
        data_in = df_siger_principal_in["Data de Entrada"].iloc[0]
        df_temp = df_siger_principal_in.dropna(subset = ["Data de Saída"])
        if len(df_temp) > 0:
            df_temp = df_temp.sort_values(by=['Data de Saída', 'Código de Obra de Saída'], ascending=True)
            data_out = df_temp["Data de Saída"].iloc[0]
        else:
            data_out = ""

        # Obras dependentes que devem existir na base
        if len(df_dependentes_passado) > 0:
            df_dependentes_passado_visualiz = df_dependentes_passado[['Tipo','ID','Código de Obra de Entrada','Código de Obra de Saída','Data de Entrada','Data de Saída','ID_FILHO']].copy()
            df_dependentes_passado_visualiz.loc[:,'Data de Entrada'] = pd.to_datetime(df_dependentes_passado_visualiz['Data de Entrada']).dt.strftime('%d/%m/%Y')
            df_dependentes_passado_visualiz.loc[:,'Data de Saída'] = pd.to_datetime(df_dependentes_passado_visualiz['Data de Saída']).dt.strftime('%d/%m/%Y')
            # Obras dependentes fora do BAS_JUN20
            df_dependentes_passado_visualiz = df_dependentes_passado_visualiz[
                                                    ~((df_dependentes_passado_visualiz["Código de Obra de Entrada"] == "BASE_JUN20")
                                                    &
                                                    (df_dependentes_passado_visualiz["Código de Obra de Saída"].isna()))]
        else:
            df_dependentes_passado_visualiz = pd.DataFrame()

        if len(df_dependentes_futuro) > 0:
            # Obras dependentes que irão existir na base
            df_dependentes_futuro_visualiz = df_dependentes_futuro[['Tipo','ID','Código de Obra de Entrada','Código de Obra de Saída','Data de Entrada','Data de Saída','ID_PAI']]
            df_dependentes_futuro_visualiz['Data de Entrada'] = pd.to_datetime(df_dependentes_futuro_visualiz['Data de Entrada']).dt.strftime('%d/%m/%Y')
            df_dependentes_futuro_visualiz['Data de Saída'] = pd.to_datetime(df_dependentes_futuro_visualiz['Data de Saída']).dt.strftime('%d/%m/%Y')
            # Obras dependentes fora do BAS_JUN20
            df_dependentes_futuro_visualiz = df_dependentes_futuro_visualiz[
                                                    ~((df_dependentes_futuro_visualiz["Código de Obra de Entrada"] == "BASE_JUN20")
                                                    &
                                                    (df_dependentes_futuro_visualiz["Código de Obra de Saída"].isna()))]
        else:
            df_dependentes_futuro_visualiz = pd.DataFrame()

        # Exclusões
        df_siger_principal_out = df_siger[(df_siger["Código de Obra de Saída"] == codigo_obra_vis)]

        # Montando relatório
        list_report = []
        list_report.append(f"\nANÁLISE DOS EQUIPAMENTOS E DEPENDÊNCIAS DA OBRA : {codigo_obra_vis}\n")

        # Apresentando a obra de entrada
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM INTEGRADOS\n")
        if len(df_siger_principal_in) > 0:
            list_report.append(f"O código de obra {codigo_obra_vis} irá integrar no SIGER os seguintes equipamentos:\n")
            df_siger_principal_in.loc[:, 'ID'] = df_siger_principal_in['ID'].str.replace('[#$]', '', regex=True)
            list_report.append(df_siger_principal_in.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não integra no SIGER novos equipamentos.\n")

        # Apresentando a obra de entrada
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM INTEGRADOS - DEPENDÊNCIA PASSADA\n")
        if len(df_dependentes_passado_visualiz) > 0:
            list_report.append(f"Para que o código de obra {codigo_obra_vis} seja integrado corretamente no SIGER, os seguintes equipamentos DEVEM EXISTIR ANTES da integração dessa obra no banco:")
            list_report.append(f"***DICA: Se alguma dessas obras for escorregada para uma data futura da data de entrada atual ({data_in}), irá levar de reboque a obra {codigo_obra_vis} para esta data!\n")
            df_dependentes_passado_visualiz.loc[:,'ID'] = df_dependentes_passado_visualiz['ID'].str.replace('[#$]', '', regex=True)
            df_dependentes_passado_visualiz.loc[:,'ID_FILHO'] = df_dependentes_passado_visualiz['ID_FILHO'].str.replace('[#$]', '', regex=True)
            list_report.append(df_dependentes_passado_visualiz.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não possui dependências que exigem que equipamentos existam na BASE ANTES da sua integração.\n")

        # Apresentando a obra de saída
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM INTEGRADOS - DEPENDÊNCIA FUTURA\n")
        if len(df_dependentes_futuro_visualiz) > 0:
            list_report.append(f"Para que o código de obra {codigo_obra_vis} seja integrado corretamente no SIGER, os seguintes equipamentos DEVEM EXISTIR DEPOIS da integração dessa obra no banco:")
            list_report.append(f"***DICA: Se alguma dessas obras for escorregada para uma data anterior da data de entrada atual ({data_in}), irá levar de reboque a obra {codigo_obra_vis} para esta data!\n")
            df_dependentes_futuro_visualiz.loc[:,'ID'] = df_dependentes_futuro_visualiz['ID'].str.replace('[#$]', '', regex=True)
            df_dependentes_futuro_visualiz.loc[:,'ID_PAI'] = df_dependentes_futuro_visualiz['ID_PAI'].str.replace('[#$]', '', regex=True)
            list_report.append(df_dependentes_futuro_visualiz.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não possui dependências que exigem que equipamentos existam na BASE APÓS a sua integração.\n")

        # Apresentando a obra de exclusão
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM EXCLUÍDOS\n")
        if len(df_siger_principal_out):
            list_report.append(f"Os seguintes equipamentos são excluídos com a integração da obra {codigo_obra_vis} no banco:\n")
            df_siger_principal_out.loc[:,'ID'] = df_siger_principal_out['ID'].str.replace('[#$]', '', regex=True)
            list_report.append(df_siger_principal_out.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não exclui nenhum equipamento do banco.\n")

        return list_report
