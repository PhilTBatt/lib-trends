import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.models import ExponentialSmoothing
import matplotlib.pyplot as plt

js_libraries = ['react', 'webpack', 'vite', 'jest', 'express', 'vue', '@angular/core','jquery', 'next', 'lodash', 'axios',
                'moment', 'redux', 'esbuild','bootstrap', 'tailwindcss', 'postcss', 'inquirer', 'd3', 'styled-components']

js_df = pd.read_csv('javascript_download_data.csv', parse_dates=['date'], index_col='date')

js_df['library_id'] = js_df['library'].astype('category')
js_df_weekly = js_df.groupby('library').resample('W').sum(numeric_only=True).reset_index()

js_series = {
    lib: TimeSeries.from_dataframe(js_df_weekly[js_df_weekly['library'] == lib].set_index('date'), value_cols='downloads',
        static_covariates=pd.DataFrame({'library': [lib]}))
    for lib in js_libraries}

split_series = [series.split_before(0.8) for series in js_series.values()]
train_js, test_js = zip(*split_series)

model = ExponentialSmoothing()
model.fit(train_js[0])  # Train on one series first
forecast = model.predict(n=len(test_js[0]))
test_js[0].plot(label="Actual")
forecast.plot(label="Forecast")
plt.legend()
plt.show()