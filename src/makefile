.PHONY: test app download training features model clean-tests

download:
	curl -o clouds.data https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/taylor/cloud.data

data/training.csv: config.yml
	python create_dataset.py --config=config.yml --output=data/training.csv
training: data/training.csv

data/features.csv: config.yml data/training.csv
	python generate_features.py --config=config.yml --input=data/training.csv --feature_output=data/features.csv --label_output=data/label.csv
features: data/features.csv data/label.csv

models/model.pkl: config.yml data/features.csv data/label.csv
	python modelling.py --config=config.yml --feature_input=data/features.csv --label_input=data/label.csv --model_output=models/model.pkl
model: models/model.pkl

clean:
	rm clouds.data
	rm -r data
	mkdir data
	rm -r models
	mkdir models

all: download training features model