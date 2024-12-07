from finance_core import Maximum, Minimum, SimpleMovingAverage


three_day_max = Maximum(3)

print(three_day_max.next(1))
print(three_day_max.next(4))
print(three_day_max.next(2))
print(three_day_max.next(5))


three_day_min = Minimum(3)

print(three_day_min.next(1))
print(three_day_min.next(4))
print(three_day_min.next(2))
print(three_day_min.next(5))


sma_three_day = SimpleMovingAverage(3)

print(sma_three_day.next(1))
print(sma_three_day.next(4))
print(sma_three_day.next(2))
print(sma_three_day.next(5))
