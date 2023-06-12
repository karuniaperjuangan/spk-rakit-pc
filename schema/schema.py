# build a schema using pydantic
from pydantic import BaseModel
from datetime import datetime

class RequestRecommendationSchema(BaseModel):
    budget: int
    jenis_penggunaan: str = 'gaming'
    cpu_brand: str = 'any'
    monitor: int = 0 # 0 = No, 1 = Yes
    peripheral: int = 0 # 0 = No, 1 = Yes
    gpu_brand: str = 'any'
 
