# PV254: [Slepé mapy](http://slepemapy.cz)

This directory contains a simple framework to build your own predictive model
working with data from [slepemapy.cz](http://slepemapy.cz). The data can be
found in another PROSO repository and you can get them by cloning the
GIT repository:

```bash
git clone https://github.com/proso/data-public.git
```

## Setup

Create virtual environment for Python 2.x and activate it:

```bash
virtualenv <directory for your environment>
source <directory for your environment>/bin/activate
```

Clone the repository:

```bash
git clone https://github.com/proso/PV254-Recommender-Systems.git
```

Install the requirements:


```bash
pip install -r <PV254 directory>/geography/requirements.txt
```

Everytime you want to use this framework you have to activate virtual environment:
```bash
source <directory for your environment>/bin/activate
```

## Basic Usage

The directory contains a simple tool `evaluate.py`. To print its help run:

```bash
python evaluate.py -h
```

### Evaluation

Place your new model to the `proso/geography/ownmodel.py` file and update the
following lines in `evaluate.py` file if you want to be able to evaluate the
model:

```python
MODELS_TO_EVALUATE = {
    'rolling_success': (ownmodel.RollingSuccessModel(), environment.InMemoryBasicEnvironment()),
    'global_succcess': (ownmodel.AverageModel(), environment.InMemoryBasicEnvironment()),
    'default': (model.DefaultModel(), environment.InMemoryEnvironment())
}
```

Your predictive model has to implement the
`proso.geography.model.PredictiveModel` and you will probably use
`proso.geography.environment.InMemoryBasicEnvironment` for storing the
auxiliary stuff.

After the above mentioned changes you can start evaluating, e.g.:
```bash
# evaluate all the given models with data from answers_train.csv and show progress bar
python evaluate.py -l answers_train.csv -p

# evaluate only the model called 'rolling_success'
python evaluate.py -l answers_train.csv -m rolling_success -p

# use only cca 10 % of data for evaluation
python evaluate.py -l answers_train.csv -s 0.1

# plot some graphs and save them to the <dest> directory
python evaluate.py -l answers_train.csv -g -d <dest>
```

### Optimization

Modify the following lines in the `evaluate.py` file if you want to naively
optimize parameters of your predictive model:

```python
MODELS_TO_OPTIMIZE = {
    'default': (model.DefaultModel, environment.InMemoryEnvironment)
}
```

After the above mentioned changes you can start optimizing, e.g.:

```bash
# Start the optimization for model called 'default' and its 2 parameters called
# 'pfae_good' and 'pfae_bad'. The bounds for the optimization are set to `[0, 10]`
# (pfa_good) and `[0, 20]` (pfae_bad). The minimal steps used by algorithm
# are 0.1 (pfae_good) and 0.2 (pfae_bad). Use only about 10 % of data and print
# progress information.
python evaluate.py -l answers_train.csv \
    -o default \
    --param_names pfae_good pfae_bad \
    --param_min 0 0 \
    --param_max 10 20 \
    --param_steps 0.1 0.2 \
    -s 0.1 -p
```