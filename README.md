essai
==============
Essay scoring system web application.

## Install

The web framework is `Flask`, and the scoring module requires `scikit-learn` and `nltk` (and don't forget to download its `punkt` tokenizer).

And you may also need to install `virtualenv` by using `apt-get install python-virtualenv` on Ubuntu beforehand.

Other packages (especially related to databases, like `psycopg2`) may also require you to install their dependencies by `apt-get`.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements
python manage.py db upgrade
python manage.py runserver -h $IP -p $PORT # or gunicorn manage:app if you want a faster server
```

Notice that installing `numpy` and `scipy` in virtual environments is not that easy.

If there are some errors like `numpy.distutils.system_info.NotFoundError: no lapack/blas resources found`, try this:
```
sudo apt-get install python-scipy
sudo apt-get build-dep python-scipy
pip install scipy
```

## Features

- A holistic score from 1 to 6 (greater means better)
- Spell checking and grammar checking
- Coherence feedbacks