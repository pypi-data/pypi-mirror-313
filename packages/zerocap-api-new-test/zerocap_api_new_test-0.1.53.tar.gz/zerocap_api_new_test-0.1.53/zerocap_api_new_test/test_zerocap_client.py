
from main import ZerocapRestClient
import uuid
import json

# API key and secret required
apiKey = "coinroutes"
apiSecret = "e2d2a9b8-85fe-4a38-b9bd-60e06b58b28a"

client = ZerocapRestClient(apiKey, apiSecret, envion="uat")
client_order_id = str(uuid.uuid4())

result = client.create_order(symbol='USDT/AUD',
                             side='buy',
                             type='limit',
                             amount='100',
                             price='1.7888234',
                             coinroutes_customer_id=5
                             )
print("创建订单详情##", json.dumps(result, indent=4))
print("-------------------------------------------")
if result:
    result = client.fetch_order(id=result['id'])
    print("查询单个订单详情##", json.dumps(result, indent=4))
    print("-------------------------------------------")

result = client.fetch_orders()
print("查询批量订单详情##", json.dumps(result, indent=4))
print("-------------------------------------------")
