# BlogNews

Este projeto foi pensado com o intuito de aprendizado através da aplicação da maioria das técnicas e funções disponibilizadas pelo Django, como modelos, views, templates, forms e etc. Além de testar em prática o conhecimento necessário para adaptar as classes disponibilizadas pelo Django ou criar classes próprias.

## Requisitos
* **Python 3.9**
* **MySQL**

## Instalação
1. Clone este repositorio em seu dispositivo através do comando
> gh repo clone MatheusSC017/BlogNews
2. Crie uma ambiente virtual em seu dispositivo
> python -m venv venv
3. Instale as bibliotecas salvas no arquivo requirements.txt, caso esteja utilizando o gerenciador de pacotes PIP você poderá utilizar o comando a seguir
> pip install -r requirements.txt

## Configuração
para realizar a configuração do site altere o arquivo Blog/blognews/settings.py ou crie um arquivo local_settings.py no mesmo diretórios, definindo os seguintes parametros

Defina a chave secreta para o site
~~~python
SECRET_KEY = 'SITE_SECRET_KEY'
~~~

Definas as configurações do e-mail para o envio da newsletter
~~~python
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_HOST = 'HOST'
EMAIL_HOST_USER = 'USER'
EMAIL_HOST_PASSWORD = 'PASSOWORD'
EMAIL_PORT = 9999
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'BLOGNEWS'
~~~

Informe a suas chaves para recaptcha ou utilize as de testes fornecidas pelo Google (SITE_KEY_GOOGLE: 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI, SECRET_KEY_GOOGLE: 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe, para mais informações acesse [Google Recaptcha](https://developers.google.com/recaptcha/docs/faq)
~~~python
RECAPTCHA_SITE_KEY = 'RECAPTCHA_SITE_KEY'
RECAPTCHA_SECRET_KEY = 'RECAPTCHA_SECRET_KEY'
~~~

Configure os provedores que serão utilizados para login, segue-se o exemplo abaixo para o provedor Google, onde deve-se informar o client_id, secret e key
~~~python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'CLIENT_ID',
            'secret': 'SECRET',
            'key': 'KEY'
        }
    }
}
~~~
 
Por ultimo configure a conexão com o banco de dados
~~~python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_database',
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    }
}
~~~

## Divisão do site

O site BlogNews é dividido em três partes:

1. **Área geral**: Disponível para o público geral, não sendo obrigatório o usuário estar logado, porém ainda com algumas limitações a serviços especificos, como comentários e pesquisas.
2. **Área para criadores de conteúdo**: Trata-se de uma área destinada a usuários com a marcação de criadores de conteúdo, onde é disponibizado a eles, páginas para criação, edição, exclusão e visualização de seus próprios Posts, albuns ou pesquisas.
3. **Área administrativa**: Trata-se de uma área para usuários com amplos poderes, onde usuários podem possuir um acesso mais profundo ao sistema de acordo com as permissões conferidas as eles por um **SuperUsuário**.

## Tipos de usuários

Os usuários do BlogNews podem ser divididos no geral em 4 grupos:

1. **Usuários finais**: São aqueles que não possuem a permissão para criar conteúdo, sendo assim, eles são limitados a apenas visualizar as informações existentes, fazer comentários ou denúncias e alterar informações próprias da conta.
2. **Criadores de conteúdos**: Possuem todos os privilegios dos usuários finais, além de poderem criar e publicar seus próprios Posts, albuns e pesquisas.
3. **Membros da Staff**: São aqueles que possuem acesso a área administrativa, porém eles estão limitados as permissões concedidas a eles pelos SuperUsuários. Sendo assim, se ele possuir permissão pode visualizar todo o contéudo do sistema, esteja ele publicado ou não, e fazer alterações ou exclusões a medida que achar necessário.
4. **SuperUsuários**: Trata-se do nível mais alto do sistema, podendo conceder permissões a si próprio e a outros usuários para assim administrar o sistema.
