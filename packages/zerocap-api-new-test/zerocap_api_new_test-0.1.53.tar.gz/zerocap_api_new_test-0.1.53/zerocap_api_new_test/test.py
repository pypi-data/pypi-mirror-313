# pip install zerocap-api-new-test -i https://www.pypi.org/simple/
import time
import traceback
import threading
import numpy as np
# from zerocap_api_new_test import ZerocapWebsocketClient, ZerocapRestClient
from main import ZerocapWebsocketClient, ZerocapRestClient

messages = []
api_key = "coinroutes"
api_secret = "e2d2a9b8-85fe-4a38-b9bd-60e06b58b28a"


def create_ws_connection():
    zc_ws = ZerocapWebsocketClient(api_key, api_secret, envion='uat')
    websocket_connection = zc_ws.create_connection()
    connect_result = zc_ws.recv(websocket_connection)

    zc_ws.send({"type": 'price', "symbol": "USDT/AUD"})
    zc_ws.send({"type": 'order'})
    zc_ws.send({"type": 'trade'})
    while True:
        try:
            message = zc_ws.recv(websocket_connection)

            global messages
            messages.append(message)
            if len(messages) >= 50:
                messages = messages[-50:]

        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(traceback.format_exc())
            return


def create_order():
    print(time.time(), "start time")
    zc_rest = ZerocapRestClient(api_key, api_secret, envion='uat')

    last_update_price_time = 0
    last_msg_time = time.time() + 1
    last_error_time = 0
    book = {"bids": [], "asks": []}
    times = {"place": np.array([]), "fetch": np.array([])}
    buy_side = True
    error_flag = False
    counter = 1

    while True:
        if not messages:
            time.sleep(1)
            print('not messages continue .....')
            continue
        try:
            message = messages.pop(0)
            print(message)

            if counter % 100 == 0:
                print(
                    time.time(),
                    f"place: {round(np.mean(times['place']) * 1e3, 6)}",
                    f"fetch: {round(np.mean(times['fetch']) * 1e3, 6)}",
                    counter
                )

                times = {"place": np.array([]), "fetch": np.array([])}

            if message['type'] == 'price':
                # time_used = time.time() - last_msg_time
                # last_msg_time = time.time()

                # if time_used > 0.5:
                #     print("time between price updates", time_used, message, "\n")

                if time.time() - last_update_price_time > 0.5:
                    data = message['data']
                    book['bids'] = data['bids']
                    book['asks'] = data['asks']

                    last_update_price_time = time.time()

                if error_flag:
                    print("price", message)

                    if time.time() - last_error_time > 0.5:
                        error_flag = False

            if len(book['bids']) > 0 and len(book['asks']) > 0:
                side = "buy" if buy_side else "sell"

                if side == "sell":
                    price = float(book['bids'][0][0]) * 0.9
                else:
                    price = float(book['asks'][0][0]) * 1.1

                time_start = time.time()

                result = zc_rest.create_order(
                    symbol='USDT/AUD',
                    side=side,
                    type='limit',
                    amount='10',
                    price=price,
                    coinroutes_customer_id='ZCStreamingLiquidity1')

                times['place'] = np.append(times['place'], time.time() - time_start)

                if result['error_message'] != '':
                    error_flag = True
                    last_error_time = time.time()
                    print(result)

                time_start = time.time()

                zc_rest.fetch_order(result['id'])

                times['fetch'] = np.append(times['fetch'], time.time() - time_start)

                buy_side = not buy_side

                counter += 1
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(traceback.format_exc())


if __name__ == '__main__':
    threading.Thread(target=create_order).start()
    create_ws_connection()

