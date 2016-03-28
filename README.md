essai
==============
Essay scoring system web application.

## Install

The web framework is `Flask`, and the scoring module requires `scikit-learn` and `nltk` (and don't forget to download its `punkt` tokenizer).

And you may also need to install `virtualenv` by using `apt-get install python-virtualenv` on Ubuntu beforehand.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements
python manage.py runserver -h $IP -p $PORT
```
