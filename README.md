# chess

Creating a chess gui and AI
# installation
```
pip install python-chess
```
```
pip install pygame
```

# TODO
For some reason getPieceCaptured shows '.' instead of the piece...

# Output DEPTH 5

## Minmax DEPTH 4
```
e7e6 7.5
nodes:  374 806
time: 59.446002s
```

## Alpha Beta DEPTH 5
```

b8c6
nodes:  73754
time: 9.891684s

g8f6
nodes:  220884
time: 19.856718s

e7e5
nodes:  534039
time: 44.651963s
```
## Store evalutations, moves in hash table DEPTH 5
```

e7e5
nodes:  69022
time: 9.684745s

d8f6
nodes:  269247
time: 27.938165s

g8e7
nodes:  738912
time: 65.663914s
```