.PHONY: test app download folders rawdata ranking h2h surfacewin database features model cleanfiles all

data/atp_data.csv: config/config.yml
	python run.py run_download_source --config=config/config.yml
download: data/atp_data.csv

data/cleaned_atp.csv: config/config.yml
	python run.py run_trimdata --config=config/config.yml
rawdata: data/cleaned_atp.csv

data/static_rankings.csv: config/config.yml
	python run.py run_rankingstable --config=config/config.yml
ranking: data/static_rankings.csv

data/atp_h2h.csv: config/config.yml
	python run.py run_h2h_record --config=config/config.yml
h2h: data/atp_h2h.csv

data/atp_winpct_surface.csv: config/config.yml
	python run.py run_surface_record --config=config/config.yml
surfacewin: data/atp_winpct_surface.csv

data/db/playerstats.db: config/config.yml
	python run.py tables_todb --config=config/config.yml --rds=False --option=H2H
	python run.py tables_todb --config=config/config.yml --rds=False --option=Ranking
	python run.py tables_todb --config=config/config.yml --rds=False --option=SurfaceWinPct 
database: data/db/playerstats.db

data/db/playerstats_rds.db: config/config.yml
	python run.py tables_todb --config=config/config.yml --rds=True --option=H2H
	python run.py tables_todb --config=config/config.yml --rds=True --option=Ranking
	python run.py tables_todb --config=config/config.yml --rds=True --option=SurfaceWinPct 
rds: data/db/playerstats_rds.db

data/atp_features.csv: config/config.yml
	python run.py run_features --config=config/config.yml
features: data/atp_features.csv

models/xgb_model.pkl: config/config.yml
	python run.py train_model --config=config/config.yml
model: models/xgb_model.pkl

cleanfiles:
	rm -r data/db data/raw data/processed data/sample
	rm -r models/xgboost

folders:
	mkdir data/db data/raw data/processed data/sample
	mkdir models/xgboost

all: download rawdata ranking h2h surfacewin database features model