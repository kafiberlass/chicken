import numpy as np
import lightgbm as lgb

from sklearn.model_selection import train_test_split

def weighted_mean_absolute_error(y_true, y_pred, weights):
    return (weights * np.abs(y_true - y_pred)).mean()

def lgbm_quantile(df, alpha=0.5):
    X = df.drop(['id', 'w', 'target'], axis=1, errors='ignore')
    y = df['target']
    weights = df['w']
    
    X_train, X_val, y_train, y_val, w_train, w_val = train_test_split(
        X, y, weights, test_size=0.2, random_state=42
    )
    
    model = lgb.LGBMRegressor(
        objective='quantile',
        alpha=alpha,
        n_estimators=1000,         
        learning_rate=0.09888205171122472,
        num_leaves=64,               
        min_child_samples=74,        
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train, sample_weight=w_train)
    
    y_pred = model.predict(X_val)
    wmae = weighted_mean_absolute_error(y_val, y_pred, w_val)
    
    print(f"🎯 Квантильная регрессия (alpha={alpha}):")
    print(f"   WMAE: {wmae:.4f}")
    
    return wmae, model