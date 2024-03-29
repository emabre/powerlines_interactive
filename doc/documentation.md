# Documentation

## Info on parameter values
Data on typical values of the parameter employed (i.e. impedances and other stuff) come from an educational paper, see ref [1], table 2.

## Implementation
### About matrix vector multiplication with numpy
The code
```Python
M = np.array(((1,2), (3,4)))
```
generates a matrix M, whose "ipython" description is:
```
array([[1, 2],
       [3, 4]])
```
Whereas the code
```Python
v = np.array([3,1])
```
generates a vector M, whose "ipython" description is:
```
array([3, 1])
```
Lastly, the code
```Python
np.dot(M,v)
```
generates a vector whose "ipython" description is:
```
array([ 5, 13])
```
hence one may easily derive the following **interpretations** for the two generated vectors and their "dot" multiplication, **in terms of the usual linear algebra notation**:
```
np.array(((1,2), (3,4))) :=
-------
|1   2|
|3   4|
-------

np.array([3,1]) :=
---
|3|
|1|
---

np.dot(M,v) :=
------- ---   ----
|1   2| |3| = |5 |
|3   4| |1|   |13|
------- ---   ----
```

## References
[1] R. Benato and S. D. Sessa, "The Ossanna’s Theorem for Educational Purposes: Impact of Distributed Parameter Transmission Lines on Power Systems," in IEEE Access, vol. 9, pp. 10577-10585, 2021, doi: 10.1109/ACCESS.2021.3049395.