# BlogNews

This project was designed with the aim of learning through the application of most of the techniques and functions provided by Django, such as models, views, templates, forms, etc. In addition to testing in practice the knowledge needed to adapt the classes provided by Django or create my own classes.



## Requirements
* **Python 3.9**
* **MySQL**

## Quick install with Docker
1. Clone the repository on your device

2. Run the docker compose file to install the application in development mode, in this form, the basic settings have already been set and some initial data will be generated for you to test the site
> docker-compose up -d --build

## On-premises installation
1. Clone the repository on your device

2. Create a virtual environment on your device
> python -m venv venv

3. Install the libraries saved in the requirements.txt file, if you are using the PIP package manager you can use the following command
> pip install -r requirements.txt

4. The last step is to configure the settings, for this change the Blog/blognews/settings.py file or create a local_settings.py file in the same directories, defining the following parameters

Set the secret key
~~~python
SECRET_KEY = 'SITE_SECRET_KEY'
~~~

Configure email settings for sending the newsletter
~~~python
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_HOST = 'HOST'
EMAIL_HOST_USER = 'USER'
EMAIL_HOST_PASSWORD = 'PASSOWORD'
EMAIL_PORT = 9999
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'BLOGNEWS'
~~~

Enter your recaptcha keys or use the test keys provided by Google (SITE_KEY_GOOGLE: 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI, SECRET_KEY_GOOGLE: 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe, for more information visit [Google Recaptcha](https://developers.google.com/recaptcha/docs/faq)
~~~python
RECAPTCHA_SITE_KEY = 'RECAPTCHA_SITE_KEY'
RECAPTCHA_SECRET_KEY = 'RECAPTCHA_SECRET_KEY'
~~~

Configure the providers that will be used for login, follow the example below for the Google provider, where you must inform the client_id, secret and key
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
 
Finally configure the connection to the database
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
