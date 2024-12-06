<a id="lbxtoolkit"></a>

# lbxtoolkit

__**Caixa de ferramentas de automações de processo (RPA)**__


Biblioteca com ferramentas utilitárias e de uso recorrente em aplicações de RPA para automações de processos.

Todas as classes e métodos deste módulo possuem **docstrings**. 
Portanto, para ter acesso às informações de uso, use `nome_classe.__doc__`. 
Exemplo:

```python
from lbxtoolkit import Servicer
help = Servicer.__doc__
print(help)
```

## **Classe e funções**

**auth_EntraID**
Usa o Microsoft Entra ID (antiga Azure AD) para evitar execução não autorizada de scripts 
- `disclaimer` : Mensagem sobre a necessidade de autenticação
- `valida_grupo` : Autentica o usuário e aborta se checa não pertencer ao grupo de segurança


**postgreSQL**
Interage com o banco de dados PostgreSQL
- `db` Inicia sessão com o banco
- `csv_df` Lê arquivo CSV e gera Dataframe (pandas) a partir dele
- `db_insert_df` Insere informações de Dataframe em tabela do banco com estrutura equivalente
- `db_select` Retorna um cursor a partir de uma query
- `db_update` Executa update em tabelas


**api_rest**
Interage com APIs RESTfull, especialmente providas para a plataforma Sienge
- `auth_base` Autentica (HTTPBasicAuth) sessão na API
- `auth_bearer` Autentica sessão na API pelos métodos: OAuth, JWT, Bearer 
- `endpoint_json` Realizad chama ao endpoint. Payload em formato `json` opcional.
- `trata_erro_sienge` Retorna a mensagem de erro do Sienge caso código de retorno seja diferente de 200.
- `close` Encerra a sessão autenticada

**lbx_logger**
Manipula e formata as mensagens de saída do script para direcioná-las para tela (stdout) e/ou arquivo de log
- `add` Adiciona a mensagem a um _buffer_ sem exibir, acumulando até a próxima chamada em algum dos níveis abaixo.
- `print` Contorna o manipulador de log e imprime diretamente na tela (stdout), sem formatar a mensagem nem registrar no arquivo
- `debug, .info, .aviso, .erro, .critico` Classifica as mensagens por nível de severidade/relevância e rediciona a saída (arquivo, tela, tela+arquivo) conforme a configuração do nível
- `stop_logging` Interrompe a manipulação das saídas pelo logger e restaura as saídas padrão (stdout/stderr) para a tela 
- `filtra` Filtra os eventos do arquivo de log registrados em um intervalo de tempo específico

**SafeLogger**
Intercepta as ordens de saída comandadas pelos métodos de lbx_logger e interrompe um daemon em execução antes de saír

**ConfigManager**
Permite a inicialização/instanciamento e o consumo de objetos entre classes e métodos independentes, inclusive métodos estáticos (sem instanciamento da classe), garantindo que todas as partes do código usem a mesma instância e, portanto, compartilhem a mesma configuração.
- `initialize` Inicialização com Argumentos Dinâmicos: O método initialize usa **kwargs para aceitar qualquer número de pares chave-valor, armazenando-os no dicionário da instância.
- `get` O método get aceita uma chave como argumento e retorna o valor correspondente do dicionário _config.
- `set` O método set permite adicionar ou atualizar dinamicamente valores no dicionário _config.
- `reset` O método reset limpa todas as configurações armazenadas, permitindo uma nova inicialização do ConfigManager com novos valores 

**ServicoWindows**
Gerencia a instalação e execução de um daemon como um serviço do windows. Também assum o controle dos argumentos recebidos via linha de comando.
- `SvcInstall` Cria um serviço do windows com base neste script
- `SvcRemove` Remove o serviço do windows configurado à partir de `SvcInstall`
- `SvcStop` Para/Interrompe a execução do serviço do windows criado por este script (método herdado da classe pai _win32serviceutil.ServiceFramework_)
- `SvcDoRun` Inicializa a execução do serviço do windows criado por este script (método herdado da classe pai _win32serviceutil.ServiceFramework_)

**Servicer**
Classe base com a esrtutura padrão para a criação dameons/serviços do windows.
- `run`, `stop` Usados para iniciar (`run`) e parar (`stop`) a execução do daemon/serviço. 
- `main` deve ser chamada para controlar a sua chamada inicial do script, tratando os argumentos da linha de comando
- `on_run` é o método que efetivamente executa o propósito do script quando o método pai `run` é executado
- `args_parser` é o método que define o comportamento do script quando o método `main` é executado (**`argpaser`**)

**misc**
Classe de miscelâneas/diversos
- `seleciona_arquivo` Abre um picker do sistema operacionar para selecionar um *arquivo* e retorna seu path
- `seleciona_dir` Abre um picker do sistema operacionar para selecionar um *diretório* e retorna seu path
- `normaliza` Limpa caracteres especiais e espaços de strings e retorna tudo em minúsculo
- `get_cmd_window` Captura a referencia da janela atual (cmd.exe) para retornar o foco à ela depois de chamar os pickers 
- `maximize_console` Maxima a janela do console (cmd.exe)
- `cor` Altera cores de fonte e funto e estilos (negrito/sublinhado)

## Instalação e uso:

### Instalação
```bash
pip install lbx_toolkit
```

### Uso
```python
from lbx_toolkit import auth_EntraID, PostgreSQL, api_rest, lbx_logger, SafeLogger, ServicoWindows, ConfigManager, Servicer
```

<a id="lbxtoolkit.api_rest"></a>

# lbxtoolkit.api\_rest

<a id="lbxtoolkit.api_rest.api_rest"></a>

## api\_rest Objects

```python
class api_rest()
```

#### Classe **api_rest**

Destina-se a interatir com APIs RESTfull, em especial as publicadas pela SoftPlan para a [Plataforma Sienge](https://api.sienge.com.br/docs/).

A classe deve ser instanciada conforme sintaxe abaixo:

```python
api_rest(url, credenciais, cadencia, timeout=6, logger=None, headers={"Content-Type": "application/json"}, verify=True)
```

São nessários 2 parâmetros posicionais obrigatórios, e 5 parametros nominais facultativos (valor padrão, se omisso, indicado na sintaxe acima):
- `url`: o endereço da URL de autenticação da API
- `crednciais`: Dicionário com credenciais de autenticação. 
- `cadencia` Número máximo de chamadas *por segudo* à API 
- `timeout` Tempo máximo (segundos) para aguardar retorno à chamada. Padrão 6s, se omisso.
- `logger` O objeto _log handler_ para lidar com as informações de saída. Se não informado, todas as saídas serão direcionadas para a stdout.
- `headers` Cabeçalhos _http_ para a requisição à API.
- `verify` Verifica a validade do certificado SSL do servidor de destino da requisição.

Quanto às credenciais de autenticação, assim como a classe de interação com o PostgreSQL, elas precisam ser fornecidas na forma de um *dicionário*. 
Para o método `api_rest.aut_basic()`, o formato deve ser: 
```python
credenciais = {
                'user': 'USUARIO_API',
                'password': 'TOKEN_USUARIO'
            }
```
Caso a autenticação seja pelo método `api_rest.aut_bearer()`, o dicionário deve corresponder ao formato previsto pelo endpoint e seu conteúdo será enviado como um JSON ao endereço indicado no parametro `url`


A classe possui 3 métodos: 
- `api_rest.auth_basic()`: instanciamento da sessão autenticando pelo método HTTPBasicAuth
- `api_rest.auth_bearer()`: instanciamento da sessão autenticando pelos métodos OAuth, JWT, Bearer    
- `api_rest.endpoint_json([endereço], [método], payload=None)`: para a chamada ao endpoint
- `close()` para encerra a instância/sessão

O consumo é feito pelo método `api_rest.endpoint_json` que suporta apenas APIs cujo payload (opcional) seja aceito no formato JSON. 

Esse método espera 2 parametros posicionais obrigatórios: o endereço do endpoint e o verbo (get, post, patch ou put), tendo parametro opcional o objeto de 'payload' (json). 
Note que o endereço do endpoint deve ser informado completo. A URL informada no instanciamento da classe corresponde apenas ao endereço de autenticação. 

O tempo, em segundos, transcorrido entre a chamada a atual e a chamada anterior ao endpoint pode ser consultado pelo argumento `.Intervalo` no objeto recebido do retorno à chamada ao método `.endpoint_json`. 

Da mesma forma, o tempo de espera imposto para respeitar a cadência do webservcie também pode ser consultado pelo argumento `.Espera`.

Exemplo de uso:

```python
from lbx_toolkit import api_rest

UrlBase=r'https://api.sienge.com.br/lbx/public/api/v1'
Credenciais = {
                'user': 'USUARIO_API',
                'password': 'TOKEN_USUARIO'
            }
ApiSienge = api_rest(UrlBase,Credenciais,2.5) # limite de 2 requisições/segundo para cadência de chamada ao endpoint
Auth = ApiSienge.auth_basic()

Nutitulo=input('Numero do título:')
Nuparcela=input('Numero da parcela:')
Vencimento=input('Vencimento [AAAA-MM-DD]:')
Payload = {
                "dueDate": f"{Vencimento}"
            }
EndPoint = f'{UrlBase}/bills/{Nutitulo}/installments/{Nuparcela}'

#chama o endpoint e recebe o retorno no objeto AlteraVcto
AlteraVcto = ApiSienge.endpoint_json(EndPoint, 'patch', Payload)
```

No exemplo acima não é esperado que o endpoint retorne nenhum dado (`patch`).

Quando se usa o verbo `get` e se espera o retorno de algum dado, use o método `.json` do pacote `request` para acessar o objeto recebido.

Para uso em APIs com autenticação JWT (JSON Web Token), OAuth, Bearer Token Authentication, a construção é a mesma indicada acima, bastando-se usar `.auth_bearer()` ao invés de _.auth_basic()_, e ajustar o dicionário `credenciais` informado no instanciamento da classe, que deve ser estruturado conforme o padrão fornecido peo mantendor da API e será enviado como payload ao endpoint (`json=credenciais`).

<a id="lbxtoolkit.auth_entra_id"></a>

# lbxtoolkit.auth\_entra\_id

<a id="lbxtoolkit.auth_entra_id.auth_EntraID"></a>

## auth\_EntraID Objects

```python
class auth_EntraID()
```

#### Classe **auth_EntraID**

Este recurso tem o propósito de controlar as permissões de execução do script usando as credencias do ambiente AD em nuvem da Microsoft (Azure AD  Microsoft Entra ID), abortando se a autentição falhar ou o usuário não pertencer ao grupo.

Essa classe possui apenas dois métodos:

- `auth_EntraID.disclaimer()`: apenas exibe uma tela de informações/instruções ao usuário.
- `auth_EntraID.valida_grupo([client_id], [client_secret], [tenant_id], timeout=60, log_file='auth_EntraID.log')`: efetua a autenticação do usuário e verifica se ele pertence ao grupo informado,  abortando a execução caso não pertença ao grupo ou a autenticação não seja validada no tempo estabelecido. Os argumentos `timeout` e `log_file` são opcionais e, se omitidos, os valores aqui atribuídos serão adotados como padrão.

É necessário obter parametros da plataforma de identidade da Microsoft (AD Azure, agora Microsoft Entra ID), no [*Centro de administração do Microsoft Entra*](https://entra.microsoft.com).
Sugerimos não armazenar estas ou outras informações sensíveis no script. Considere usar o pacote `dotenv` para isso.

Os argumentos obrigatórios (posicionais) são:

1. `tenant_id` corresponde ao campo *ID do Locatário*, que pode ser obtido na página [visão geral de identidade do domínio](https://entra.microsoft.com/`blade`/Microsoft_AAD_IAM/TenantOverview.ReactView)

2. `client_id` corresponde ao *ID do aplicativo (cliente)*, obtido na secção [_Identidade  Aplicativos  Registros de Aplicativo_](https://entra.microsoft.com/`view`/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceType/Microsoft_AAD_IAM). Considere não reaproveitar aplicativos e criar um específico para essa finalidade.

3. `secret_id` corresponde ao *Valor* do _ID secreto_ (não ao próprio ID Secreto) do aplicativo. Este token não é passivel de consulta após gerado e para obtê-lo, é necessário criar um novo segredo para o aplicativo na subsecção _"Certificados e Segredos"_, após clicar no nome do aplicativo exibo na indicada no item (2). O token (_Valor do segredo_) deve ser copiado e anotado no ato da criação, pois *não é possível consultá-lo posteriormente*.


```python
from lbx_toolkit import auth_EntraID

client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'
tenant_id = 'SEU_TENANT_ID'

# inicializa instância
auth = auth_EntraID(client_id, client_secret, tenant_id, timeout=60, log_file='auth_EntraID.log')  

# exibe a mensagem padrão de aviso
auth.disclaimer()

auth.valida_grupo('Nome do Grupo de Distribuição') 
# se usuário não pertencer a grupo informado, a execução do script é abortada.
```

<a id="lbxtoolkit.config_manager"></a>

# lbxtoolkit.config\_manager

<a id="lbxtoolkit.config_manager.ConfigManager"></a>

## ConfigManager Objects

```python
class ConfigManager()
```

#### Classe **ConfigManager**

É um singleton que garante que todas as partes do código usem a mesma instância e, portanto, compartilhem a mesma configuração.

- `initialize(chave1=valor1, ..., chaveN=valorN)` : O método initialize usa **kwargs para aceitar qualquer número de pares chave-valor, armazenando-os no dicionário _config da instância.
- `get('chave')`: O método get aceita uma chave como argumento e retorna o valor correspondente do dicionário _config.
- `set('chave', valor)`: O método set permite adicionar ou atualizar dinamicamente valores no dicionário _config.
- `reset`: O método reset limpa todas as configurações armazenadas, permitindo uma nova inicialização do ConfigManager com novos valores

<a id="lbxtoolkit.lbx_logger"></a>

# lbxtoolkit.lbx\_logger

<a id="lbxtoolkit.lbx_logger.lbx_logger"></a>

## lbx\_logger Objects

```python
class lbx_logger()
```

#### Classe **lbx_logger**

Essa classe requer a importação do módulo `logging` e tem o propósito de manipular/formatar as mensagens de saída, alterando o formato e redirecionando destino padrão (stdout e stderr) para uma combinação de tela e/ou arquivo.

O comportamento padrão é registrar todas as saídas **simultaneamente** em tela e no arquivo com endereço informado no parâmetro `log_file_path`. Se este parametro for omisso no instanciamento da classe, as mensagens serão exibidas apenas na tela.

A mensagens devem ser classificadas por grau de severidade/relevância, da menor para a maior, na seguinte ordem: *debug, info, warning (aviso), error (erro), critical (critico)*

A classificação do nível de serveridade da mensagem se dá pelo método escolhido para exibir a mensagem, correspondente aos níveis de severidade equivalentes.

A classe deve ser instanciada conforme sintaxe abaixo:

```python
log = lbx_logger(log_file_path=None, log_level=logging.DEBUG, formato_log='%(asctime)s - %(levelname)s - %(message)s', modulo=None, ignore_console=None, ignore_file=None)
```

Todos os parametros são nominativos e facultativos. Em caso de omissão, os valores padrão são assumidos conforme o exemplo acima.

Os parametros para o instanciamento da classe são:

- `log_file_path`: Define o caminho e o nome do arquivo de log. Se omisso, as mensagens serão todas direcionadas apenas para a tela.
- `log_level`: Define o nível mínimo de severidade das mensagens a serem manipuladas pelo logger. Se omisso, será assumido o nível mais baixo (_debug_). As mensagens com nível abaixo do especificado são descartadas. Os níveis devem ser informados de acordo com a sintaxe acima (prefixados com _logging._ e com o nome do nível em inglês e maiúsculas). Exemplo: 
- `logging.DEBUG`: para manipular chamadas do método *.debug()* e acima.
- `logging.INFO`: para manipular chamadas do método *.info()* e acima.
- `logging.WARNING`: para manipular chamadas do método *.aviso()* e acima.
- `logging.ERROR`: para manipular chamadas do método *.erro()* e acima.
- `logging.CRITICAL`: para manipular chamadas do método *.critico()* e acima.        
- `formato_log`: Define o formato em que a mensagem será apresentada. Se omisso, o padrá é *DATA_HORA - NIVEL - MENSAGEM*. Para maiores opções veja: [Atributos de log](https://docs.python.org/3/library/logging.html#logrecord-attributes)
- `modulo`: Nome do módulo para o qual os logs serão monitorados. Permite instanciar várias vezes a classe para criar manipuladores diferentes para módulos diferente. Informe o nome do módulo para criar um log específico para ele ou simplesmente omita o parametro para criar um log para o script em geral.
- `ignore_console`: Lista com os níveis de severidade a serem ignorados para *apresentação na tela*, registrando *apenas no arquivo* (quando informado no parametro `log_file_path`) e obedecendo ao nível mínimo estabelecido no parametro `log_level`. Note que omitir o parametro `log_file_path` e incluir um nível na lsita `ignore_console` implica em ignorar/suprimir esse nível de mensagem de qualquer apresentação.
- `ignore_file`: Mesma lógica do parametro `ignore_console`, mas com lógica invertida: suprime o registro do nível do arquivo e demonstra *apenas na tela*.

1. As mensagem são manipuladas substituindo-se o comando `print()` pela chamada a um dos 5 métodos acima (_.add(), .debug(), .info(), .aviso(), .erro(), .critico()_). Exceto o método `.add()`, qualquer um dos demais métodos pode interromper a execução do script, através da passagem do parâmetro `exit`. Ao informar esse parametro na chamadada do método, atribua a ele o código de saída desejado (0 para normal, qualquer outro número para saída com erro). Exemplo:

    ```python
    log.erro('Essa mensagem apenas resulta em uma mensagem de nível ERROR')
    log.erro('Essa mensagem resulta em uma mensagem de nível ERRO e encerra o script com código de retorno -1', exit=-1)
    ```

Qualquer chamada ao comando `print()`, uma vez instanciado manipulador de log, será registada como uma chamada ao método _.info()_ e registrada com este nível de severidade. 
Para retornar ao comportamente padrão do comando print, ou interromper o manipulador, faça chamada ao método `.stop_logging()`

2. O método _.add()_ não exibe/grava imediatamente a mensagem, mas apenas a diciona a _buffer_. Todas as chamas a _.add()_ irão concatenar a mensagem recebida até a próxima chamada em algum dos níveis _.debug(), .info(), .aviso(), .erro(), .critico()_. Na primeira chama de um destes níveis após uma (ou mais) chamada(s) ao método _.add()_ o *buffer* será concatenado à mensagem recebida por um destes métodos e o resultado será manipulado pelo log conforme os parametros definidos no intanciamento da classe e o método chamado. Essa função é útil para tratar mensagens com retorno condicional. Exemplo:

    ```python
    log.add('Mensagem 1# ') ## não será exibida/registrada
    log.add('Mensagem 2# ') ## não será exibida/registrada
    log.info('Mensagem 3) ## será exibida/registrada como nível "info" e com texto: "Mensagem 1# Mensagem 2# Mensagem 3"
    ```

3. Os métodos que exibem as mensagens (`.debug()`,`.info()`,`.aviso()`, `.erro()`, `.critico()`) possuem 3 parametros: `message`, `corte=None`, `exit=None`.

    - `message`: posicional e obrigatório. corresponde à mensagem a ser exibida
    - `corte`: o tamanho máximo da mensagem a ser exibida. opcional e se omitido, exibe a mensagem inteira. se fornecido, corta a mensagem no comprimento informado
    - `exit`: opcional. se informado (requer um código de retorno), aborta o script com o código informado. se omisso (padrão) a mensagem apenas é minutada pelo log, sem interferir no funcionamento do script

4. O método `.filtra()` possui 3 parametros posicionais, todos opcionais: `log_file`, `dh_ini`, `dh_fim`.

    Se os 3 forem omitidos, serão exibidas as entradas de log do arquivo corrente, definido no instanciamento da classe `lbx_logger`, registradas na última hora. Deste modo, o valor padrão para `dh_fim` é `now()`  e para `dh_ini` é `now()` menos 1 hora.

    Caso queira filtrar os registro de outro arquivo de log, que não seja o do script corrente, informe o endereço do arquivo no primeiro parametro.

    E caso queira alterar alterar o período de filtragem, informe nos parametros 2 e 3 a data/hora de início e fim do período. Estes dois parametros aceitam tanto um objeto do tipo `datetime` como uma string (que será convertida para datetime), desde que ela esteja no formato `dd/mm/aaaa hh:mm:[ss]` (segundos são opcionais).

    Considerando que os parametros são posicionais, caso queira omitir apenas um dos parametros, preencha a posição do parametro a ser omitido com `None`.

    A saída dessa função retorna um objeto, que pode ser salvo em disco ou impresso na tela.


5. Exemplos de uso:

    ```python
    from lbx_toolkit import lbx_logger 
    import logging
    import os
    from pathlib import Path

    DirBase = Path('./')  # diretório corrente do script
    BaseName = os.path.splitext(os.path.basename(__file__))[0] # nome do script sem extensão
    LogFile = Path(DirBase, BaseName + '.log') # salva logs no diretório corrente, em um arquivo nomeado com nome do script + extensão ".log"

    ### instancia o manipulador para tratar todas as mensagens (nível DEBUG acima), 
    #   mas suprime a apresentação em tela das mensagens de nível "DEBUG" na tela, 
    #   apenas registrando-as somente no arquivo
    #   e sumprime o registro no arquivo das mensagens de nível "ERROR", 
    #   mostrando-as apenas na tela
    log = lbx_logger(LogFile, logging.DEBUG, ignore_console=[logging.DEBUG], ignore_file=[logging.ERROR]) 

    # Exemplo de mensagens de log
    log.debug('Esta é uma mensagem de debug') 
    log.info('Esta é uma mensagem informativa')
    log.add('Esta mensagem não será exibida agora, mas acumulada no buffer# ')
    log.aviso('Esta é uma mensagem de aviso')
    log.erro('Esta é uma mensagem de erro')
    log.erro('Esta é uma mensagem erro muito comprida e será limitada a 40 caracteres, o restante será cortado e ingorado ao ser manipulado', 40)
    log.critico('Esta é uma mensagem crítica')

    # Exemplo de função que gera uma exceção
    def funcao_com_erro():
        raise ValueError('Este é um erro de exemplo')

    # Testando redirecionamento de print e captura de exceção
    print('Mensagem de teste via print')
    try:
        funcao_com_erro()
    except Exception as e:
        print(f'Capturado um erro: {e}')

    log.erro('Essa é uma mensagem de erro e abortará a execução do script', exit=1)

    log.info('Essa mensagem não será exibida pois o script foi abortado na mensagem anterior')

    # obtem os registros de log da última hora (comportamento padrão)
    filtra_log = log.search() 

    # obtem os registros das últimas 6 horas
    ultimas_6h = datetime.datetime.now() - datetime.timedelta(hours=6) ## carimbo de tempo de 6 horas atrás !!! requer import datetime
    filtra_log = log.search(None, ultimas_6h) # None no 1º parametro impõe o log do arquivo corrente como padrão (definido em 'LogFile' e apontado no instanciamento da classe)

    # obtem os registros do dia 14/01/2020 até 3h atrás
    ultimas_3h = datetime.datetime.now() - datetime.timedelta(hours=3) ## carimbo de tempo de 6 horas atrás !!! requer import datetime
    filtra_log = log.search(None, '14/01/2020 00:00', ultimas_3h) # 

    # obtem os registros do horário comercial do dia 23/12/2023 do arquivo salvo em C:\temp\outro_arquivo.log
    Outro_Log = Path(r'c:\temp\outro_arquivo.log')
    filtra_log = log.search(Outro_Log, '23/12/2023 08:00', '23/12/2023 18:00') # 

    # salva conteúdo filtrado em um arquivo:
    filtrado = 'filtered_log.txt'
    with open(filtado, 'w', encoding='ISO-8859-1') as output_file:  # indique o enconding conforme salvo (UTF-8 ou ISO-8859-1)
        output_file.writelines(filta_log)    

    # mostra o conteúdo filtrado na tela
    print(''.join(filtra_log))

    # mostra o conteúdo filtrado na tela, listando apenas as os registros do nível "DEBUG"
    for line in filtered_lines:
        if "DEBUG" in line:
            print(line, end='')
    ```

<a id="lbxtoolkit.lbx_logger.SafeLogger"></a>

## SafeLogger Objects

```python
class SafeLogger()
```

Essa classe tem o propoósito de interceptar as ordens de saída (exit) disparadas pelos métodos do lbx_logger e interromper um daemon/serviço que esteja em execução antes.
Para isso, a classe precisa ser instancianda recebendo como parametros o objeto de log handler do script e o daemon do serviço a ser interrompido
O daemon, por sua vez, precisa obrigatoriamente possui um método `stop`

<a id="lbxtoolkit.misc"></a>

# lbxtoolkit.misc

<a id="lbxtoolkit.misc.misc"></a>

## misc Objects

```python
class misc()
```

#### Classe **misc**

Classe que reune pequenas funções uteis para agilizar tarefas comuns.

Sintaxe e exemplos de uso. Parametros omissos assume-se os valores padrão indicados abaixo:

- `Arquivo = seleciona_arquivo(DirBase, TiposArquivo=[('Todos os arquivos', '*.*')], Titulo='Selecionar arquivo')`
- `Diretório = seleciona_dir(DirBase=Path(r'./'), Titulo='Selecionar diretório'):`
- `NomeLimpo = normaliza('String # SEM Noção!') # string_sem_nocao`
- `cmd_window = get_cmd_window()`
- `maximize_console()`
- `print(cor('Texto branco ', 'BC') + cor('Texto preto ', 'PT'))`

<a id="lbxtoolkit.postgresql"></a>

# lbxtoolkit.postgresql

<a id="lbxtoolkit.postgresql.postgreSQL"></a>

## postgreSQL Objects

```python
class postgreSQL()
```

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

    Qualquer argumento da função `read_csv()` pode ser repassado na chamada do método.

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

    Exemplo de  uso:

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

<a id="lbxtoolkit.service"></a>

# lbxtoolkit.service

<a id="lbxtoolkit.service.Servicer"></a>

## Servicer Objects

```python
class Servicer()
```

#### Classe **Servicer**    
Classe base que implementa as rotinas padrão para a criação dameons/serviços do windows.

Os métodos padrão são `run`, `stop` e `main`, que não devem ser redefinidos/sobrecarregados. Estes métodos devem ser invocados para iniciar (`run`) e parar (`stop`) a execução do daemon/serviço. 
`main` deve ser chamada para controlar a sua execução inicial, tratando os argumentos da linha de comando.

A classe local configuradora da classe Servicer(), é quem criará o daemon de serviço.

Esta classe local precisar herdar Servicer() e sobrepor ao menos os método `on_run()` e  `args_parser()`.

O método `__ini__` da classe local deve provocar o instanciamento da classe pai com `super().__init__(Log, piddir)` e nunca sobrepor o método __init__ da classe pai, mas pode receber códigos complementares após o instanciamentod da classe pai ou através dos métodos sobrecarregáveis `on_init()`, `on_init_pre()` e `on_init_pos()`. 

Após o __init__(), defina no contexto da classe local os métodos a serem sobrecarregados em Servicer(), em seguida os métodos funcionais (o que de fato o app faz) e instancie a classe local.

Os métodos possíveis de sobrecarga em Servicer() são:
`on_stop`, `on_run`, `on_cleanup`, `args_parser`
Cada um destes métodos possuim dois metodos complementares associados, pósfixados com "pre" e "pos" (ex: `on_start_pre`, `on_start_pos`).
Estes métodos complementares permitem a injeção de código antes (pre) e depois (pós) da execução do método principal, para melhor flexibilidade e controle do fluxo do daemon


A classe base possui ainda algumas dependÊncias que precisam ser inicializadas fora do contexto da classe configuradora/local. 
Para isso, use classe ConfigManager.initialize(), disponível também no módulo `lbxtoolkit`.
O objetos mandatórios a serem inicilizados pelo **ConfigManager** são:
-    **log** = Objeto instanciado da classe lbx_logger, para manipular as entradas de log
-    **daemon** = Objeto resultante do instanciamento da própria própria classe configuradora (deve ser inicializado após o instanciamento do objeto daemon, usando `ConfigManager.set()`)
-    **config** = Dicionário contento os parametros (name, display_name e description) para instalar o serviço do windows
-    **servicepath** = Objeto do Path com o caminho deste script
-    **argparse_cfg** = Dicionário contendo os parametros de configuração (descrition, usage, add_help e formatter_classe) do módulo argparse (manipulado dos parametros de linha de comando)
-    **argparse_opt** = Lista de dicionários com a configuração do argumentos de entrada aceitos (short, long, action, help)
-    **ambiente** = Definie o ambiente de excução: Linux, Windows [console] ou Serviço [Windows]        

> [!NOTE]
> Para ser funcional, é necessária que a classe local herde essa classe base e redefina (por sobrecarga) ao menos os métodos `on_run` e `args_parser()`. 

> [!CAUTION]
> **Não inicialize diretamente a classe!!**
> Sempre crie uma classe local que herde esta classe

Exemplo de uso:

```python
import os
import platform
from pathlib import Path
from lbxtoolkit import Servicer, ServicoWindows, lbx_logger

class ServicerConfig(Servicer):        
    def __init__(self, Log=None, piddir=None):  ## Log e piddir são parametros mandatórios. outros parametros posicionais ou nominais (*args e **kwargs) pode ser adicionados aqui para serem utilizados pelos métodos locais
        super().__init__(Log=Log, piddir=piddir) ## provoca a inicialização da classe pai
        ## complete o código de instanciamento da classe aqui, se necessário
        ## os métodos on_init(), on_init_pre() e on_init_pos()
    ## SOBRECARGA DOS MÉTODOS DA CLASSE PAI 
    def on_run(self): ## mandatório. dependência de Servicer(). necessário para redefinir por sobrecarga o método que inicia o daemon.
        self.FAZ_O_QUE_PRECISA_SER_FEITO_QUANDO_DAEMON()
        # se o método on_run_pre() e on_run_pos() forem definidos, ele serão executados respectivamente antes e depois deste método, quando o método run() for chamado
        return super().on_run()            
    def on_stop(self): ## opcional. é dependência de Servicer() mas pode ser omisso se a interrupção do script não exigir nada a do que o Servicer() ja faz no método SvcStop()
        # não há necessidade de redefinir por sobrecarga o método on_stop. o comportamento padrão da classe base é suficiente. na maioria dos casos
        # mas fique livre para definir algo aqui.          
        # se o método on_stop_pre() e on_stop_pos() forem definidos, ele serão executados respectivamente antes e depois deste método, quando o método stop() for chamado
        pass
        #
        # 
    def args_paser(self): ## mandatório. dependência de Servicer(). necessário para tratar as opções/argumentos recebidos da linha de comando
        # defina argumentos de argpaser definidos no dicionário args_opt, definido fora da classe e inicializado por ConfigManager.
        if self.args.file: ## processa arquivo interativamente quando recebido paramtros '-f' ou '--file'
            Arquivo = Path(self.args.file)
            self.METODO_INTERATIVO(Arquivo)        
        if self.args.daemon: ## inicia execução como daemon quando recebido parametro '-d' ou '--daemon'        
            ServicoWindows.RunAsDaemon()
        else:
            self.parser.print_help()
        self.log.stop_logging()               
        return super().args_paser()            
    ## DEFINIÇÃO DOS MÉTODOS LOCAIS
    def FAZ_O_QUE_PRECISA_SER_FEITO_QUANDO_DAEMON(self):
        # seu código aqui
        pass
    def METODO_INTERATIVO((self, file=None)
        # seu código aqui
        pass
    # (quantos métodos locais mais forem necessários à execução do script)

    Config = { # Parametro obrigatório para a classe ServicoWindows. Deve ficar entre BaseDir e LogDaemon
                'name' : "NomeServicoWindows",    
                'display_name' : "Nome de exebição do serviço do windows",
                'description' : "Descrição da função do serviço windows"
            }        
    Ambiente = 'Linux' if  platform.system() == 'Linux' else 'Serviço' if not os.getenv('VIRTUAL_ENV') else 'Windows'
    PythonPath = Path(os.path.join(os.getenv('VIRTUAL_ENV'), 'Scripts', 'python.exe')) if os.getenv('VIRTUAL_ENV') else Path('.', '.venv' , 'Scripts', 'python.exe') 
    ServicePath = Path(os.path.abspath(__file__))
    ArgparseCfg = {
                    'description' :  f'Descreva o que o script faz',
                    'usage' : '%(prog)s [opções] [comando]',
                    'add_help' : False,
                    'formatter_class' : argparse.RawTextHelpFormatter
                    }
    ArgparseOpt = [
                        {
                            'short' : '-d', 
                            'long' : '--daemon', 
                            'action' : 'store_true', 
                            'help' : 'Executa como daemon exbindo as saídas no console (linux/windows)'
                        },
                        {
                            'short' : '-f', 
                            'long' : '--file',
                            'action' : 'store', 
                            'help' : 'Processa o arquivo indicado, mostrando os resultados no console e terminal (linux/windows)'
                        },                    
                        {
                            'short' : '-h', 
                            'long' : '--help', 
                            'action' : 'help', 
                            'help' : 'Exibe esta mensagem de ajuda'
                        }
                    ]                                        
    LogHandler = lbx_logger(LogFile, logging.DEBUG, ignore_console=[logging.DEBUG]) ## ajuste LogFile para None para desativar log e exibir tudo no console e incluia na lista ignore_console=[] os níveis de log que deseja não exibir no console
    ConfigManager.initialize(
                            log=LogHandler,
                            config=Config, 
                            ServicePath=ServicePath, 
                            argparse_cfg=ArgparseCfg, 
                            argparse_opt=ArgparseOpt,
                            ambiente=Ambiente
                            )
    Daemon = ServicerConfig(DirRetorno, Log=LogDaemon, piddir=DirPIDDaemons)
    ConfigManager.set('daemon',Daemon)

    if __name__ == "__main__":

        Daemon.main()            
```

<a id="lbxtoolkit.service.Servicer.main"></a>

#### main

```python
def main()
```

Nunca sobrecarregue esse método.
Utilize-a como função principal do seu script e definina a funcionalidade e controle a execução do script em `args_parser`

<a id="lbxtoolkit.service.Servicer.run"></a>

#### run

```python
def run()
```

Inicia a execução do do serviço. Nunca sobrecarregue esse método.

<a id="lbxtoolkit.service.Servicer.stop"></a>

#### stop

```python
def stop(evento='STOP')
```

Interrompe o daemon/serviço. Nunca sobrecarregue esse método

<a id="lbxtoolkit.service.Servicer.cleanup"></a>

#### cleanup

```python
def cleanup()
```

Método auxiliar utilizado no stop() para limpar o o PID file na interrupção. Nunca sobre carregue essa classe!

<a id="lbxtoolkit.service.Servicer.daemon_log"></a>

#### daemon\_log

```python
def daemon_log(evento=None)
```

Método auxiliar utilizado alimentar log do histórico de inicialização/interrupção do serviço/daemon. Nunca sobrecarregue esse método

<a id="lbxtoolkit.service.Servicer.on_init_pre"></a>

#### on\_init\_pre

```python
def on_init_pre()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_init_pos"></a>

#### on\_init\_pos

```python
def on_init_pos()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_init"></a>

#### on\_init

```python
def on_init()
```

Método complementar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_cleanup_pre"></a>

#### on\_cleanup\_pre

```python
def on_cleanup_pre()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_cleanup_pos"></a>

#### on\_cleanup\_pos

```python
def on_cleanup_pos()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_cleanup"></a>

#### on\_cleanup

```python
def on_cleanup()
```

Método complementar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_run_pre"></a>

#### on\_run\_pre

```python
def on_run_pre()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_run_pos"></a>

#### on\_run\_pos

```python
def on_run_pos()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_run"></a>

#### on\_run

```python
def on_run()
```

Método Principal. Deve ser **OBRIGADORIAMENTE** ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_stop_pre"></a>

#### on\_stop\_pre

```python
def on_stop_pre()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_stop_pos"></a>

#### on\_stop\_pos

```python
def on_stop_pos()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.on_stop"></a>

#### on\_stop

```python
def on_stop()
```

Método auxiliar. Deve ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service.Servicer.args_paser"></a>

#### args\_paser

```python
def args_paser()
```

Método Principal. Deve ser **OBRIGADORIAMENTE** ser sobrecarregado na classe local para funcionar.

<a id="lbxtoolkit.service_windows"></a>

# lbxtoolkit.service\_windows

<a id="lbxtoolkit.service_windows.ServicoWindows"></a>

## ServicoWindows Objects

```python
class ServicoWindows(win32serviceutil.ServiceFramework)
```

#### Classe **ServicoWindows**

Gerencia a instalação e execução de um daemon como um serviço do windows. Também assume o controle dos argumentos recebidos via linha de comando.

- `SvcInstall`: Cria um serviço do windows com base neste script
- `SvcRemove`: Remove o serviço do windows configurado à partir de `SvcInstall`
- `SvcStop`: Para/Interrompe a execução do serviço do windows criado por este script (método herdado da classe pai _win32serviceutil.ServiceFramework_ invocado automaticamente pela chamada do service manager do windows)
- `SvcDoRun`: Inicializa a execução do serviço do windows criado por este script (método herdado da classe pai _win32serviceutil.ServiceFramework_ invocado autoamticamente pela chamada do service manager do windwos)

<a id="lbxtoolkit.service_windows.ServicoWindows.SvcInstall"></a>

#### SvcInstall

```python
@staticmethod
def SvcInstall()
```

Cria um serviço do windows com base no script

<a id="lbxtoolkit.service_windows.ServicoWindows.SvcRemove"></a>

#### SvcRemove

```python
@staticmethod
def SvcRemove()
```

Remove o serviço do windows configurado à partir de `SvcInstall`

<a id="lbxtoolkit.service_windows.ServicoWindows.SvcStop"></a>

#### SvcStop

```python
def SvcStop()
```

Para/Interrompe a execução do serviço do windows criado por este script

<a id="lbxtoolkit.service_windows.ServicoWindows.SvcDoRun"></a>

#### SvcDoRun

```python
def SvcDoRun()
```

Inicializa a execução do serviço do windows criado por este script

