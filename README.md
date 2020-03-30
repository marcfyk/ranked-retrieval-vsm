# ranked-retrieval-vsm

## Overview
This is a ranked retrieval system to perform free text queries on a
vector space model, after being indexed on a corpus.

## How to run
Run the following command to index all files in the `<training-directory>` and save your file paths
into the `<config-file>`.
```
python3 index.py -t <training-directory> -c <config-file>
```
Run the following command to start the script to run queries.
```
python3 search.py -c <config-file>
```
After running the `search.py`, you can enter free text queries and return top ten results.


