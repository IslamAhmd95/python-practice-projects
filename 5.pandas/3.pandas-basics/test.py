import pandas as pd
import seaborn as sns
import numpy as np

# df = sns.load_dataset('penguins')

# data = {'first': [1, 2, 3, 4], 'second': [5, 6, 7, 8]}
# df = pd.DataFrame(data=data, index=['a', 'b', 'c', 'd'])
# df.iloc[0, 0] = 15
# print(df) 

# df.to_csv('data/new.csv')
# df = pd.read_csv('data/new.csv', index_col=0)
# df.index = ['a', 'b', 'c', 'd']
# print(df)

# df.to_json('data/new.json')
# df = pd.read_json('data/new.json')
# df.index = df['first']
# print(df.info())
# print("-" * 50)
# print(df.describe()['first']['25%'])


# data = [('a', 1), ('b', 2), ('c', 3), ('a', 4)]
# df = pd.DataFrame(data, index=['a', 'b', 'c', 'a'])
# print(df)



# df = pd.DataFrame({
#     "name": ["Alice", "Bob", "Charlie", "David"],
#     "score": [85, 90, 78, 92]
# })

# multi_index = pd.MultiIndex.from_tuples([('a', 1), ('b', 2), ('c', 3), ('a', 2)], names = ['letters', 'numbers'])
# df.index = multi_index
# df.to_csv('data/new.csv')
# df = pd.read_csv('data/new.csv')
# df.set_index(['letters', 'numbers'], inplace=True)
# print(df)


# print(df.iloc[:, 0])

# print("-" * 50)

# df1 = df.loc[df['score'] > 70].sort_index(ascending=[False, True])
# print(df1)
# print("-" * 50)
# df2 = df.loc[df['score'] > 70].sort_values(by=['name', 'score'], ascending=[False, True])
# print(df2)
# print(df1.index.names)




# print(df.corr(numeric_only=True))


# df.reset_index(drop=True, inplace=True)
# multi_index = pd.MultiIndex.from_tuples([('b', 1), ('a', 2), ('c', 3), ('d', 4)], names = ['letters', 'numbers'])
# df.index = multi_index
# df = df.reset_index().drop(['letters', 'numbers'], axis=1)
# print(df)
# df = df.sort_index()
# df['all_score'] = df['score'] * 2
# df1 = df.loc['a':'b', 'name': 'all_score']
# print(df1)



# df = pd.DataFrame({
#     "name": ["Alice", "Bob", "Charlie", "David", None],
#     "age": [25, None, 30, 22, 28],
#     "score": [85, 90, np.nan, 70, 88],
#     "city": ["Cairo", "Alex", "Giza", None, "Cairo"]
# })

# df1 = df.isnull().values.all()
# print(df1)


# data = {
#     'name': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
#     'city': ['Cairo', 'London', 'Cairo', 'London', 'London'],
#     'score': [85, 90, 78, 95, 88]
# }

# df = pd.DataFrame(data)

# df1 = df.groupby(['city']).agg({
#     'score': ['mean', 'sum'],
#     'name': lambda x: ', '.join(sorted(set(x)))
# })
# df1.columns = ['name' if col == ('name', '<lambda>') else '_'.join(col) for col in df1.columns if isinstance(col, tuple)]
# df1 = df1.reset_index().sort_values('score_mean', ascending=True)
# print(df1)

# customers = pd.DataFrame({
#     'CustomerID': [1, 3, 4],
#     'Name': ['Alice', 'Bob', 'Charlie']
# })

# orders = pd.DataFrame({
#     'OrderID': [101, 102, 103],
#     'CustomerID': [1, 2, 2],
#     'Amount': [250, 150, 300]
# })

# df = pd.merge(orders.set_index('CustomerID'), customers.set_index('CustomerID'), left_index=True, right_index=True)
# print(df)
# df = pd.concat([customers, orders], axis=0, ignore_index=True)
# print(df)

# data = {
#     'Name': ['Alice', 'Bob', 'Charlie'],
#     'Date': ['2023-05-01', '2023-05-02', '2023-05-31'],
#     'Score': [85, 90, 78]
# }

# df = pd.DataFrame(data, index=['a', 'b', 'c'])
# df['Date'] = pd.to_datetime(df['Date'])
# df['day_name'] = df['Date'].dt.day_name()
# df['month_name'] = df['Date'].dt.month_name()
# df['month'] = df['Date'].dt.month
# df['monthEnd'] = df['Date'].dt.is_month_end
# print(df)
# print("-" * 60)
# print(df[df['Date'] > '2023-06-01'])


# print(df['Date'].dtype)


# dates = pd.date_range(start='2023-01-01', end='2023-05-01', freq='MS')
# df = pd.DataFrame(dates, columns=['date'], index= range(len(dates)))
# df['value'] = [10, 20, 30, 40, 50]
# df['date'] = pd.to_datetime(df['date'])
# df.set_index('date', inplace=True)
# df1 = df.resample('YE').mean()
# print(df1)
# df2 = df.resample('D').ffill()
# print(df2)

# df.reset_index(inplace=True)
# df['rolling_avg'] = df['value'].rolling(window=3).mean()
# print(df)


# data = {
#     'Name': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
#     'City': ['Cairo', 'London', 'Cairo', 'London', 'London'],
#     'Score': [85, 90, 78, 95, 88]
# }

# df = pd.DataFrame(data)
# df1 = pd.pivot_table(df, index='City', values='Score', columns='Name', aggfunc=['mean', 'median'], fill_value=0)
# print(df1.reset_index())

# print(pd.crosstab(df['City'], df['Name']))

# df2 = df.groupby(['City', 'Name'])['Score'].agg(['mean', 'median'])
# print(df2)


# arrays = [
#     ['A', 'A', 'B', 'B'],
#     ['cat', 'dog', 'cat', 'dog']
# ]
# index = pd.MultiIndex.from_arrays(arrays, names=['letters', 'animals'])
# df = pd.DataFrame({'value': [101, 102, 103, 104]}, index=index)
# df = df.sort_index()
# # print(df.loc['A':'B'])
# # print(df.loc[('A', 'dog')])
# # df = df.reset_index()
# # print(df)
# unstacked = df.unstack()
# print(unstacked)
# print(unstacked.loc['A', ('value', 'cat')])
# stacked = unstacked.stack(future_stack=True)
# print(stacked)
# print(pd.pivot_table(df, index='letters', columns='animals', values='value', aggfunc=['mean', 'median']))

# df = pd.DataFrame({
#     'Name': ['Alice', 'Bob', 'Charlie'],
#     'Score': [85, 90, 78]
# })

# df['Name'] = df['Name'].map(lambda x: x.lower())
# df['Score'] = df['Score'].map(lambda x: x * 2)
# df = df.map(lambda x: x.title() if isinstance(x, str) else int(x / 2))
# print(df.dtypes)
# print(df.apply(lambda col: col.mean() if col.dtype != 'O' else None))


# data = {
#     'Region': ['North', 'North', 'South', 'South', 'South'],
#     'City': ['Cairo', 'Cairo', 'Aswan', 'Aswan', 'Luxor'],
#     'Sales': [100, 150, 200, 250, 300]
# }

# df = pd.DataFrame(data)
# def my_range(sales):
#     return sales.max() - sales.min()

# df2 = df.groupby('City')['Sales'].agg(['sum', my_range])
# df2.index = ['a', 'b', 'c']
# print(df2)

# df = pd.DataFrame({
#     'Name': [' Alice ', 'BOB', 'CharLie', None],
#     'City': ['Cairo', 'London', 'new york', 'new jersey']
# })

# # df['Name'] = df['Name'].str.strip().str.capitalize()
# df['City'] = df['City'].str.replace('New.*', 'NEW YORK', case=True, regex=True)
# print(df)

# df = pd.DataFrame({
#         'Name': ['John Smith', 'Alice Johnson', 'Bob Davis', 'John Cena'], 
#         'City': ['Cairo', 'London', 'new york', 'Paris']
#     })

# df[['First Name', 'Last Name']] = df['Name'].str.extract(r'([A-Z][a-z]+)\s([A-Z][a-z]+)', expand=True)
# print(df['Name'].str.split()[0])
# print(df)


# df = pd.DataFrame({
#     'City': ['Cairo', 'London', 'Cairo', 'Paris', 'Cairo', 'London']
# })

# print(df.dtypes)
# print(df.memory_usage(deep=True))

# df['City'] = df['City'].astype('category')

# print(df.dtypes)
# print(df.memory_usage(deep=True))

# print(df[df['City'].cat.codes == 0])
# df['City'] = df['City'].cat.rename_categories({'Cairo': 'CAI', 'London': 'LON', 'Paris': 'PAR'})
# print(df['City'].cat.categories)


# df = pd.DataFrame({
#     'Date': pd.date_range(start='2024-01-01', periods=10, freq='D'),
#     'Sales': [10, 20, 15, 30, 45, 40, 35, 50, 55, 60]
# })

# print(df['Sales'].rolling(window=3, min_periods=2).agg(['mean', 'median']))
# print(df['Sales'].expanding().mean())




"""
Notes:
    1. better: just always call df.sort_index() after creating your MultiIndex.
    2. axis=0: acts on rows → vertical
    3. axis=1: acts on columns → horizontal
"""