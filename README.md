# BlogNews

This project was designed with the aim of learning through the application of most of the techniques and functions provided by Django, such as models, views, templates, forms, etc. In addition to testing in practice the knowledge needed to adapt the classes provided by Django or create my own classes.



## Requirements
* **Python 3.9**
* **MySQL**

## Installation

### Quick install with Docker
#### Installation for Development mode
1. Clone the repository on your device

2. Create a .env.dev file with the website configuration, for development purposes you can use the example below:
~~~
SECRET_KEY=secret_key_for_use_in_docker_change_me
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:1337 http://127.0.0.1:1337

EMAIL_BACKEND=django.core.mail.backends.dummy.EmailBackend
EMAIL_HOST=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='BlogNews'

RECAPTCHA_SITE_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_SECRET_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
RECAPTCHA_SITE_KEY_TEST=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_SECRET_KEY_TEST=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe

SQL_ENGINE=django.db.backends.mysql
SQL_DATABASE=blog_database
SQL_USER=blog_database_user
SQL_PASSWORD=blog_database_password
SQL_HOST=db
SQL_PORT=3306

DATABASE=mysql
INITIAL_DATA=True
~~~

3. Run the docker compose file to install the application in development mode, in this form, the basic settings have already been set and some initial data will be generated for you to test the site
> docker-compose up -d --build

### On-premises installation
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

## Structure

### Site division

The BlogNews website is divided into three parts:

1. **General area**: Available to the general public, it is not mandatory for the user to be logged in, but still with some limitations to specific services, such as comments and searches.
2. **Area for content creators**: This is an area intended for users marked as content creators, where pages are available for creating, editing, deleting and viewing their own Posts, albums or searches.
3. **Administrative area**: This is an area for users with broad powers, where users can have deeper access to the system according to the permissions granted to them by a **SuperUser**.

### Types of users

BlogNews users can be broadly divided into 4 groups:

1. **End users**: They are those who do not have permission to create content, therefore, they are limited to only viewing existing information, making comments or complaints and changing their own account information.
2. **Content creators**: They have all the privileges of end users, in addition to being able to create and publish their own Posts, albums and surveys.
3. **Staff members**: They are those who have access to the administrative area, but they are limited to the permissions granted to them by Super Users. Therefore, if he has permission, he can view all the system's content, whether published or not, and make changes or deletions as he deems necessary.
4. **Superusers**: It is the highest level of the system, being able to grant permissions to itself and other users to administer the system.
