## Eazyml Augmented Intelligence
EazyML Augmented Intelligence extract insights from Dataset with certain insights
score which is calculated using coverage of that insights.

### Features
- Builds a predictive model based on the input training data, mode, and options. 
    Supports classification and regression tasks.
### APIs
It provides following apis :

1. scikit_feature_selection
    ```python
    ez_augi(mode='classification',
            outcome='target',
            train_file_path='train.csv')
