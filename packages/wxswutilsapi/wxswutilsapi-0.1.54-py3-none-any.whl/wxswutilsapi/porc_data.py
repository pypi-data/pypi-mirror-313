import numpy as np
from BaselineRemoval import BaselineRemoval
from pykalman import KalmanFilter
from pykalman import KalmanFilter
from scipy.signal import savgol_filter
from numba import jit

def filter_sort(x):
    try:
        output = []
        for i in range(len(x)):
            if i<2 or (i>(len(x)-2)):
                output.append(x[i])
                pass
            else:
                a=x[i-1:i+2]
                a=np.array(a)
                a.sort()
                output.append(a[1])
                pass
            pass
        return output
    except Exception as e:
        raise ValueError(f"filter_sort:{str(e)}") from e

def remove_baseline(x,method,para):
    try:
        if len(x)<64:
            return x
        
        x = np.array(x, dtype=np.float64)
        y = []

        baseObj1 = BaselineRemoval(x)
        if method == 'ModPoly':
            output1 = baseObj1.ModPoly(para)
            y.extend(list(output1))
            pass
        elif method == 'IModPoly':
            output1 = baseObj1.IModPoly(para)
            y.extend(list(output1))
            pass
        elif method == 'ZhangFit':
            output1 = baseObj1.ZhangFit(para)
            y.extend(list(output1))
            pass
        else:
            y.extend(x)
            pass
        if len(y)>0:
            return y
        return x
    except Exception as e:
        raise ValueError(f"remove_baseline:{str(e)}") from e

def convolve( data, conv_core):
    try:
        x = np.array(data, dtype=np.float32)
        conv_core = -1.0*np.array(conv_core, dtype=np.float32)
        if conv_core.sum() != 0:
            conv_core /= conv_core.sum()

        i = len(conv_core) >> 1
        l = len(x)
        xx = [x[0]] * (len(conv_core) >> 1)
        xx.extend(x)
        xx.extend([x[-1]] * (len(conv_core) >> 1))
        y = np.convolve(xx, np.array(conv_core, dtype=np.float32), 'same')[i:i + l]

        # y = np.convolve(x, conv_core, 'same')

        return np.array(y)
    except Exception as e:
        raise ValueError(f"convolve:{str(e)}") from e
    
window_mapping = {
    4: [1, 2, 4, 2, 1],
    8: [1, 2, 4, 8, 4, 2, 1],
    16: [1, 2, 4, 8, 16, 8, 4, 2, 1],
    32: [1, 2, 4, 8, 16, 32, 16, 8, 4, 2, 1],
    64: [1, 2, 4, 8, 16, 32, 64, 32, 16, 8, 4, 2, 1]
}

def Smooth(x,position_index = 32):
    try:
        gause1_window = [1, 2, 4, 8, 16, 32, 16, 8, 4, 2, 1]
        position_index = int(position_index)
        gause1_window = window_mapping[position_index]
        y=convolve(x,gause1_window)
        return y
    except Exception as e:
        raise ValueError(f"Smooth:{str(e)}") from e


def Derivative( x):
    try:
        derivative_3point = [-0.5, 0, 0.5]
        derivative_5point = [-0.083, 0.66,0, -066.,0.083]

        y=x
        # y=self.fir(y,self.gause_window)
        # y=self.fir(y,self.gause_window)
        y = convolve(y, derivative_3point)
        # y=self.fir(y,self.gause_window)
        return y
    except Exception as e:
        raise ValueError(f"Derivative:{str(e)}") from e

def normalization(x,pos):
    try:
        res = []
        dat = x
        if pos<5 or pos>(len(dat)-5):
            th = dat[pos]
            pass
        else:
            th_data=dat[(pos-5):(pos+5)]
            th = max(th_data)
            if th == 0:
                th = sum(th_data) / len(th_data)
                pass
        a = []
        for j in range(len(dat)):
            try:
                a.append(float(dat[j]) / float(th))
            except Exception as e:
                a.append(0)
            pass
        res.extend(a)
        return res
    except Exception as e:
        raise ValueError(f"normalization:{str(e)}") from e

def snv(data):
    try:
        b=np.array(data)
        std=np.std(b)
        average=np.average(b)

        res=[]
        for i in b:
            res.append((i-average)/std)
            pass
        return np.array(res,dtype=float)
    except Exception as e:
        raise ValueError(f"snv:{str(e)}") from e

def select_range(x,parameter):
    try:
        res=x[parameter[0]:parameter[0] + parameter[1]]
        return res
    except Exception as e:
        raise ValueError(f"select_range:{str(e)}") from e

def toList(y):
    try:
        try:
            return y.tolist()
        except Exception as e:
            return  y
    except Exception as e:
        raise ValueError(f"toList:{str(e)}") from e
    
def Kalman1D(observations, damping=1):
    try:
        # To return the smoothed time series data
        observation_covariance = damping
        initial_value_guess = observations[0]
        transition_matrix = 1
        transition_covariance = 0.1
        initial_value_guess
        kf = KalmanFilter(
            initial_state_mean=initial_value_guess,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition_matrix
        )
        pred_state, state_cov = kf.smooth(observations)
        return pred_state
    except Exception as e:
        raise ValueError(f"Kalman1D:{str(e)}") from e
# 数据预处理
def proc_data(methods,x):
    try:
        if len(x) == 0:
            return x
            pass
        y = x
        for method in methods:
            if method['method'] == 'RemoveNoise':
                y = filter_sort(y)
                pass
            elif method['method'] == 'RemoveBaseline':
                y1 = []
                for parameter in method['parameters']:
                    _select_range = y[parameter['select_range'][0]:parameter['select_range'][0] +
                                                                  parameter['select_range'][1]]
                    para = parameter['parameter']
                    func = parameter['func']
                    y1.extend(remove_baseline(_select_range, func, para))
                    pass
                y = y1
                pass
            elif method['method'] == 'Smooth':
                position_index = 32
                try:
                    position_index = method['parameters']['position_index']
                except Exception as e:
                    position_index =  32
                y = Smooth(y,position_index).tolist()
                pass
            elif method['method'] == 'Derivative':
                y = Derivative(y).tolist()
                pass
            elif method['method'] == 'Select_Range':
                y = select_range(y, method['parameters'])
                pass
            elif method['method'] == 'Normalization':
                y = normalization(y, method['parameters']['position_index'])
                pass
            elif method['method'] == 'Kalman':
                y = np.array(Kalman1D(y)).reshape(-1)
                pass
            elif method['method'] == 'SNV':
                y = np.array(snv(y)).reshape(-1)
                pass
            elif method['method'] == 'Savgol_Filter':
                try:
                    parameters = {"window_length":23,"polyorder":2,"deriv":2}
                    try:
                        method_parameters = method['parameters'][0]
                        parameters['window_length'] = method_parameters['window_length']
                        parameters['polyorder'] = method_parameters['polyorder']
                        parameters['deriv'] = method_parameters['deriv']
                    except Exception as e:
                        parameters = {"window_length":23,"polyorder":2,"deriv":2}
                    y = savgol_filter(y, parameters['window_length'], parameters['polyorder'], deriv=parameters['deriv'])
                except Exception as e:
                    raise ValueError(f"Savgol_Filter:{str(e)}") from e
                pass
            pass
        result = []
        try:
            result = y.tolist()
        except Exception as e:
            result =  y
        return result
    except Exception as e:
        raise ValueError(f"proc_data:{str(e)}") from e


# 数据预处理
def wavenumber_proc_data(methods,x):
    try:
        if len(x) == 0:
            return x
            pass
        y = x
        for method in methods:
            if method['method'] == 'RemoveBaseline':
                y1 = []
                for parameter in method['parameters']:
                    x = y[parameter['select_range'][0]:parameter['select_range'][0] +
                                                                  parameter['select_range'][1]]
                    y1.extend(x)
                    pass
                y = y1
                pass
            elif method['method'] == 'Select_Range':
                y = select_range(y, method['parameters'])
            pass
        result = []
        try:
            result = y.tolist()
        except Exception as e:
            result =  y
        return result
    except Exception as e:
        raise ValueError(f"wavenumber_proc_data:{str(e)}") from e
    
@jit(nopython=True)
def iir_filter(x, k):
    # x是list类型
    x = np.array(x)
    
    # 创建与 x 相同形状的零数组
    y = np.zeros(x.shape)
    
    x_pre = x[0]  # 初始值为第一个元素
    for i in range(len(x)):
        res = np.around(np.add(np.multiply(x_pre, np.subtract(1, k)), np.multiply(x[i], k)), 3)
        x_pre = res
        y[i] = res
    
    # 结果为np类型
    return y  