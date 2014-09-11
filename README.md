freedom-house
=============

Local development
-----------------

Clone the repo and ensure you have python, virtualenv and pip installed. 

```bash
virtualenv env --no-site-packages
source env/bin/activate
pip install -r requirements.txt
python manage.py syncdb --all
python manage.py migrate --fake
python manage.py runserver
```

Production deployment
---------------------

Production deployment assumes you're running on heroku.

You will need

* a django secret key
* a New Relic license key

```bash
heroku create
heroku addons:add heroku-postgresql
heroku config DJANGO_DEBUG=false \
              DJANGO_COMPRESS_OFFLINE=true \
              DISABLE_COLLECTSTATIC=1 \
              DJANGO_SECRET_KEY=some-secret-key \
              NEW_RELIC_APP_NAME="Freedom House App" \
              NEW_RELIC_LICENSE_KEY=some-license-key
git push heroku master
heroku run python manage.py syncdb --all
heroku run python manage.py migrate --fake
```
