import dongsw.extension.pandas as pd
from dongsw.extension.sklearn.metrics import mean_squared_error, root_mean_squared_error_


data = pd.DataFrame({'1':[1,2,3], '2':[2,3,4]})
pd.mean_(data)
