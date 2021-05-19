import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = ''  # 企业ID， 登陆企业微信，在我的企业-->企业信息里查看
        self.CORPSECRET = ''  # 自建应用，每个自建应用里都有单独的secret
        self.AGENTID = ''  # 应用代码
        self.TOUSER = ""  # 接收者用户名,@all 全体成员

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID, 'corpsecret': self.CORPSECRET, }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7200:  # token的有效时间7200s
                return access_token
            else:
                with open('access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, msg):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": msg
            },
            "safe": "0"
        }
        send_msgs = (bytes(json.dumps(send_values), 'utf-8'))
        response = requests.post(send_url, send_msgs)
        # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        response = response.json()
        return response["errmsg"]


if __name__ == '__main__':
    wx = WeChat()
    wx.send_data(msg="测试发送信息")
