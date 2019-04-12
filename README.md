# Example project repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)

<!-- tocstop -->

## Project Charter 

**Vision**: To make reasonable, reliable, and fun predictions for any real or hypothetical match-ups between two ATP players

**Mission**: Enable users to select two ATP players for the singles match-up, and to input additional optional match parameters such as surface, type and stage of tournament etc., and get a prediction of how the match will go. The prediction is based on a supervised machine learning model built and validated upon historical matches.

**Success criteria**:

* Model performance: 75% cross-validated classification accuracy on the pre-trained data
* Business metrics: 30% users enter more than 1 pair of players, 10% recurrent users in a month


## Backlog
**Theme**
Help tennis enthusiasts, gamers, and column writers to discover possible directions of a tennis game with AI-powered predictions. Users can use parameters to simulate upcoming tennis matches or fantasize a hypothetical match-up between players in different eras who never played together.

**Epics**
* 1. Exploratory data analysis and data cleansing
[Backlog stories]
- a) Data overview and descriptive statistics (1 point, planned)
- b) Initial data cleaning with outliers, missing values, and other attributes (1 point, planned)
- c) Dataset transformation to make it a standard format for predictive modelling (2 points, planned) 

* 2. Model building and validation
[Backlog stories]
- a) Engineer feature set as predictor variables (4 points, planned)
- b) Split data into training and validation sets (0 point)
- c) Build an initial benchmark model for reference (1 point)
- d) Iteratively develop a set of models with engineered features, optimize parameters to find the best model (4 points)
- e) Validate the model using primary and alternative metrics (1 point)

* 3. Product development
[Backlog stories]
- a) Build data pipeline for the project (2 points??)
- b) Build user iterface prototyupe for the project (4 points??)
- c) Realize all functionality and improve user interface (8 points??)

* 4. Product tests, refinement, and roll-out
[Backlog stories]
- a) Perform tests on the use cases (4 points??)
- b) Optimize product before roll-out (4 points??)
- c) Final shipment of the product beta (2 points)

**Icebox**
- a) Include additional functionalities such as a short summary paragraph and additional statistics with the prediction
- b) Display of important preditor variables that is associated with the prediction
- c) Develop a more interactive and image-loaded user-interface for guidance
- d) Display upcoming matches according to the ATP World Tour schedule

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

