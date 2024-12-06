from .lbx_logger import lbx_logger
import logging
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np

class postgreSQL: # Classe de acesso e interação com banco PostgreSQL
    """
#### Classe **postgreSQL**

Recursos de interação com o banco de dados relacional PostgreSQL

1. O método `postgreSQl.db()` exige que as credenciais e parametros de acesso sejam fornecidas em um *dicionário* com, ao mínimo, o seguinte formato:

```python
credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
            }

conexao = postgreSQL.db(credenciais)
```

O nome do schema é ser declarado no contexto da query, mas se desejar alterar o schema padrão, adicione *`'options' : '-c search_path=[NOME_SCHEMA]',`* ao dicionário.

Qualquer argumento de conexão previsto no pacote *psycopg2* são aceitos como entrada no dicionário acima.

2. O método `postgreSQl.csv_df()` lê arquivo texto do tipo CSV e o converte para o objeto Dataframe do `pandas`. A assinatura da função exige que se forneça o caminho do arquivo CSV e, opcionalmente o caracter delimitador. Se o caracter demilitador não for informado, será assumido `;`. Considere usar a função `Path` para tratar o caminho do arquivo de origem.

```python
from pathlib import Path
arquivo_csv = Path('./diretorio/arquivo_exemplo.csv')
dados = postgreSQL.csv_df(arquivo_csv, CsvDelim=',') # usando vírgula como separador. se omisso, assume ";'
```

Qualquer argumento da função read_csv do Pandas é aceito na chamada do método.


3. O método `postgreSQl.db_insert_df()` insere dados a partir de um Dataframe (pandas) em uma tabela do banco com estrutura de colunas equivalente.

A assinatura da função é `postgreSQL.db_insert_df([conexao], [dataframe_origem], [tabela_destino], Schema=None, Colunas=None, OnConflict=None)`

É necessário que os nomes das colunas do dataframe coincidam com o nome das colunas da tabela. 
Não há como traduzir/compatibilizar (de-para) nomes de colunas entre o dataframe e a tabela.

Os três primeiros parametros são posicionais e correspondem, respectivamente, (1) ao objeto da conexão com o banco, (2) ao objeto que contém o dataframe e (3) ao nome da tabela de destino.
Assume-se que a tabela pertença ao schema padrão (definido na variável _search_path_ do servidor). Caso a tabela de destino esteja em um _schema_ diferente do padrão, deve-se informar seu nome no parâmetro opcional `Schema`.

O parametro opcional `Colunas` espera um objeto do tipo _lista_ que contenha a relação das colunas a serem importadas. 
As colunas listadas neste objeto precisam existir nas duas pontas (dataframe e tabela).
Caso seja omisso, todas as colunas do dataframe serão inseridas na tabela. Neste caso, admite-se que haja colunas na tabela que não exitam no dataframe (serão gravadas como NULL), mas o contrário provocará erro. 

O último parametro opcional `OnConflict` espera uma declaração para tratar o que fazer caso o dado a ser inserido já exista na tabela, baseado na cláusula [*ON CONFLICT*](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT) do comando INSERT. A claúsula deve ser declarada explicita e integralmente nessa variável (clausula, _target_ e _action_) e não há crítica/validação desse argumento, podendo gerar erros se declarado inconforme com o padrão SQL.

Exemplo de uso:

```python
from lbx_toolkit import postgreSQL
from pathlib import Path

credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
            }

conexao = postgreSQL.db(credenciais)

arquivo_csv = Path('./diretorio/arquivo_exemplo.csv')
dados = postgreSQL.csv_df(arquivo_csv, CsvDelim=',') # usando vírgula como separador. se omisso, assume ";'

postgreSQL.db_insert_df(conexao, dados, 'teste_table', Schema='meu_esquema', OnConflict='on conflict (coluna_chave_primaria) do nothing')

# conexão com o banco precisa ser fechada explicitamente após a chamada do método, caso não seja mais utilizada:
conexao.close()
```

4. O método `postgreSQl.db_select()` executa consultas no banco de dados e retorna um `cursor` com o resultado.

A assinatura da função é `postgreSQL.db_select([conexao], [query])`

São permitidas apenas instruções de consulta (podendo serem complexas, por exemplo, com uso de [CTE](https://www.postgresql.org/docs/current/queries-with.html)). A presença de outras instruções SQL de manipulação de dados e metadados não são permitidas e abortarão a execução da query, se presentes.

O `cursor` é fechado no contexto do método, antes do retorno, *não podendo* ser manipulado após recebido como retorno da função.

A função retorna *dois objetos*, o primeiro contendo os dados do cursor, o segundo, contendo os nomes das respectivas colunas.

Exemplo de uso:

```python
from lbx_toolkit import postgreSQL
from pathlib import Path

credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
            }

conexao = postgreSQL.db(credenciais)

query = 'select * from meu_esquema.teste_table'

dados, colunas = postgreSQL.db_select(conexao, query)
conexao.close()
```

5. O método `postgreSQl.db_update()` executa updates no banco

A assinatura da função é `postgreSQL.db_update([conexao], [query])`

São permitidas apenas instruções de update. A presença de outras instruções SQL de manipulação de dados e metadados não são permitidas e abortarão a execução da query.

A função retorna *a quantidade de linhas alteradas*.

Exemplo de uso:

```python
from lbx_toolkit import postgreSQL
from pathlib import Path

credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
            }

conexao = postgreSQL.db(credenciais)

query = "update meu_esquema.teste_table set coluna='novo_valor' where pk='chave'"

result = postgreSQL.db_update(conexao, query)
conexao.close()
    ```

    """    
    def __init__(self, config, logger=None):
        self.logger = logger if not logger is None else lbx_logger(None, logging.DEBUG, '%(levelname)s: %(message)s') # se não fornecer o logger, vai tudo para o console

        try:
            self.Conexao = psycopg2.connect(**config)  ## na chamada de uma função/método, o * explode os valores de um dicionário em argumentos posicionais (só valores) e ** explode discionário em argumentos nominais (nome=valor)
        except Exception as Err:
            raise
        #
        #
    def csv_df(self, CsvPath, CsvDelim=';', **kwargs): # Le arquivo CSV e gera Dataframe do Pandas
        """
        Os parametros de read_csv() do Pandas podem ser passados opcionalmente para a função para ajustar a importação
        """
        try:
            DataFrame = pd.read_csv(CsvPath, delimiter=CsvDelim, **kwargs)  # Verifique se o delimitador é ';'
            DataFrame.replace({np.nan: None}, inplace=True)  ## troca 'NaN' por None (null no postgresql)
            return DataFrame
        except Exception as Err:
            raise
        #
        #
    def db_insert_df(self, DataFrame, Tabela, Schema=None, Colunas=None, OnConflict=None): # Insere os dados de um dataframe em uma tabela equivalente no banco (exige mesma estrutura de colunas)
        # Essa função exige que os nomes dos cabeçalhos das colunas do CSV sejam os mesmos das colunas da tabela de destino
        Colunas = Colunas or DataFrame.columns.tolist()     # Caso não seja fornecida a lista de colunas, assume as colunas do DataFrame
        Valores = [tuple(Linha) for Linha in DataFrame[Colunas].values]    
        Schema = Schema or 'public'
        Query = f'insert into {Schema}.{Tabela} ({', '.join(Colunas)}) values %s '
        if not OnConflict is None:
            Query = Query + OnConflict

        try:
            self.Cursor = self.Conexao.cursor() 
            execute_values(self.Cursor, Query, Valores)  
            self.Conexao.commit()
        except Exception as Err:
            self.Conexao.rollback()
            raise
        finally:        
            self.Cursor.close()
            #Conexao.close() ## conexão precisa ser fechada explicitamente fora da classe
        #
        #
    def db_select(self, Query): # Retorna um cursor à partir de um select
        BlackList = ['INSERT ', 'DELETE ', 'UPDATE ', 'CREATE ', 'DROP ', 'MERGE ', 'REPLACE ', 'CALL ', 'EXECUTE ']
        if any(element in Query.upper() for element in BlackList):
            BlackListed = [element for element in BlackList if element in Query.upper()]          
            self.logger.erro(f'{__name__}: Este método permite apenas consultas. A query informada possui as seguintes palavras reservadas não aceitas: {BlackListed} e não foi executada!')
            return None    
        else:
            try:
                self.Cursor = self.Conexao.cursor()
                self.Cursor.execute(Query)
                Dados = self.Cursor.fetchall()
                Colunas = [Col[0] for Col in self.Cursor.description]
                self.Conexao.commit()
                self.Cursor.close()
                return Dados, Colunas
            except Exception as Err:
                self.Conexao.rollback()
                raise   
        #
        #
    def db_update(self, Query): # Retorna um cursor à partir de um select
        UpdRows = 0
        BlackList = ['INSERT ', 'SELECT ', 'CREATE ', 'DROP ', 'MERGE ', 'REPLACE ', 'CALL ', 'EXECUTE ']
        if any(element in Query.upper() for element in BlackList):
            BlackListed = [element for element in BlackList if element in Query.upper()]          
            self.logger.erro(f'{__name__}: Este método permite apenas updates e deletes. A query informada possui as seguintes palavras reservadas não aceitas: {BlackListed} e não foi executada!')
            return None            
        else:
            try:
                self.Cursor = self.Conexao.cursor()
                self.Cursor.execute(Query)
                UpdRows = self.Cursor.rowcount
                self.Conexao.commit()
                self.Cursor.close()
                return UpdRows
            except Exception as Err:
                self.Conexao.rollback()
                raise  
        #
        #
