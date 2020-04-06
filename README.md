# COVID-19 NZ Data Processing

A simple script to automatically fetch, process, and plot the NZ covid-19 cases data from the Ministry of Health's website (https://health.govt.nz).

Getting started:
- 
Dependencies:
- pandas
- requests
- xlrd
- beautifulsoup4
- matplotlib

Simply run:

`pip install git+https://github.com/ABI-Covid-19/moh-data.git`

Example of usage:

```python
from src.moh_data.main import Basic
import matplotlib.pyplot as plt

run_data = Basic()
run_data.plot_daily_trend()
run_data.plot_cumulative_sum()

plt.show()

```

Running the above code in a file should produce the following two figures:

![alt text](resources/Figure_1.png)

![alt text](resources/Figure_2.png)