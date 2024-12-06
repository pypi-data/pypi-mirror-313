# tsingroc-pymeteo

清鹏智能气象数据Python SDK

## 安装

```shell
pip install tsingroc-pymeteo
```

## 使用

```python
from tsingrocpymeteo import Meteo
from shapely.geometry import box
from datetime import datetime

meteo = Meteo(
    "<后端服务地址>", "<access key>", "<secret key>"
)

# 创建查询范围，类型为shapely.Polygon
center = (115.875, 27.5)
bbox = box(center[0] - 0.4, center[1] - 0.4, center[0] + 0.4, center[1] + 0.4)

res = meteo.get(
    "archive_cn", # 数据表名
    None,
    "era5", # 气象模型名
    bbox,
    (datetime(2024, 11, 7, 0, 0, 0, 0), datetime(2024, 11, 8, 0, 0, 0, 0)), # 时间范围
)

print(res)
```

响应格式如下：
- dict: 查询结果
    - table_name (str): 数据表名
    - points (List[dict]): 查询结果
        - model (str): 气象模型名
        - location (str): 坐标点的 WKT 字符串
        - data (pd.DataFrame): 查询结果
    - cost (dict): 查询耗时
