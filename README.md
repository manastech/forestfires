# ForestFires

## Initialization
Clone the project repository into a folder of your choice within your local directory.
```bash
$ git clone https://github.com/manastech/forestfires.git
```

## Install python deps (required to run the notebooks)
Within your local project folder, run these commands.
```bash
# Install virtualenv and the python requirements
$ python3 -m pip install --user virtualenv
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt

$ deactivate
```

## Run notebooks

```bash
$ source env/bin/activate
$ jupyter lab
```
