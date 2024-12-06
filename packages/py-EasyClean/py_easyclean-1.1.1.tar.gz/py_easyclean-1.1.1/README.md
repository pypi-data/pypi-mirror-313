# EasyClean - Automated Data Preprocessing & Cleaning

**EasyClean automates data preprocessing & cleaning for your next Data Science project in Python.**

```python
pip install py-EasyClean
```

View EasyClean on [PyPi](https://pypi.org/project/py-EasyClean/).

---

## Description

Every Data Scientist knows that cleaning and preprocessing data is a big part of any project. But let’s be honest—it’s not the most fun thing to do. _What if there was a way to make it easier?_

**EasyClean** is here to help! It takes care of **preprocessing** and **cleaning** your data in Python, so you can **save time** and focus on the cool stuff in your project.

EasyClean can do things like:

- **Remove duplicates**
- Fill in **missing values**
- Spot and fix **outliers**
- **Encode** categories (OneHot, Label)
- Pull out useful info from **datetimes**

---

## Basic Usage

EasyClean takes a **Pandas dataframe as input** and has a built-in logic of how to **automatically** clean and process your data. You can let your dataset run through the default EasyClean pipeline by using:

```python
from EasyClean import EasyClean
pipeline = EasyClean(dataset)
```

The resulting output dataframe can be accessed by using:

```python
pipeline.output

> Output:
    col_1  col_2  ...  col_n
1   data   data   ...  data
2   data   data   ...  data
... ...    ...    ...  ...
```

---

## Adjustable Parameters

In some cases, the default settings of EasyClean might not optimally fit your data. Therefore it also supports **manual settings** so that you can adjust it to whatever processing steps you might need.

It has the following adjustable parameters, for which the options and descriptions can be found below:

```python
EasyClean(dataset, mode='auto', duplicates=False, missing_num=False, missing_categ=False,
          encode_categ=False, extract_datetime=False, outliers=False, outlier_param=1.5,
          logfile=True, verbose=False)
```

| Parameter        |      Type      | Default Value | Other Values                                                                                                                                  |
| ---------------- | :------------: | :-----------: | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **mode**         |     `str`      |   `'auto'`    | `'manual'`                                                                                                                                    |
| duplicates       |     `str`      |    `False`    | `'auto'`, `True`                                                                                                                              |
| missing_num      |     `str`      |    `False`    | `'auto'`, `'linreg'`, `'knn'`, `'mean'`, `'median'`, `'most_frequent'`, `'delete'`, `False`                                                   |
| missing_categ    |     `str`      |    `False`    | `'auto'`, `'logreg'`, `'knn'`, `'most_frequent'`, `'delete'`, `False`                                                                         |
| encode_categ     |     `list`     |    `False`    | `'auto'`, `['onehot']`, `['label']`, `False` ; to encode only specific columns add a list of column names or indexes: `['auto', ['col1', 2]]` |
| extract_datetime |     `str`      |    `False`    | `'auto'`, `'D'`, `'M'`, `'Y'`, `'h'`, `'m'`, `'s'`                                                                                            |
| outliers         |     `str`      |    `False`    | `'auto'`, `'winz'`, `'delete'`                                                                                                                |
| outlier_param    | `int`, `float` |     `1.5`     | any int or float, `False`                                                                                                                     |
| logfile          |     `bool`     |    `True`     | `False`                                                                                                                                       |
| verbose          |     `bool`     |    `False`    | `True`                                                                                                                                        |

---

### mode

Defines the mode in which EasyClean will run:

- **Automated processing** (`mode='auto'`): The data will be automatically analyzed and cleaned by passing through all the steps in the pipeline, with all parameters set to `'auto'`.
- **Manual processing** (`mode='manual'`): You can manually specify which processing steps EasyClean should perform. All parameters are set to `False` by default, except for the ones you define.

For example, to handle only outliers in your data and skip all other steps:

```python
pipeline = EasyClean(dataset, mode='manual', outliers='auto')
```

---

### duplicates

Defines whether EasyClean should handle duplicate values in the data. If set to `'auto'` or `True`, EasyClean will remove rows that are exact duplicates across all features. Set `duplicates=False` to skip this step.

---

### missing_num

Defines how **numerical** missing values are handled. Missing values can be predicted, imputed, or deleted. When set to `'auto'`, EasyClean attempts to predict missing values using **Linear Regression**, and any remaining values are **imputed with K-NN**.

You can specify a handling method by setting `missing_num` to: `'linreg'`, `'knn'`, `'mean'`, `'median'`, `'most_frequent'`, `'delete'`, or `False` to skip this step.

---

### missing_categ

Defines how **categorical** missing values are handled. Missing values can be predicted, imputed, or deleted. When set to `'auto'`, EasyClean attempts to predict missing values using **Logistic Regression**, with remaining values **imputed using K-NN**.

You can set `missing_categ` to: `'logreg'`, `'knn'`, `'most_frequent'`, `'delete'`, or `False` to skip this step.

---

### encode_categ

Defines how **categorical** values are encoded. EasyClean supports OneHot and Label encoding.

When set to `'auto'`, EasyClean:

- OneHot-encodes features with **less than 10 unique values**.
- Label-encodes features with **10–20 unique values**.
- Does not encode features with **more than 20 unique values**.

You can manually specify encoding using `['onehot']` or `['label']`. To encode specific columns, pass their names or indexes, e.g., `['onehot', ['column_1', 2]]`. Set `encode_categ=False` to skip this step.

---

### extract_datetime

Extracts components from datetime features into separate columns. Set `extract_datetime='s'` to extract up to seconds (day, month, year, hour, minute, second).

You can customize granularity by setting `extract_datetime` to:

- `'D'` for day
- `'M'` for month
- `'Y'` for year
- `'h'` for hour
- `'m'` for minute

Set `extract_datetime=False` to skip this step.

---

### outliers

Defines how outliers are handled. EasyClean supports two methods:

- **Winsorization** (`'winz'`): Replaces outliers with boundary values.
- **Deletion** (`'delete'`): Removes outliers entirely.

Outliers are identified using the bounds:

```python
[Q1 - 1.5*IQR , Q3 + 1.5*IQR]
```

where:

- Q1 and Q3 are the first and third quartiles of feature values.
- IQR is the interquartile range.

You can customize the bounds by changing the `outlier_param` value. It is **not recommended** to modify this.

---

### outlier_param

Allows customization of the outlier bounds by setting a value other than the default `1.5`. Use an integer or float if needed, but changes are not recommended.

---

### logfile

Determines if a logfile should be created during the EasyClean process. If `True`, a `easyclean.log` file is generated in the working directory.

---

### verbose

Controls whether process logs are displayed in real-time on the console. Set to `True` to follow the logs during execution.
