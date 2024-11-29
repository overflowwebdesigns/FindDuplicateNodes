# Clone thie repository
```git clone https://github.com/overflowwebdesigns/FindDuplicateNodes.git```

# Run
```
python3 findDups.py
```
The script will ask you for the path to your SVG file.

# The output will be something like this:
```
Duplicate points found:
Path ID: path240
Path ID: path229
Path ID: path230
Path ID: path199
Path ID: path150
Path ID: path170
Path ID: path172
Path ID: path178
Path ID: path165
Path ID: path92
Path ID: path15
Path ID: path59
Path ID: path53
```

These ID's will match up to shapes in your InkScape file.  If you view them with the "edit path by nodes" tool in InkScape you will find there is a duplicate node.

## Note: This will produce a false positive once and awhile do to tolerances with close points.
