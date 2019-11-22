## Pandas 使用技巧

### 1、分组

分组&去重

```python
# 按年分组，用户id distinct
df.groupby('year').userId.nunique()
```

分组并求总和占比，见 Python/jupyter/分组并求总和占比.ipynb

### 2、json相关

读取文件，一行一个json的

```python
chunks = pd.read_json('help.json', lines=True, chunksize = 1000)
for d in chunks:
   print(d)

```

### 3、时间相关

时间戳转日期时间

doc: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html

```python
# 时间戳转datetime
df['tm'] = pd.to_datetime(df['tm'], unit='ms')
# 再转 date
df['tm'] = df['tm'].apply(lambda x: x.date())
```

