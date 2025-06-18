import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.models import RNNModel
from sklearn.metrics import mean_squared_error
from darts.dataprocessing.transformers import Scaler
import matplotlib.pyplot as plt

js_libraries = ['react', 'webpack', 'vite', 'jest', 'express', 'vue', '@angular/core','jquery', 'next', 'lodash', 'axios',
                'moment', 'redux', 'esbuild','bootstrap', 'tailwindcss', 'postcss', 'inquirer', 'd3', 'styled-components']

js_df = pd.read_csv('javascript_download_data.csv', parse_dates=['date'], index_col='date')

js_series = {
    lib: TimeSeries.from_dataframe(js_df[js_df['library'] == lib].set_index('date'), value_cols='downloads',
        static_covariates=pd.DataFrame({'library': [lib]}))
    for lib in js_libraries}

temp_df = js_df[js_df['library'] == 'react'].set_index('date')
temp_series = TimeSeries.from_dataframe(temp_df, value_cols='downloads')
idk
# Check the contents and structure of the TimeSeries
print(f"Shape of the TimeSeries for 'react': {temp_series.shape}")
print(f"Values of the TimeSeries for 'react': {temp_series.values()}")

split_series = [series.split_before(0.8) for series in js_series.values()]
train_js, test_js = zip(*split_series)

model = RNNModel(model="RNN", input_chunk_length=12, n_epochs=10, add_encoders={'cyclic': {'future': ['month']}})

model.fit(train_js)
js_forecast = model.predict(n=len(test_js[0]), series=train_js)

for i, lib in enumerate(js_libraries):
    forecast_values = js_forecast[i].values()
    actual_values = test_js[i].values()

    js_mse = mean_squared_error(actual_values, forecast_values)
    print(f"Mean Squared Error (MSE) for Library {lib}: {js_mse}")
    print(f"Predictions for {lib}: {js_forecast[i].values()[0]}")

    plt.figure(figsize=(10, 6))
    test_js[i].plot(label="Actual", color='blue')
    js_forecast[i].plot(label="Forecast", color='red')
    plt.title(f"Actual vs Predicted Values for {lib}")
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Downloads')
    plt.show()