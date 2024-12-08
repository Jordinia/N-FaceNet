```python
from roboflow import Roboflow

rf = Roboflow(api_key="hDRVY879zqjf421YDiEA")
project = rf.workspace("nfacenet").project("nfacenet")
version = project.version(3)
dataset = version.download("yolov11", location="./dataset")
```