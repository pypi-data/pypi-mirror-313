# SIGER

API desenvolvida para acessar diretamente em DataFrames os dados do SIGER. Adicionalmente, várias manipulações e expansões de funcionalidades
também estão implementadas

## Instalação

Você pode instalar a última versão do pacote via pip:

```bash
pip install siger
```

## Módulos

Este projeto contém os seguintes módulos:

### ImportSIGER

Módulo base de todos os submódulos seguintes. É aqui que são definidos os códigos para download das informações do SIGER.

Exemplo de uso:

```python
from siger import ImportSIGER
oSIGER = ImportSIGER("https://siger.cepel.br/", "XXX", "XXX")

# Relatório de Obras
df_robras = oSIGER.get_robras()
```

### VerificaSIGER

Neste módulo estão armazenadas todas as funções e comparações que realizamos para verificar a qualidade dos 
decks carregados para o programa, assim como verificar possíveis erros após o carregamento.

Exemplo de uso:

```python
from siger import VerificaSIGER
oSIGER = VerificaSIGER("https://siger.cepel.br/", "XXX", "XXX")

# Verifica carregamento
path_decks=""            # Opcional
df_robras_original=""    # Opcional
relatorio_carregamento = oSIGER.verifica_carregamento(path_decks, df_robras_original)
```

### VisualizaSIGER

Neste módulo é ampliada a visão de como os equipamentos estão relacionados dentro do SIGER e quais seus dependentes.

Exemplo de uso:

```python
from siger import VisualizaSIGER
oSIGER = VisualizaSIGER("https://siger.cepel.br/", "XXX", "XXX")

# Verifica carregamento
df_siger = oSIGER.get_base_siger()
codigo_obra_para_visualizar = ""
relatorio_carregamento = oSIGER.verifica_carregamento(path_decks, df_robras_original)
```

### WebSIGER

Aqui estão as funcionalidades que permitem o carregamento de uma lista de decks para dentro do SIGER. É possível aqui, programar a execução do carregamento desde os 7 arquivos até o carregamento desde o início da base.

Exemplo de uso:

```python
from siger import WebSIGER
import pandas as pd
oSIGER = WebSIGER("https://siger.cepel.br/", "XXX", "XXX")

# Verifica carregamento
df_arquivos_carregar = pd.read_csv("ARQUIVO_CARGA", sep=";")
chromedriver_path = r"D:\_APAGAR\_ChromeDriver\chromedriver.exe"
flag_carregamento = oSIGER.carrega_siger(df_arquivos_carregar, chromedriver_path)
```

## Licença

Este projeto está licenciado sob a GNU GENERAL PUBLIC LICENSE. Isso significa que você pode copiar, distribuir e modificar o software, desde que você acompanhe quaisquer modificações com a mesma licença e que você disponibilize o código-fonte.

Para mais detalhes, por favor veja o arquivo LICENSE no repositório ou visite o site oficial da GNU.
