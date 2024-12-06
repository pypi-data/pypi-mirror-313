# Tracebloc package
This package is pre-requiste to run tracebloc jupyter notebook.


This package helps to create and start the experiment for training ML models in 
tracebloc environment.


# Deployment Steps

Pre Requisite - Make sure you have a PyPi account and have access to tracebloc-package and tracebloc-package-dev

### Step 1 - Clean up:

Delete the following folders if they exist

- dist
- tracebloc_package.egg-info
- tracebloc_package_dev.egg-info

### Step 2 - Update Config:

Update the following details in setup.py and commit

- Version
    - As applicable

### Step 3 - Install Requirements:

```
pip install -r requirements.txt
```

### Step 4 - Build:
**For Dev**
```
python setup.py sdist
```

**For Prod/Live**
```
python setup.py sdist --live
```

### Step 5 - Upload:
```
twine upload dist/*
    username: __token__
    password: <your auth token>
```
