from finance_core import TimeSeries

values = [10.0, 12.0, 14.0, 16.0, 18.0]
index = [i for i in range(len(values))]

ts = TimeSeries(
    index=index,
    values=values
)

print(ts.sma(3))
