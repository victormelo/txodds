# txodds

All the requirements are on `requirements.txt`. Install them with `pip install -r requirements.txt`


To run the Producer and Consu `test_evaluation.csv`

## All the code needed to train and run your network to produce that prediction from scratch, along with instructions on how to run the code

All the code is on the file `model.py` and the dependencies to run the code is on the file `requirements.txt`. The files `train_100k.csv`, `train_100k.truth.csv`, `test_100k.csv` must be unzipped on the folder `data`

To run the code simply do:
`python model.py`

## A short description of the approach you took and how you arrived at the solution you did

My Neural Net is basically a three layer MLP with (100, 50, 20) neurons. The activation function used in the units is the ReLU. The models are trained with 250 epochs.

I trained two models.
The first model was trained with 66% of the data and tested with 34%. I did this so I could get an idea how the model would perform on a "real scenario", by that I mean evaluated with data never seen. 
The results I got with this experiment were:
```
Slope mse: 0.42872882576
Intercept mae: 5.56380679529
```
