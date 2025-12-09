import pytest
import pandas as pd
import numpy as np
import os
import sqlite3
import gc
from unittest.mock import MagicMock, patch
from sanice import Sanice

@pytest.fixture
def dirty_df():
    data = {
        "ID": [1, 2, 3, 4, 5],
        "Value": ["R$ 100,00", "R$ 200,50", None, "R$ 50,00", "R$ 1.000.000,00"], 
        "Date Str": ["2023-01-01", "2023/01/02", "03-01-2023", "invalid", "2023-01-05"],
        "Category": ["A", "A", "B", "B", "A"],
        "Email": [" JOHN@GMAIL.COM ", "mary@outlook", "peter@uol.com.br", None, "test"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def ml_df():
    X = np.arange(100)
    y = (2 * X + 1) + np.random.normal(0, 1, 100)
    return pd.DataFrame({"feature": X, "target": y})

def test_etl_pipeline(dirty_df):
    app = Sanice(dirty_df, lang="en")
    
    (app
        .fix_columns() 
        .transform("value", "money")
        .transform("email", "email")
        .convert_date("date_str")
        .remove_nulls()
    )
    
    df = app.pegar_dataframe()
    assert df["value"].dtype == "float64"
    assert df.iloc[0]["value"] == 100.0

def test_smart_run_features():    
    df = pd.DataFrame({
        "dates": ["2022-01-01", "2022-01-02"] * 200, 
        "category": ["High", "Low"] * 200
    })
    df.to_csv("temp_smart.csv", index=False)
    
    app = Sanice("temp_smart.csv", smart_run=True)
    df_res = app.pegar_dataframe()
    
    assert "datetime" in str(df_res["dates"].dtype)
    assert str(df_res["category"].dtype) == "category"
    
    del app
    gc.collect()
    try:
        if os.path.exists("temp_smart.csv"): os.remove("temp_smart.csv")
    except PermissionError:
        pass

def test_sql_integration():
    db_name = "test_db.sqlite"
    conn = sqlite3.connect(db_name)
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_sql("test_table", conn, index=False)
    conn.close()
    
    try:
        app = Sanice.from_sql(f"sqlite:///{db_name}", "SELECT * FROM test_table", lang="en")
        assert app is not None
        app.create_column("c", "a + b")
        app.export_sql(f"sqlite:///{db_name}", "processed_table")
        
    finally:
        gc.collect()
        try:
            if os.path.exists(db_name): os.remove(db_name)
        except PermissionError:
            pass

def test_mongo_export(dirty_df):
    app = Sanice(dirty_df, lang="en")
    
    with patch("pymongo.MongoClient") as mock_client:
        mock_db = MagicMock()
        mock_col = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_col
        
        app.export_mongo("mongodb://fake", "db", "col")
        mock_col.insert_many.assert_called_once()

def test_automl_pipeline(ml_df):
    model_path = "test_model.pkl"
    try:
        app = Sanice(ml_df)
        app.auto_ml(alvo="target", tipo="regressao", salvar_modelo=model_path)
        assert os.path.exists(model_path)
    finally:
        if os.path.exists(model_path): os.remove(model_path)

def test_all_languages_aliases(dirty_df):
    languages = ["pt", "en", "zh", "hi"]
    check_commands = {
        "pt": "corrigir_colunas",
        "en": "fix_columns",
        "zh": "修正列名",
        "hi": "column_sudhare"
    }
    for lang in languages:
        app = Sanice(dirty_df, lang=lang)
        cmd = check_commands[lang]
        if not hasattr(app, cmd):
            pytest.fail(f"Missing command '{cmd}' for language '{lang}'")

def test_cli_version(capsys):
    from sanice.core import cli
    import sys
    sys.argv = ["sanice", "-v"]
    try: cli()
    except SystemExit: pass
    captured = capsys.readouterr()
    assert "Sanice v" in captured.out