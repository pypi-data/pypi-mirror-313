# Finance core

```python
from finance_core import TimeSeries

index = [1, 2, 3, 4, 5]
values = [10.0, 12.0, 14.0, 16.0, 18.0]

ts = TimeSeries(
    index=index,
    values=values
)

print(ts.sma(3))
>> [None, None, 12.0, 14.0, 16.0]
```