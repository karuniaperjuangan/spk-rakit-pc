
from fastapi import APIRouter
from schema import RequestRecommendationSchema
import json
from random import sample
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

"""
class RequestRecommendationSchema(BaseModel):
    budget: int
    jenis_penggunaan: str = 'gaming'
    cpu_brand: str = 'any'
    monitor: int = 0 # 0 = No, 1 = Yes
    peripheral: int = 0 # 0 = No, 1 = Yes
    gpu_brand: str = 'any'
"""

usage_weight ={
    "gaming": {
        'gpu': 0.4,
        'cpu': 0.3,
    },
    "multimedia": {
        'monitor': 0.2,
        'cpu': 0.3,
        'gpu': 0.2,
    },
    "office": {
        'cpu': 0.3,
        'gpu': 0.1,
    }
}
@router.post("/recommendation")
async def recommendation(request_recommendation: RequestRecommendationSchema):
    success = False
    while not success:
        try:
            with open('./data/processed/component.json', 'r') as f:
                component = json.load(f)
                used_component = {}

                budget = request_recommendation.budget
                if (budget < 3000000 and request_recommendation.monitor == 1) or (budget < 2000000 and request_recommendation.monitor == 0):
                    return {"message": "Budget tidak mencukupi"}
                else:
                    list_key_component = ['monitor','casing','gpu','ssd','keyboard','motherboard','mouse','processor','psu','ram']
                    if request_recommendation.peripheral == 0:
                        list_key_component.remove('keyboard')
                        list_key_component.remove('mouse')
                    if request_recommendation.monitor == 0:
                        list_key_component.remove('monitor')
                    ### Processor ###
                    if request_recommendation.cpu_brand == 'amd':
                        list_processor = [x for x in component['processor'] if x['brand'] == 'amd']
                    elif request_recommendation.cpu_brand == 'intel':
                        list_processor = [x for x in component['processor'] if x['brand'] == 'intel']
                    else:
                        list_processor = component['processor']
                    #filter by price, tolerance -0.1 to 0 from weight
                    list_filtered_processor = [x for x in list_processor 
                                    if x['price'] <= budget * (usage_weight[request_recommendation.jenis_penggunaan]['cpu']) 
                                    and x['price'] >= budget * (usage_weight[request_recommendation.jenis_penggunaan]['cpu'] - 0.1)]
                    if len(list_filtered_processor) > 0:
                        list_processor = list_filtered_processor
                        used_component['processor'] = sample(list_processor, 1)[0]
                    else: 
                        used_component['processor'] = sorted([
                        x for x in list_processor if x['price'] <= budget * (usage_weight[request_recommendation.jenis_penggunaan]['cpu'])], key=lambda x: x['price'])[-1]
                    #used_component['processor'] = sample(list_processor, 1)[0]
                    budget -= used_component['processor']['price']
                    list_key_component.remove('processor')

                    ### GPU ###
                    if request_recommendation.gpu_brand == 'amd':
                        list_gpu = [x for x in component['gpu'] if x['brand'] == 'amd']
                    elif request_recommendation.gpu_brand == 'nvidia':
                        list_gpu = [x for x in component['gpu'] if x['brand'] == 'nvidia']
                    else:
                        list_gpu = component['gpu']
                    #filter by price, tolerance -0.1 to 0 from weight
                    list_filtered_gpu = [x for x in list_gpu
                                        if x['price'] <= request_recommendation.budget * (usage_weight[request_recommendation.jenis_penggunaan]['gpu'])
                                        and x['price'] >= request_recommendation.budget * (usage_weight[request_recommendation.jenis_penggunaan]['gpu'] - 0.1)]
                    if len(list_filtered_gpu) > 0:
                        list_gpu = list_filtered_gpu
                        used_component['gpu'] = sample(list_gpu, 1)[0]
                    else: 
                        used_component['gpu'] = sorted([
                        x for x in list_gpu if x['price'] <= budget * (usage_weight[request_recommendation.jenis_penggunaan]['gpu'])], key=lambda x: x['price'])[-1]
                    
                    
                    budget -= used_component['gpu']['price']
                    list_key_component.remove('gpu')

                    


                    ### Motherboard ###
                    list_motherboard = [x for x in component['motherboard'] if x['socket'] == used_component['processor']['socket']]
                    #print(list_motherboard)
                    ## no more of 0.25 remaining budget
                    list_motherboard = [x for x in list_motherboard if x['price'] <= budget *0.5]
                    list_motherboard = sorted(list_motherboard, key=lambda x: x['price'])[len(list_motherboard)//2:]
                    if len(list_motherboard) > 0:
                        used_component['motherboard'] = sample(list_motherboard, 1)[0]
                    else:
                        used_component['motherboard'] = sorted([
                        x for x in [x for x in component['motherboard'] if x['socket'] == used_component['processor']['socket']] if x['price'] <= budget], key=lambda x: x['price'])[-1]
                    budget -= used_component['motherboard']['price']
                    list_key_component.remove('motherboard')

                    ### RAM ###
                    # ram_type from socket must same with ram_type from RAM
                    socket = used_component['motherboard']['socket']
                    socket = [x for x in component['socket'] if x['name'] == socket][0]

                    list_ram = [x for x in component['ram'] if x['ram_type'] == socket['ram_type']]
                    list_ram = [x for x in list_ram if x['price'] <= budget * 0.4]
                    list_ram = sorted(list_ram, key=lambda x: x['price'])[len(list_ram)//2:]
                    if len(list_ram) > 0:
                        used_component['ram'] = sample(list_ram, 1)[0]
                    else:
                        used_component['ram'] = sorted([
                        x for x in [x for x in component['ram'] if x['ram_type'] == socket['ram_type']] if x['price'] <= budget], key=lambda x: x['price'])[-1]
                    budget -= used_component['ram']['price']
                    list_key_component.remove('ram')

                    ### PSU ###
                    # 550 W if GPU less than 5000000, 650 W if GPU m5000000 - 10000000, 750 W if GPU more than 10000000
                    list_psu = [psu for psu in component['psu'] if psu['wattage']is not None]
                    if used_component['gpu']['price'] < 5000000:
                        list_psu = [x for x in list_psu if int(x.get('wattage','0W').split('W')[0]) == 550 and x['price'] <= budget * 0.5]
                    elif used_component['gpu']['price'] >= 5000000 and used_component['gpu']['price'] < 10000000:
                        list_psu = [x for x in list_psu if int(x.get('wattage','0W').split('W')[0]) == 650 and x['price'] <= budget * 0.5]
                    elif used_component['gpu']['price'] >= 10000000 and used_component['gpu']['price'] < 2000000:
                        list_psu = [x for x in list_psu if int(x.get('wattage','0W').split('W')[0]) == 750 and x['price'] <= budget * 0.5]
                    else:
                        list_psu = [x for x in list_psu if int(x.get('wattage','0W').split('W')[0]) == 1600 and x['price'] <= budget * 0.5]
                    used_component['psu'] = sample(list_psu, 1)[0]

                    for key in list_key_component:
                        list_component = component[key]
                        list_component = [x for x in list_component if x['price'] <= budget * usage_weight[request_recommendation.jenis_penggunaan].get(key, 0.5)]
                        if len(list_component) == 0:
                            list_component = [x for x in list_component if x['price'] <= budget]
                        if len(list_component) == 0:
                            continue
                        used_component[key] = sample(list_component, 1)[0]
                        budget -= used_component[key]['price']
                    success = True
        except (IndexError, ValueError, KeyError):
                success = False
        return {'remaining_budget': budget, 'used_component': [{"component":key,**value} for key, value in used_component.items()]}


    