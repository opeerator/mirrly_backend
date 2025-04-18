```
cd face_tracking/
python3 tracking.py 
```
- after running, open the following link to see your face from the robot's eyes
- http://127.0.0.1:5001/video_feed
- first moves eyes for small changes, and then head for larger changes
- robot accurately tracks your face as long as it's in frame

```
cd face_tracking/
python3 move_collection.py 
```
- shows the collection of eye movements (gaze left and right, open and close eyelids) and head movements (side to side, up and down)