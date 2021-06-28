import tushare as ts

today_all = ts.get_today_all()
print(type(today_all))

print(today_all.dtypes)

print(today_all.values[0])

