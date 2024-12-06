from .lbx_logger import lbx_logger
import logging
from time import sleep, time
import validators
import requests
from requests.auth import HTTPBasicAuth

class api_rest: # Classe para interação com APIs Rest (especialmente Sienge)
    """
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

    """
    class CustomError(Exception):
        """
        Sob uma mensagem de erro customizada, exibindo a mensagem recebida como parametro.
        """
        def __init__(self, mensagem):
            self.message = mensagem
            super().__init__(self.message)


    def __init__(self, url, credenciais, cadencia=3, timeout=6, logger=None, headers={"Content-Type": "application/json"}, verify=True):
        self.logger = logger if not logger is None else lbx_logger(None, logging.DEBUG, '%(levelname)s: %(message)s') # se não fornecer o logger, vai tudo para o console

        if not validators.url(url):
            self.logger.critico('URL inválida: {url}. Primeiro parametro precisar uma URL válida. Script abortado', exit=1)
        if not isinstance(credenciais, dict):
            self.logger.critico('O segundo parametro posicional precisa ser um dicionário. Script abortado', exit=1)

        self.RetEndPoint = None  # Inicializa self.RetEndPoint como None            
        self.Headers = headers
        self.Verify = verify            
        self.Url = url
        self.Timeout = timeout
        self.Credenciais = credenciais
        self.Cadencia = 1/cadencia  ## candencia corresponde a chamadas por segundo, não minuto
        self.TempoUltReq = None 
        self.Intervalo = self.Cadencia + 1     
        #
        #
    def controla_cadencia(self): ## para controle apenas, não deve ser chamada fora da classe
        # Verificar o tempo atual
        Agora = time()
        
        # Calcular intervalo entre requisições
        if self.TempoUltReq:
            self.Intervalo = Agora - self.TempoUltReq
        else:
            self.Intervalo = float('inf')  # Primeira requisição não espera
        
        # Calcular o tempo de espera necessário para respeitar o limite
        if self.Intervalo < self.Cadencia:
            self.Espera = self.Cadencia - self.Intervalo
            sleep(self.Espera)
            return self.Espera
        else:
            self.Espera = 0
            return self.Espera, self.Intervalo
        #
        #
    def auth_basic(self): # Autentica e abre sessão na API 
        if not self.Credenciais['user'] or not self.Credenciais['password']:
            self.logger.critico('Dicionário de credenciais não possui chaves "user" e/ou "password". Script abortado', exit=1)             
        try:          
            self.Sessao = requests.Session()
            #Sessao.auth = (ApiUser, ApiPass)
            self.Sessao.auth = HTTPBasicAuth(self.Credenciais['user'], self.Credenciais['password'])
            Auth = self.Sessao.post(self.Url)  
            #print(f'Status: {Auth.status_code}')
            #print(f'Retorno: {Auth.text}')
            return self.Sessao
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}")
            return Err
        #
        #
    def auth_bearer(self): # Autentica e abre sessão na API
        #self.UrlLogin = UrlLogin if UrlLogin is not None else self.Url
        try:          
            self.Sessao = requests.Session()
            Token = self.Sessao.post(self.Url, headers=self.Headers, json=self.Credenciais, verify=self.Verify)            
            self.Headers.update({"Authorization": f"Bearer {Token.text}"})
            if 200 <= Token.status_code <= 299:
                self.Sessao.status_code = Token.status_code
                self.Sessao.token = Token.text
                return self.Sessao
            else:
                self.logger.critico(f"Erro ao autenticar API: {Token.status_code} - {Token.text}") 
                raise Exception
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}")
            return Err
        #
        #
    def auth_token(self): # Autentica e abre sessão na API
        if self.Credenciais['token']:
            Token = self.Credenciais['token']
            self.Headers.update({"UserAuthorization": f"token {Token}"})
        else:
            self.logger.critico(f'Falha de requisição api_rest.auth_token: Token não fornecido no dicionário de credenciais! Necessário informar chave da API em dicionário com chave "token" no instanciamento da classe', exit=1)
                
        try:          
            self.Sessao = requests.Session()
            Auth = self.Sessao.post(self.Url, headers=self.Headers, verify=self.Verify)            
            
            if 200 <= Auth.status_code <= 299:
                self.Sessao.status_code = Auth.status_code
                return self.Sessao
            else:
                self.logger.critico(f"Erro ao autenticar API: {self.Sessao.status_code} - {self.Sessao.text}") 
                raise Exception
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}")
            return Err
        #
        #        
    def url_request(self, metodo, payload=None): #  Efetua chamada diretamente à URL e não a EndPoint específico
        self.ult_tempo_req = time() 
        self.Metodo = metodo.lower()
        self.EndPoint = self.Url        
        self.Payload = payload
        MetodosAceitos = ['post', 'get', 'patch', 'put']
        if not any(element in self.Metodo for element in MetodosAceitos):
            self.logger.critico(f'Método {self.Metodo} não previsto. Abortando chamada!', exit=1)
        else:
            ChamadaApi = f'self.Sessao.{self.Metodo}(self.Url, timeout=self.Timeout, headers=self.Headers, verify=self.Verify)' if self.Payload is None else f'self.Sessao.{self.Metodo}(self.Url, timeout=self.Timeout, headers=self.Headers, verify=self.Verify, data=self.Payload)'
            self.controla_cadencia()
            self.TempoUltReq = time()   
            try: 
                self.RetEndPoint = eval(ChamadaApi)
                if self.RetEndPoint.status_code >= 500:
                    self.logger.critico(f'Erro [{self.RetEndPoint.status_code}] no lado servidor na resposta à requisição')   
                    raise Exception
                self.RetEndPoint.Espera = self.Espera ## adiona o tempo de espera ao retorno da API
                self.RetEndPoint.Intervalo = self.Intervalo ## adiciona o intervalo entre chamada ao retorno da API                                
                return self.RetEndPoint
            except requests.exceptions.ReadTimeout as Err:
                self.logger.critico(f'Excedido tempo limite {self.Timeout} para retorno do endpoint: {Err}\nEndpoint: {self.EndPoint}')            
                return Err
            except Exception as Err:
                self.logger.critico(f'Falha na chamada do endpoint: {Err}\nEndpoint: {self.EndPoint}\nCodigo retorno: {self.RetEndPoint.status_code}\nResposta:{self.RetEndPoint.text}')
                return self.RetEndPoint
        #
        #
    def endpoint_json(self, endpoint, metodo, payload=None): # Interage com End Point
        self.ult_tempo_req = time() 
        self.Metodo = metodo.lower()
        #self.EndPoint = self.Url + endpoint
        self.EndPoint = endpoint
        self.Payload = payload
        MetodosAceitos = ['post', 'get', 'patch', 'put']
        if not any(element in self.Metodo for element in MetodosAceitos):
            self.logger.critico(f'Método {self.Metodo} não previsto. Abortando chamada!', exit=1)
        else:
            ChamadaApi = f'self.Sessao.{self.Metodo}(self.EndPoint, timeout=self.Timeout, headers=self.Headers, verify=self.Verify)' if self.Payload is None else f'self.Sessao.{self.Metodo}(self.EndPoint, timeout=self.Timeout, headers=self.Headers, verify=self.Verify, json=self.Payload)'
            self.controla_cadencia()
            self.TempoUltReq = time()   
            try: 
                self.RetEndPoint = eval(ChamadaApi)
                if self.RetEndPoint.status_code >= 500:
                    self.logger.critico(f'Erro [{self.RetEndPoint.status_code}] no lado servidor na resposta à requisição')   
                    raise Exception
                self.RetEndPoint.Espera = self.Espera ## adiona o tempo de espera ao retorno da API
                self.RetEndPoint.Intervalo = self.Intervalo ## adiciona o intervalo entre chamada ao retorno da API                                
                return self.RetEndPoint
            except requests.exceptions.ReadTimeout as Err:
                self.logger.critico(f'Excedido tempo limite {self.Timeout} para retorno do endpoint: {Err}\nEndpoint: {self.EndPoint}')            
                return Err
            except Exception as Err:
                self.logger.critico(f'Falha na chamada do endpoint: {Err}\nEndpoint: {self.EndPoint}\nCodigo retorno: {self.RetEndPoint.status_code}\nResposta:{self.RetEndPoint.text}')
                return self.RetEndPoint
        #
        #
    def trata_erro_sienge(CodRet, Retorno):
        if not 200 <= CodRet <= 299:        
            try:
                DicRetorno = eval(Retorno.replace('null','None').replace(r'\n\t',' '))
                if 'clientMessage' in DicRetorno and DicRetorno['clientMessage'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['clientMessage']
                elif 'developerMessage' in DicRetorno and DicRetorno['developerMessage'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['developerMessage']
                elif 'message' in DicRetorno and DicRetorno['message'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['message']
                else:
                    MsgErro = Retorno
            except:
                MsgErro = Retorno.replace(r'\n\t',' ')        
            finally:
                return MsgErro
        else:
            return Retorno      
        #
        #
    def close(self): # Encerra a cessão
        self.Sessao.close()                   
        #
        #
