# mt19937ar
Python implementation of [mt19937ar](http://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/MT2002/mt19937ar.html)

## Installation
```bash
pip install mt19937ar
```

## Usage
```python
from mt19937ar import MT19937ar

mt = MT19937ar()
mt.init_by_array([0x123, 0x234, 0x345, 0x456])

print(mt.genrand_int32()) # 1067595299
print(mt.genrand_int32()) # 955945823
print(mt.genrand_int32()) # 477289528
```
