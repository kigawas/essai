essai
==============
Essay scoring system web application.

##Install

The web framework is `Flask`, and the scoring module requires `scikit-learn` and `nltk` (and download its punkt tokenizer).
And you may also install `virtualenv` by using `apt-get install python-virtualenv` on Ubuntu.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements
python manage.py runserver -h $IP -p $PORT
```
