# essai

Essay scoring system web application.

## Install

The web framework is `Flask`, and the scoring module requires `scikit-learn` and `nltk` (and don't forget to download its `punkt` tokenizer).

### Install prerequisites

In order to avoid redundant and meaningless building, I strongly recommend using [miniconda](http://conda.pydata.org/miniconda.html) to manage and install pre-built binaries.

#### Install 3rd-party libraries

For spell checking and grammar checking:

Debian/Ubuntu:

```
sudo apt-get install enchant default-jdk
```

Fedora:

```
sudo dnf install enchant oracle-jdk8
```

#### Install miniconda

Download a Python 2.7 installer for your OS at [here](http://conda.pydata.org/miniconda.html).

Or download from [TUNA's mirror](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/).

#### Create virtual environment

After installing miniconda, we need to set up a virtual environment:

`conda create -n essai --file package-list.txt`

When finishing, activate it: `source activate essai`.

And you may install Python packages from pip by `pip install -r requirements.txt`.

#### Get pickles
If you want to use the scorer, you may need to train a scorer like what I did [here](https://gist.github.com/kigawas/fbc016a1dce54a8b398d) and serialize it using `pickle`.

If you want to use coherence evaluation, you may also need to do the same thing just like [coheoka](https://github.com/kigawas/coheoka).

#### Test scoring
At first, make sure the submodule is ready:
```
git submodule init
git submodule update
```

Before running this web application, you should set a environment variable like: `export CORENLP_URL=http://x.y.z:port`(e.g. http://corenlp.run, this is Stanford's official CoreNLP demo) or it will just use `localhost:9000`.

Let's check if the scorer works well:
```
python app/scoring.py
```
If any error occurs, check the instruction before. 

#### Run a server

Just `python manage.py runserver [-h $IP -p $PORT]`, if you want a faster server, try `gunicorn manage:app`.

## Features

- A holistic score from 1 to 6 (greater means better)
- Spell checking and grammar checking
- Coherence feedbacks
