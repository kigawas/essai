essai
==============
Essay scoring system web application.

## Install

The web framework is `Flask`, and the scoring module requires `scikit-learn` and `nltk` (and don't forget to download its `punkt` tokenizer).

### Install prerequisite

You may need to install libraries by using `apt-get install`.

```
sudo apt-get install libpq-dev python-scipy python-sklearn python-virtualenv
sudo apt-get install enchant default-jdk # for spell checking and grammar checking
```

### Run in the global environment

```
sudo pip install -v scikit-learn==0.16.1
sudo pip install -r requirements-global.txt
python manage.py db upgrade
python manage.py runserver -h $IP -p $PORT # or gunicorn manage:app if you want a faster server
```

### Run in the virtual environment

** Only do this if you have enough memory to build `numpy`, `scipy` and `scikit-learn` on your own. **

```
virtualenv venv
source venv/bin/activate
pip install -r requirements-virtual.txt
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