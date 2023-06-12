# build a schema using pydantic
from pydantic import BaseModel
from datetime import datetime

class RequestRecommendationSchema(BaseModel):
    budget: int
    jenis_penggunaan: str 
    cpu_brand: int = 0 # 0 = Any, 1 = Intel, 2 = AMD
    monitor: int = 0 # 0 = No, 1 = Yes
    peripheral: int = 0 # 0 = No, 1 = Yes
    gpu_brand: int = 0 # 0 = Any, 1 = Nvidia, 2 = AMD, 3 = No GPU
    ram: int = 0 # 0 = Any, 4GB, 8GB, 16GB, 32GB
 
