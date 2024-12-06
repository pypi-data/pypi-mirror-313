import os
import sys
import re 
import datetime
import logging
from pathlib import Path

class lbx_logger: # Classe para gerenciar a saída para log
    r"""
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
    """    
    class LevelFilter(logging.Filter):    
        def __init__(self, levels_to_ignore):
            self.levels_to_ignore = levels_to_ignore
            #
            #         
        def filter(self, record):
            return record.levelno not in self.levels_to_ignore
            #
            #
    def __init__(self, log_file_path=None, log_level=logging.DEBUG, formato_log='%(asctime)s - %(levelname)s - %(message)s', modulo=None, ignore_console=None, ignore_file=None):
        self.ignore_file = [] if ignore_file is None else ignore_file       
        self.ignore_console = [] if ignore_console is None else ignore_console
        self.modulo = __name__ if modulo is None else modulo
        self.logger = logging.getLogger(self.modulo)
        self.logger.setLevel(log_level)
        self.msg = ''
        self.log_file_path = log_file_path
        
        if log_file_path:
            # Criando um handler para escrever em um arquivo de log
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(log_level)  # Sempre registrar tudo no arquivo
            
            # Criando um handler para exibir no console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)  # Registrar DEBUG e acima no console
            
            # Adicionando filtro para ignorar certos níveis no console e no arquivo
            file_handler.addFilter(self.LevelFilter(self.ignore_file))
            console_handler.addFilter(self.LevelFilter(self.ignore_console))

            # Definindo o formato das mensagens de log
            formatter = logging.Formatter(formato_log)
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Adicionando os handlers ao logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        else:
            # Tudo direcionado para o console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)  # Registrar no console
            
            # Adicionando filtro para ignorar certos níveis no console e no arquivo
            console_handler.addFilter(self.LevelFilter(self.ignore_console))        

            # Definindo o formato das mensagens de log
            formatter = logging.Formatter(formato_log)
            console_handler.setFormatter(formatter)
            
            # Adicionando o handler ao logger
            self.logger.addHandler(console_handler)
        
        # Redirecionando exceções para o logger
        sys.excepthook = self.handle_exception
        
        # Redirecionando saída padrão
        self.original_stdout = sys.stdout
        sys.stdout = self
        #
        #
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("Exceção não prevista", exc_info=(exc_type, exc_value, exc_traceback))
        #
        #
    def input(self, prompt=''):
        """
        Método personalizado para capturar entrada sem interferência do logger.
        Temporariamente restaura o stdout original.
        """
        # Restaurar stdout para o original
        sys.stdout = self.original_stdout
        
        # Capturar entrada do usuário
        user_input = input(prompt)
        
        # Voltar a redirecionar stdout para o logger
        sys.stdout = self
        
        return user_input
        #
        #
    def print(self, *args, **kwargs):
        # Imprime diretamente na saída padrão
        print(*args, **kwargs, file=self.original_stdout)
        #
        #
    def add(self, message, corte=None):
        message = message[:corte] if corte else message
        self.msg = self.msg + message if not message is None else self.msg
        #
        #     
    def write(self, message):
        if message.strip():  # Ignorar mensagens vazias
            self.logger.info(message.strip())
        #
        #
    def flush(self):
        pass  # Método necessário para compatibilidade com sys.stdout
        #
        #
    def debug(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.debug(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def info(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.info(msg)
        self.msg = ''
        if exit:
            os._exit(exit)        
        #
        #     
    def aviso(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.warning(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def erro(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.error(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def critico(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.critical(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def stop_logging(self):
        # Restaurar o stdout original
        sys.stdout = self.original_stdout
        # Remover handlers do logger
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
        #
        #
    def filtra(self, log_file, dh_ini, dh_fim):
        # Validar parametros de entrada
        if dh_ini:
            if not isinstance(dh_ini, datetime.datetime):
                if not re.fullmatch(r'([0-3][0-9]/[0-1][0-2]/[1-2][0-9]{3} [0-2][0-9]\:[0-6][0-9])(\:[0-6][0-9]){0,1}', dh_ini):
                    self.logger.error(f'Data/Hora início {dh_ini} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None                
                elif len(dh_ini) == 16:  # Formato 'dd/mm/yyyy hh:mm'
                    dh_ini += ":00"
                try:
                    self.inicio = datetime.datetime.strptime(dh_ini, '%d/%m/%Y %H:%M:%S')
                except:
                    self.logger.error(f'Data/Hora início {dh_ini} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None
            else:
                self.inicio = dh_ini
        else:
            self.inicio = datetime.datetime.now() - datetime.timedelta(hours=1) ## assume a última hora como intervalo, se omisso

        if dh_fim:
            if not isinstance(dh_fim, datetime.datetime):
                if not re.fullmatch(r'([0-3][0-9]/[0-1][0-2]/[1-2][0-9]{3} [0-2][0-9]\:[0-6][0-9])(\:[0-6][0-9]){0,1}', dh_ini):
                    self.logger.error(f'Data/Hora fim {dh_fim} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None                
                elif len(dh_fim) == 16:  # Formato 'dd/mm/yyyy hh:mm'
                    dh_fim += ":00"
                try:
                    self.fim = datetime.datetime.strptime(dh_fim, '%d/%m/%Y %H:%M:%S')
                except:
                    self.logger.error(f'Data/Hora fim {dh_fim} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None
            else:
                self.fim = dh_fim
        else:
            self.fim = datetime.datetime.now() ## assume a última hora como intervalo, se omisso

        if not log_file and not self.log_file_path:
            self.logger.critical('Nenhum arquivo de log disponível. Log desta instância configurado apenas para exibição em tela, sem registro em arquivo')
            return None
        elif not log_file and self.log_file_path:
            log_file_path = self.log_file_path
        elif log_file:
            if Path(log_file).is_file():
                log_file_path = log_file
            else:
                self.logger.critical(f'Arquivo de log {log_file} não existe!')
                return None
        else:
            self.logger.critical('Erro validação arquivo de entrada. Abortando!')
            return None
                   
        # Função para verificar se a linha está dentro do intervalo de tempo
        def is_within_time_range(timestamp, dh_inicio, dh_fim):
            return dh_inicio <= timestamp <= dh_fim

        # Ler e filtrar o arquivo de log com a codificação ISO-8859-1
        with open(log_file_path, 'r', encoding='ISO-8859-1') as log_file:
            log_lines = log_file.readlines()

        # Variável para armazenar o último timestamp válido
        last_valid_timestamp = None
        filtered_lines = []

        for line in log_lines:
            try:
                # Extraia a data e a hora da linha
                timestamp_str = line.split()[0] + " " + line.split()[1]
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                last_valid_timestamp = timestamp
                if is_within_time_range(timestamp, self.inicio, self.fim):
                    filtered_lines.append(line)
            except Exception as e:
                # Caso a linha não tenha um carimbo de tempo, use o último timestamp válido
                if last_valid_timestamp and is_within_time_range(last_valid_timestamp, self.inicio, self.fim):
                    filtered_lines.append(line)

        # Retornar o objeto contendo as linhas filtradas
        return filtered_lines
        #
        #         
class SafeLogger: ## intercepta as entradas de log para parar o daemon/watcher quando parametro EXIT existir
    """
    Essa classe tem o propoósito de interceptar as ordens de saída (exit) disparadas pelos métodos do lbx_logger e interromper um daemon/serviço que esteja em execução antes.
    Para isso, a classe precisa ser instancianda recebendo como parametros o objeto de log handler do script e o daemon do serviço a ser interrompido
    O daemon, por sua vez, precisa obrigatoriamente possui um método `stop` 
    """
    def __init__(self, logger, daemon):
        self.log = logger # recebe o objeto do log
        self.daemon = daemon # recebe o objeto do watchdog (daemon)
        #self.Args = args # recebe os argumentos da linha de comando (para saber se está rodando como daemon ou interativo)
        #
        #
    def __getattr__(self, name):
        # Este método é chamado quando um método inexistente é chamado na classe
        # Ele repassa a chamada para o logger original, aplicando a lógica de exit
        original_attr = getattr(self.log, name)

        if callable(original_attr):
            def wrapper(*args, **kwargs):
                #if 'exit' in kwargs and (Args.d or not (Args.d or Args.f)): #não tentar para o daemon se execucção interativa
                if 'exit' in kwargs and isinstance(kwargs['exit'], int) and self.daemon: #não tentar para o daemon se execucção interativa
                    if not self.daemon.exit:  # Verifica se o daemon já foi interrompido
                        evento = 'CRASH' if kwargs['exit'] != 0 else 'STOP'
                        msg1 = 'um erro ocorreu. Interceptando log para interromper daemon/watcher...' if kwargs['exit'] != 0 else \
                            'Interrompendo daemon/watcher...'
                        msg2 = 'daemon/watcher interrompido... exibindo o erro interceptado: ' if kwargs['exit'] != 0 else \
                            'daemon/watcher interrompido!'
                        
                        self.log.aviso(msg1)
                        self.daemon.stop(evento)
                        self.log.aviso(msg2)

                result = original_attr(*args, **kwargs)
                return result            
            return wrapper
        else:
            return original_attr
        #
        #