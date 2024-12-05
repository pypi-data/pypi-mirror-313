import numpy as np
from sklearn.calibration import cross_val_predict
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error

def optimise_pls_cv(n_components,x, y, n_comp):  # pls�㷨
    try:
        mse = []
        if n_components == 0:
            component = np.arange(1, n_comp)
            for i in component:
                pls = PLSRegression(n_components=i)
                y_cv = cross_val_predict(pls, x, y, cv=8)
                mse.append(mean_squared_error(y, y_cv))
            MSE_MIN = np.argmin(mse)
            MSE_MIN += 1
            pass
        else:
            MSE_MIN = n_components
            pass
        pls_opt = PLSRegression(n_components=MSE_MIN)
        y, x = zip(*[(a, b) for a, b in zip(y, x) if a is not None])
        y=list(y)
        x=list(x)
        pls_opt.fit(x, y)
        return pls_opt, pls_opt.predict(x)
    except Exception as e:
        raise ValueError(f"optimise_pls_cv:{str(e)}") from e