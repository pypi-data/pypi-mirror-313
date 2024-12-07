from .iqr import out  # This allows `from vijay_lib import Vijay` to work
def outlier(n):
    import numpy as np
    data = n
    
    q1= np.percentile(data,25)
    q2= np.percentile(data,50)
    q3= np.percentile(data,75)
    
    iqr = q3 - q1
    
    ub = q3 + 1.5 * iqr
    lb = q1 - 1.5 * iqr
    
    upper_value_index = np.where((data > q3) & (data < ub))
    lower_value_index = np.where((data > lb) & (data < q1))
    
    up_value = max(data[upper_value_index[0]])
    low_value = min(data[lower_value_index[0]])
    
	
    return (low_value, up_value)
