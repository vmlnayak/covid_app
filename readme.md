## Django_rest_covid_data_fetch_app
### clone the project by using
```sh
git clone https://github.com/vmlnayak/covid_app.git
```
## Installation
#### Create the virtual environment

```sh
virtualenv venv
```
#### Activate the virtual environment
##### for MAC OS

```sh
source mypython/bin/activate
```
##### for windows

```sh
venv\Scripts\activate
```
##### Note: You can deactivate the venv by deactivate

```sh
pip install -r requirements.txt
```
Apply this command to load country data before running application. 
```
python manage.py loaddata  api/fixture/country_list.json
```

### This Application required django, Python, Celery and other tools mentioned in requirements.txt file. 
Run application using below command.
```sh
python manage.py runserver
```
## API Documentation 

[python] - <https://docs.python.org/3.9/>
[Django] - <https://docs.djangoproject.com/en/3.2/>
[Django Rest] - <https://www.django-rest-framework.org/>
