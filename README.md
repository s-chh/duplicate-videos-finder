# duplicate-videos-finder
Find all the duplicate videos in a folder and deletes them. Repeats it for all sub-directories as well.

<br>

Videos are marked as duplicate if their first frame matches on per-pixels comparison and they have the exact same number of total frames.

<br>

This code requires Python3. Run the following command to install all the dependencies:
```python
pip install -r requirements.txt
```

Use the following command to run the code: 
```python
python duplicate.py --inspection_dir "D:\Pictures\"
```
