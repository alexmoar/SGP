# SGP - Sistema Gestion de Proyectos

Version Python: `3.8`

Version django: `4.0.4`

#### Settings project

* Clone repository

```
$ git clone
$ cd sgp
```

* Build image docker

```
$ docker-compose build
```

* Up

```
$ docker-compose up
```

* Migrations

```
$ docker-compose run --rm app python manage.py makemigrations
$ docker-compose run --rm app python manage.py migrate
```

* Static files

```
$ docker-compose run --rm app ./manage.py collectstatic
```

* Create superuser

```
$ docker-compose run --rm app python manage.py createsuperuser
```


* Test

```
$ docker-compose run --rm app pytest -rA
```


Made with ♥ by [Jose Florez](www.joseflorez.co)
