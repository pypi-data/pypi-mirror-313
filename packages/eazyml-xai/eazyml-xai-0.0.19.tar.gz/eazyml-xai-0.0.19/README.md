## Eazyml Explainable AI
It provides explanations for a model's prediction, based on provided train and test data files.

### Features
- It provides explanations for a model's prediction, based on provided train and test data files.
### APIs
It provides following apis :

1. scikit_feature_selection
    ```python
    ez_explain(
            mode='classification',
            outcome='target',
            train_file_path='train.csv',
            test_file_path='test.csv',
            model=my_model,
            options={"data_source": "parquet", "record_number": [1, 2, 3]})
