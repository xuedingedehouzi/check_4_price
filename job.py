import requests
import json
import schedule
import time
from spiders.WeChat import WeChat

def check_single_stock(hospital_id):
    url = f""
    response = requests.request("GET", url)

    # 返回关键项
    key_item = {}

    result = json.loads(response.text)
    status_code = result["statusCode"]
    if status_code == 200:
        data = result["data"]
        for i in data:
            data_id = i["id"]
            if data_id == "41":
                key_item = i
                break
    return key_item


def check_all_4_price():
    url = f""
    response = requests.request("GET", url)

    result = json.loads(response.text)
    status_code = result["statusCode"]
    if status_code == 200:
        data = result["data"]
        wx = WeChat()
        for i in data:
            hospital_id = i["id"]
            hospital_name = i["name"]
            hospital_phone = i["phone"]
            # 推迟1秒执行
            time.sleep(1)
            # 查询单个医院的库存
            key_item = check_single_stock(hospital_id)
            print(key_item)
            stock_status = key_item["yumiao_status"]
            stock_status_str = "正常供应" if (int(stock_status) == 1) else "供应少量" if (int(stock_status) == 2) else "缺货"
            if stock_status_str != "缺货":
                msg = hospital_name + "可以预约四价了,联系方式为:" + hospital_phone + "当前库存情况为：" + stock_status_str
                # 发送微信推送消息
                wx.send_data(msg=msg)


def job():
    print("执行新的任务")
    check_all_4_price()


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
