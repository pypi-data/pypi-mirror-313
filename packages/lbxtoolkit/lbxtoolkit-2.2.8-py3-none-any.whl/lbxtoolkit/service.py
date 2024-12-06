from .config_manager import ConfigManager
from .service_windows import ServicoWindows
from .lbx_logger import lbx_logger
import os
import sys
import datetime
from pathlib import Path
import platform
import socket
import argparse
import servicemanager
import win32serviceutil

class Servicer(): # Cria um daemon para rodar como serviço
    """
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
    """
    def __init__(self, Log=None, piddir=None):#TODO: ao criar uma classe padrão usar args/kwargs para lidar como parametros variáveis no instanciamento
        # PRE-REQUISITOS/DEPENDÊNCIAS: 
        self.log = ConfigManager.get('log')
        self.kwargs = ConfigManager.get('argparse_cfg')
        self.kwopts = ConfigManager.get('argparse_opt')                
        self.ambiente = ConfigManager.get('ambiente')         
        if self.log is None or not isinstance(self.log, lbx_logger):
            raise ValueError(f'Argumento "log" é mandatório e deve ser uma instância de "lbxtoolkit.lbx_logger"') 
        if self.kwargs is None:
            raise ValueError(f'Argumento "argparse_cfg" é mandatório e deve ser um dicionário com ao mínimo as chaves: [description, usage, usage, add_help, formatter_class] para configuração do módulo argpase') 
        if self.kwopts is None:
            raise ValueError(f'Argumento "argparse_opt" é mandatório e deve ser uma lista de dicionários ao mínimo as chaves: [short, long, action, help] para tratamento dos argumentos recebidos da linha de comando') 
        if self.ambiente is None or self.ambiente not in ['Linux', 'Windows', 'Serviço']:
            raise ValueError(f'Argumento "ambiente" é mandatório e deve ser uma string com um dos seguintes valores: [Linux, Windows, Serviço]') 
                
        self.on_init_pre() ## método opcional a ser definito por sobrecarga na função local

        # Argumentos padrão obrigatórios       
        self.LogFile = Path('.',os.path.splitext(os.path.basename(__file__))[0] + '.daemon') if not Log else Log
        self.OS = platform.system()
        self.PID = os.getppid()     
        self.IP = socket.gethostbyname(socket.gethostname())
        self.Host = socket.gethostname()
        self.Usuario = os.getlogin() if self.OS == 'Windows' else os.path.expanduser('~').split(r'/')[1]
        #self.Me = os.path.abspath(__file__) ## estava retornando o service.py do lbxtoolkit ao invés de retornar o script que está em execução.
        self.Me = os.path.abspath(sys.argv[0])
        self.PIDDir = Path('.') if not piddir else piddir
        self.PIDFile =  Path(self.PIDDir,str(self.PID))
        self.exit = False
        self.mode = '[DAEMON (console)]'

        self.on_init() ## método opcional a ser definito por sobrecarga na função local

        self.on_init_pos() ## método opcional a ser definito por sobrecarga na função local                
        #
        #
    def main(self):
        """ 
            Nunca sobrecarregue esse método.
            Utilize-a como função principal do seu script e definina a funcionalidade e controle a execução do script em `args_parser`
        """
        #kwargs = ConfigManager.get('argparse_cfg')
        #kwopts = ConfigManager.get('argparse_opt')                
        #ambiente = ConfigManager.get('ambiente')    

        config = ConfigManager.get('config')        

        if config is None or not 'name' in config or not 'display_name' in config or not 'description' in config:
            raise ValueError(f'Argumento "config" é mandatório e deve ser um dicionário contendo as chaves/valores para "name", "display_name" e "description"')
        elif [chave for chave in config if config[chave] is None]:
            raise ValueError(f'Argumento "config" ({config}) possui as seguintes chaves com valores inválidos [None]: {[chave for chave in config if config[chave] is None]:}')

        ServicoWindows._svc_name_ = config['name']
        ServicoWindows._svc_display_name_ = config['display_name']
        ServicoWindows._svc_description_ = config['description']        
                     
        if len(sys.argv) == 1 and self.ambiente == 'Serviço': ## VEM DAQUI https://gist.github.com/drmalex07/10554232?permalink_comment_id=2555358#gistcomment-2555358        
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(ServicoWindows)
            servicemanager.StartServiceCtrlDispatcher()
        elif len(sys.argv) > 1 and sys.argv[1] == 'install':
                ServicoWindows.SvcInstall()
        elif len(sys.argv) > 1 and sys.argv[1] == 'remove':
                ServicoWindows.SvcRemove()            
        else:
            if len(sys.argv) > 1 and sys.argv[1] in ['start', 'stop', 'restart', 'debug']:
                win32serviceutil.HandleCommandLine(ServicoWindows)
            else:        
                self.parser = argparse.ArgumentParser(**self.kwargs)
                for opt in self.kwopts:
                    self.parser.add_argument(opt['short'], opt['long'], action=opt['action'], help=opt['help'])
                self.args = self.parser.parse_args()        

                self.args_paser() ## tratamento dos arguemntos deve ser redefindo por sobrecarga no na função local
            #
            #             
    def run(self):
        """Inicia a execução do do serviço. Nunca sobrecarregue esse método."""

        self.on_run_pre() ## método opcional a ser definito por sobrecarga na função local    
        
        self.daemon_log('START')
        ## Gera o PIDFile
        self.log.add(f'Iniciando daemon [PID: {self.PID}] para monitorar os processos que rodam como serviço/daemon monitorados em: {self.PIDDir}... ')
        try:
            with open(self.PIDFile, 'w', encoding='utf-8') as f:
                f.write(self.Me + ';' + str(self.LogFile))    
        except Exception as Err:
            self.stop('CRASH')
            self.log.erro(f'Erro [{Err}] ao salvar PIDFile: {self.PIDFile}')  
        self.log.info(f'Ok!')  ## trocar para debug em prd ??

        self.on_run()  # função principal para interreper o daemon/serviço, definir localmente por sobrecarga (criar classe que herde essa classe e defina essa função)  

        self.on_run_pos() ## método opcional a ser definito por sobrecarga na função local    
        #
        #
    def stop(self, evento='STOP'):
        """Interrompe o daemon/serviço. Nunca sobrecarregue esse método"""

        self.on_stop_pre() ## método opcional a ser definito por sobrecarga na função local        

        self.daemon_log(evento)
        self.on_stop() # função principal para interreper o daemon/serviço, definir localmente por sobrecarga (criar classe que herde essa classe e defina essa função)
        self.cleanup()
        self.exit=True

        self.on_stop_pos() ## método opcional a ser definito por sobrecarga na função local        
        #
        #
    def cleanup(self): ## Elimina o arquivo PID do processo se estiver rodando como daemon
        """Método auxiliar utilizado no stop() para limpar o o PID file na interrupção. Nunca sobre carregue essa classe!"""

        self.on_cleanup_pre() ## método opcional a ser definito por sobrecarga na função local        

        if self.PIDFile: ## verifica se está rodando como daemon
            if Path(self.PIDFile).exists():
                Path(self.PIDFile).unlink()  ##exclui o pidfile do daemon se o arquivo existir        
                self.PIDFile = None

        self.on_cleanup_pos() ## método opcional a ser definito por sobrecarga na função local       
        #
        #
    def daemon_log(self, evento=None): ## Gerar log de início/interrupção do serviço
        """Método auxiliar utilizado alimentar log do histórico de inicialização/interrupção do serviço/daemon. Nunca sobrecarregue esse método"""

        evento = 'CHECK' if not evento else evento
        evento = evento.upper()
        TimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Message  = f'{TimeStamp} - {evento} - {self.OS} - {self.Host}/{self.IP} - PID: {self.PID} - {self.Usuario} - {self.Me}'
        try:
            with open(self.LogFile, 'a') as file: 
                file.write(Message + '\n') 
        except Exception as Err:
            self.log.erro(f'Erro [{Err}] ao gravar status do daemon em {self.LogFile}')                
        #
        #
    def on_init_pre(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_init_pos(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""        
        pass
    def on_init(self):
        """Método complementar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_cleanup_pre(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_cleanup_pos(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_cleanup(self):
        """Método complementar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_run_pre(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_run_pos(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_run(self):
        """Método Principal. Deve ser **OBRIGADORIAMENTE** ser sobrecarregado na classe local para funcionar."""
        pass
    def on_stop_pre(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_stop_pos(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def on_stop(self):
        """Método auxiliar. Deve ser sobrecarregado na classe local para funcionar."""
        pass
    def args_paser(self):
        """Método Principal. Deve ser **OBRIGADORIAMENTE** ser sobrecarregado na classe local para funcionar."""
        pass
    #
    #
