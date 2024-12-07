from rspy_utilities import distinct

print(list(distinct([1, 2, 2, 3, 3, 4])))  # [1, 2, 3, 4]

for i in distinct(range(1000), lambda x: x % 10):
    print(i)

iterator = distinct(range(10), lambda x: x % 10)

assert next(iterator) == 0
assert next(iterator) == 1
assert next(iterator) == 2
assert next(iterator) == 3
assert next(iterator) == 4
assert next(iterator) == 5
assert next(iterator) == 6
assert next(iterator) == 7
assert next(iterator) == 8
assert next(iterator) == 9

raised = False
try:
    next(iterator)
except StopIteration:
    raised = True

assert raised
