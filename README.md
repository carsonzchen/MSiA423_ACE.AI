# ACE.AI - project repository

**Developer: Carson Chen**

**QA: Shreyas Sabnis**

## Midproject PR update and instructions

**0. Set up environment**

a) The environment_windows.yml or environment_linux.yml file contains the packages required to run the model code, depending on if you are running it on a windows or linux machine. You need to use conda to setup the virtual environment. The default environment name is ace. You may replace it with another environment name of your choice.

###### conda env create --name ace -f environment_xxx.yml
###### conda activate ace

b) AWS RDS configuration

Update 'config/.mysqlconfig' to configure update environment variables MYSQL_USER and MYSQL_PASSWORD for your RDS instance, then from the main folder, add the above environments to your bash profile (linux) by running:

###### echo '/config/.mysqlconfig' >> ~/.bashrc
###### source ~/.bashrc

Also, update 'src/config' file to configure your RDS
* RDS_HOST -> The endpoint of your RDS instance
* RDS_PORT -> The port number associated with your RDS instance

**1. Script that acquires data from data source and puts it into S3**
* Run 'src/upload_data.py', provide your own bucket name, in the main path. Raw data will save as 's3://<your_bucket_name>/data/atp_data.csv'.

###### python src/upload_data.py --bucket <your_bucket_name>

**2. Script that creates prediction database schema in RDS**
* Run 'src/create_db_rds.py'

###### python src/create_db_rds.py

## Project Directory
<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)

<!-- tocstop -->

## Project Charter 

**Vision**: To make reasonable, reliable, and fun predictions for any real or hypothetical match-ups between two ATP (Association of Tennis Professionals) players

**Mission**: Enable users to select two ATP players for the singles match-up, and to input additional optional match parameters such as surface, type and stage of tournament etc., and get a prediction of how the tennis match will go - who wins, in how many sets, and the associated probabilities. The prediction is based on a supervised machine learning model built and validated upon historical matches.

**Success criteria**:

* Model performance: 75% cross-validated classification accuracy on the training data (Met)
* Business metrics: 30% users enter more than 1 pair of players, 10% recurrent users in a month

**Data source**:
All ATP matches between 2000 and March 2018, compiled by Edouard Thomas on Kaggle.com

https://www.kaggle.com/edouardthomas/atp-matches-dataset

## Backlog

**Theme**

Help tennis enthusiasts, gamers, and column writers to discover possible directions of a tennis game with AI-powered predictions. Users can use parameters to simulate upcoming tennis matches or fantasize a hypothetical match-up between players in different eras who never played together.

**Epics**

* 1. Exploratory data analysis and data cleansing
* Backlog stories
- a) Data overview and descriptive statistics (1 point)
- b) Initial data cleaning with outliers, missing values, skewness, and imbalance (1 point)
- c) Dataset transformation to make it a standard format for predictive modelling (2 points) 

* 2. Model building and validation
* Backlog stories
- a) Engineer feature set as predictor variables (4 points)
- b) Split data into training and validation sets (0 point)
- c) Build an initial benchmark model for reference (1 point)
- d) Iteratively develop a set of models with engineered features, optimize parameters to find the best model (8 points)
- e) Validate the model using primary and potential alternative metrics such as F1-score (1 point)

* 3. Product development
* Backlog stories
- a) Build data pipeline for the project (2 points)
- b) Build user iterface prototype for the project (4 points)
- c) Realize all functionality and improve user interface (8 points)
- d) Initialize database in RDS (1 point)

* 4. Product tests, refinement, and roll-out
* Backlog stories
- a) Perform tests on the use cases (4 points)
- b) Optimize product before roll-out (4 points)
- c) Final shipment of the product beta (2 points)

* Realized icebox stories
- a) Include additional functionalities such as a short summary paragraph and additional statistics with the prediction
- b) Display of important predictor variables that is associated with the prediction
- c) Develop a more interactive and image-loaded user-interface for guidance

**Icebox**
* epic
- Deploy model with Flask

* stories
- d) Display upcoming matches according to the ATP World Tour schedule

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── score_model_db.py             <- Script for scoring new predictions using a trained model
│   ├── app.py                        <- Script for running the flask app
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│   ├── config.yml                    <- Configuration files for reproduceable and modularized data pipeline settings and parameters
│   ├── flask_config.py               <- Configuration files for the app and databases
│
├── data                              <- Folder that contains data used or generated. Only the sample/ subdirectories are tracked by git. 
│   ├── db/                           <- Place to put local sqlite database 
│   ├── processed/                    <- Place to put processed intermediate data tables 
│   ├── raw/                          <- Place to put raw data downloaded from websites
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
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
│   ├── create_db.py                  <- Script for creating a sqlite (or rds) database and add tables to it 
│   ├── download_upload_data.py       <- Script for ingesting data from different sources and upload them to S3 to store
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── evaluate_model.py             <- Script for evaluating the performance of trained model
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── preprocess.py                 <- Script for preprocessing raw data
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── makefile                          <- Simplifies the execution of run.py file in bash script
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── config.py                         <- Configuration file for Flask app
├── environment_linux.yml             <- Python package dependencies for linux system
├── environment_windows.yml           <- Python package dependencies for windows system
```
