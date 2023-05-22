import requests
from json import dumps as jsonDumps
 
class QL:
    def __init__(self, address: str, id: str, secret: str) -> None:
        """
        初始化
        """
        self.address = address
        self.id = id
        self.secret = secret
        self.valid = True
        self.login()
 
    def log(self, content: str) -> None:
        """
        日志
        """
        print(content)
 
    def login(self) -> None:
        """
        登录
        """
        url = f"{self.address}/open/auth/token?client_id={self.id}&client_secret={self.secret}"
        try:
            rjson = requests.get(url).json()
            if(rjson['code'] == 200):
                self.auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
            else:
                self.log(f"登录失败：{rjson['message']}")
        except Exception as e:
            self.valid = False
            self.log(f"登录失败：{str(e)}")
 
    def getEnvs(self) -> list:
        """
        获取环境变量
        """
        url = f"{self.address}/open/envs?searchValue="
        headers = {"Authorization": self.auth}
        try:
            rjson = requests.get(url, headers=headers).json()
            if(rjson['code'] == 200):
                return rjson['data']
            else:
                self.log(f"获取环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"获取环境变量失败：{str(e)}")
 
    def deleteEnvs(self, ids: list) -> bool:
        """
        删除环境变量
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,"content-type": "application/json"}
        try:
            rjson = requests.delete(url, headers=headers, data=jsonDumps(ids)).json()
            if(rjson['code'] == 200):
                self.log(f"删除环境变量成功：{len(ids)}")
                return True
            else:
                self.log(f"删除环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"删除环境变量失败：{str(e)}")
            return False
 
    def addEnvs(self, envs: list) -> bool:
        """
        新建环境变量
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,"content-type": "application/json"}
        try:
            rjson = requests.post(url, headers=headers, data=jsonDumps(envs)).json()
            if(rjson['code'] == 200):
                self.log(f"新建环境变量成功：{len(envs)}")
                return True
            else:
                self.log(f"新建环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"新建环境变量失败：{str(e)}")
            return False
 
    def updateEnv(self, env: dict) -> bool:
        """
        更新环境变量
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,"content-type": "application/json"}
        try:
            rjson = requests.put(url, headers=headers, data=jsonDumps(env)).json()
            if(rjson['code'] == 200):
                self.log(f"更新环境变量成功")
                return True
            else:
                self.log(f"更新环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"更新环境变量失败：{str(e)}")
            return False
    
def getEnvValueByName(Envs,EnvName):
    result = next((item for item in Envs if item.get('name') == EnvName), None)
    return result['value']
def getIdByName(Envs,EnvName):
    result = next((item for item in Envs if item.get('name') == EnvName), None)
    return result['id']
# if __name__ == "__main__":
#     address = "http://192.168.2.121:5700"
#     client_id = "9QO7c7RE_wfK"
#     client_secret = "mPlXkDn1_-FV87BE6HVWPNl0"
 
#     ql = QL(address, client_id, client_secret)
 
#     envs = ql.getEnvs()
    # result = ql.getEnvValueByName('JC_Passwd')


    #print(envs)
    # result = next((item for item in envs if (name := item.get('name')) == 'JC_COOKIE'), None)
    # print("JC_COOKIE:"+str(result))
 
    # envs = {"name":"JC_COOKIE","value":"heheh","id":result['id']}
    # result = ql.updateEnv(envs)

    # print(result)
    # #result = ql.deleteEnvs(envs)

    