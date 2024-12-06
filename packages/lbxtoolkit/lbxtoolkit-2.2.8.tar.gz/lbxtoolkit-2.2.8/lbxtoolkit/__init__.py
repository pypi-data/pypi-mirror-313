"""
# **Caixa de ferramentas de automações de processo (RPA)**

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
"""
import locale
from .lbx_logger import lbx_logger, SafeLogger
from .config_manager import ConfigManager
from .service_windows import ServicoWindows
from .service import Servicer
from .auth_entra_id import auth_EntraID
from .postgresql import postgreSQL
from .api_rest import api_rest
from .misc import misc

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

__all__ = [
 "lbx_logger",
 "SafeLogger",
 "ConfigManager",
 "ServicoWindows",
 "Servicer",
 "auth_EntraID",
 "postgreSQL",
 "api_rest",
 "misc"
]
