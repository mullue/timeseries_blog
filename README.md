# Time Series Blog Post
The time series blog post repo contains a series of notebooks, each of which will be used as a blog post on time series concepts. The blog series is structured as a series of increasingly more advanced concepts in time series forecasting.

## Project Structure
Each directory within this folder holds a single blog post. Each blog posts consists of a CF template to standup operational architecture for pulling in data, performing processing, training and inference. There is also an accompanying notebook, which is the same content as the blog.

## Characteristics of each blog

1. Starts with the description of a real business problem.
2. Uses a new, open, and interesting data source for a real life problem. Preferrably from AWS open data registry.
3. Introduces new ML technicques and concepts building on previous blog posts knowledge (but not same dataset or problem)
4. Has an accompanying architecture (and CF), starting simple, but becoming more complex with subsequent blogs. 
5. Is consise and easy to follow. Introduce maximum 5 new sub-topics from below per new blog.
6. Blogs are completely independent of each other, but can refer to each other to refer to concepts utilized, but not covered directly. 
7. Concludes with link to related posts in the blog series.


## Data sources and problems
* Global data set of events used for time series trend analysis of news topics: https://registry.opendata.aws/gdelt/
* Predicting weekly temperature using historical climate data: SILO climate data on AWS: https://registry.opendata.aws/silo/
* Add more here


## Possible sub-topics to be covered:

* Feature engineering
..* filling and interpolation
..* differencing
..* normalisation
..* splitting data for train and test

* Data Analysis 
..* stationarity
..* seasonality
..* trend
..* stochasticity
..* decomposition of the above
..* graphs and statistical tests for the above

* Concepts
..* forecast horizon, context length, frequency, univariate vs multivariate
..* target, exogenous and related data
..* probabalistic versus parametric
..* baseline models

* Machine learning
..* linear model baselines
..* ARIMA
..* Prophet
..* DeepAR

* Common Issues
..* amount fo samples
..* lack of historical data to capture seasonality
..* low frequency or aggregated data doesnt match desired prediction frequency
..* highly stochastic data
..* abrupt changes in the patterns of data

* Tools
..* scikit-learn, pandas
..* Gluon TS
..* Amazon Forecast

* Operations
..* data pipelines
..* retraining
..* monitoring
..* drift detection
..* integration into exsiting systems and processes
..* measuring outcomes


## Proposed Titles and Synoposis

### 1. Predicting news trends with GDELT, SageMaker processing and GluonTS
Using gluon ts, develop a linear baseline, and then an ARIMA model to predict how a topic is trending in the news.

#### Topics covered
* linear baselines
* ARIMA
* data pipelines
* graphing

### 2. Benchmarking popular time series forecasting algorithms on electricity demand forecast
Using of the Gluonts Python library in AWS Sagemaker Notebook Instance to benchmark popular time series forecast Algorithms, including ARIMA, Prophet, and DeepAR on electricity demand forecast.

#### Topics covered
* splitting data for train and test
* Naive baselines
* ARIMA
* Prophet
* DeepAR
* Gluon TS
* measuring outcomes
* graphing
