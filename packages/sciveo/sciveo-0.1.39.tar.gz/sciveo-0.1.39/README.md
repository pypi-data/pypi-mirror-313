# SCIVEO - ML/AI and Scientific tools

## Experiments Management Client
`sciveo` is a Python library that serves as a client for managing machine learning and scientific experiments on the sciveo.com platform. This library provides a convenient interface to interact with the sciveo.com API, enabling users to organize, track, and analyze their experiments efficiently.
There are few configuration params samplers, which allows easy parameter tuning. The "auto" sampler perhaps is the easiest to use, but also
"random" and "grid" ones are available.

## Monitoring client
There is also the sciveo.monitor() which will start monitoring machine CPU/RAM/GPU/NET/DISK/TEMP etc.
It is very easy to start and use.


## Features

- **Experiment Tracking:** Easily log and track your machine learning experiments.
- **Experiment Comparison:** Compare different experiments and their results.
- **Data Visualization:** Visualize experiment metrics and results.
- **Integration with sciveo.com:** Seamlessly connect and synchronize with the sciveo.com platform.
- **Monitoring machines (from HPC to jetson nano):** Visualisation and metrics collection in sciveo platform.

## Installation

 - main sciveo
pip install sciveo

 - optional for sciveo monitoring
pip install sciveo[mon]
 - optional for sciveo network tools
pip install sciveo[net]

 - for full installation
pip install sciveo[all]

## Example usage

There are few public examples in sciveo.com.

The library has local and remote mode. The local one is ready to use, but for the remote one you will need a sciveo.com account.

When have sciveo account:
```shell
sciveo init
```
Where ~/.sciveo/ path and ~/.sciveo/default file will be created. Just need to change the secret_access_key value.

or
```shell
export SCIVEO_SECRET_ACCESS_KEY='my_sciveo_user_auth_token'
```
or create a file like ~/.sciveo/some_file_name where put:
secret_access_key=my_sciveo_user_auth_token

Sciveo Monitoring cli
```shell
sciveo monitor --period 120
```

Monitoring started along with other python code.
```python
import sciveo

# Non blocking monitoring, so continue the code execution after it.
sciveo.monitor(period=120, block=False)

#rest of your python code here

```

Sciveo Scan hosts port tool available
```shell
sciveo scan --port 22 --timeout 0.5
```


Experimental Projects management

```python

# These are experiment specific imports for the demo purposes only.
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from ml.time_series import TimeSeriesTrainer, TimeSeriesPredictor

# This is the only needed import when using sciveo along with the experiment-related imports
import sciveo

def train():
    # sciveo.open() method returns current Experiment object, with its configuration sample
    with sciveo.open() as E:
        # Just an example time series trainer (using TF/Keras simple 1D conv model).
        trainer = TimeSeriesTrainer(
            ds,
            E.config.input_window, # Experiment.config is the configuration, so input_window as hyper parameter.
            E.config.input_window,
            E.config.steps # steps parameter.
        )
        trainer.create()

        history = trainer.train(E.config.max_epochs, E.config.patience)
        trainer_eval = trainer.evaluate()

        model_name, model_path = trainer.save("model-name-path.timeseries")

        # Experiment logging for everything which seems interesting for the experiment.
        E.log({"model_path": model_path})

        E.log({"train history": history.history})
        E.log({"trainer_eval": trainer_eval})

        # Plot data, various input types (dict, list etc.).
        # Showing data as charts (single and combined) and tables.
        # There is a more advanced render option which could be used for tables, charts definition.
        E.plot("train history", history.history)

        predictor = TimeSeriesPredictor(model_path)
        Y_predicted, Y_valid, x = predict_chunk(ds.dataset["test"], predictor)

        # Plot predicted and labeled
        for i, col_name in enumerate(ds.columns):
            y_predicted = Y_predicted[0,:,i].numpy().tolist()
            y_valid     = Y_valid[0,:,i].numpy().tolist()

            # Could provide x column for the plot, there are multiple options like timestamps etc.
            # The "X" is reserved for x column name, if not present default range [1, N]
            E.plot(col_name, { "predicted": y_predicted, "label": y_valid, "X": x })

        mse = mean_squared_error(y_valid, predictions)
        mae = mean_absolute_error(y_valid, predictions)
        rmse = np.sqrt(mean_squared_error(y_valid, predictions))
        r2 = r2_score(y_valid, predictions)
        mape = mean_absolute_percentage_error(y_valid, predictions)

        E.log({"R2": r2})
        E.log(f"RMSE: {rmse}")
        E.log("MAPE", mape)
        E.log("R2", r2, "RMSE", rmse, "MAPE", mape)

        # There is a sorting option for the Project's experiments
        # By default it is "score", so there is a method Experiment.score() which could be used for experiments evaluation.
        E.score(100 - mape)
        # There is explicit Experiment "eval" section where all available evaluation metrics could be logged.
        E.eval("R2", r2)
        E.eval("RMSE", rmse)
        E.eval("MAPE", mape)


# Configuration of the Project's experiments run.
configuration = {
    "input_window": {
        "values": [10, 20, 30, 40, 50, 100, 200] # "values" option provides selection from a list of values.
    },
    "steps": {
        # "min"/"max" is a range of values where sampling will get next value.
        # It is int/float sensitive, so if range is [1, 100], the sampled value will be integer.
        # If range is [1.0, 100.0], sampling float values.
        "min": 1, "max": 100
    },
    "max_epochs": (10, 50), # Same range of values but using a tuple (min, max).
    "patience": (1, 3),
    "idx": {
        "seq": 1 # Sequence sampling, so just increase it on every run, could be used as experiment index.
    }
}

# Dataset info
sciveo.dataset({"name": "EURUSD60.csv", "split": ds.ratios}) # any dict with params.

# sciveo.start() method starts the Project's experiments run.
sciveo.start(
    project="TimeSeriesTrainer param tune", # Project name, could be existing or a new one.
    configuration=configuration, # The hyper param configuration
    function=train, # Function which will be executed on every loop.
    remote=True, # There are 2 modes: local and remote. For remote option there is a need of sciveo.com authentication.
    count=20, # Number of experiments which will be run.
    sampler="random" # Configuration sampling method, options currently are "random" (by default), "grid" and "auto".
)

```




### Who do I talk to? ###

* Pavlin Georgiev
* pavlin@softel.bg