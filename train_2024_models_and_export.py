# from your project folder
pip install nfl_data_py xgboost scikit-learn pandas numpy joblib

python train_2024_models_and_export.py \
  --out-dir models_2024 \
  --schedule data/2025_schedule_from_grid.csv \
  --json-out data/nfl_2025_ai_predictions.json \
  --season-out 2025
