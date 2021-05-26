# duplicate-videos-finder
Find all the duplicate videos in a folder and deletes them. Repeats it for all sub-directories as well.

A video is marked as duplicate if the first frame pixels matches and they have same number of total frames.

<br>

This code requires Python3. Run the following command to install all the dependencies:
```python
pip install -r requirements.txt
```

Use the following command to run the code: 
```python
python duplicate.py --inspection_dir "D:\Pictures\"
```
