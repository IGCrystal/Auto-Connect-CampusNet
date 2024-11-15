import requests

# 配置登录信息
login_url = "http://10.71.29.181/eportal/InterFace.do?method=login"  # 填入请求URL
cookies = {
    "EPORTAL_COOKIE_USERNAME": "xxxxxxxxxxx",  # 你的学号
    "EPORTAL_COOKIE_DOMAIN": "false",
    "EPORTAL_COOKIE_SAVEPASSWORD": "true",  # 已开启保存密码
    "EPORTAL_COOKIE_OPERATORPWD": "",
    "EPORTAL_COOKIE_NEWV": "true",
    "EPORTAL_COOKIE_PASSWORD": "41991b2c8296c2cfde278ef16ce2aa717b25d26dc0955578e259e9886f3fc89d6f566a",  # 加密后的密码
    "EPORTAL_COOKIE_SERVER": "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8",  # 运营商信息（注：不同学校可能编码不一样，以自己学校的为准）: 中国移动(%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8)
    "EPORTAL_COOKIE_SERVER_NAME": "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8",  # 依旧是运营商信息
    "EPORTAL_AUTO_LAND": "",
    "EPORTAL_USER_GROUP": "%E5%AD%A6%E7%94%9F",  #  账号身份信息 （学生、老师……）
    "JSESSIONID": "F56A865393E7FCE1BCFB24856B4EB0A3"  #  会话标识符
}


# 检查是否已登录校园网
def check_network_status():
    try:
        # 访问任意网页（如百度）以检测是否会被重定向
        response = requests.get("http://www.baidu.com")
        response_text = response.text

        # 检查是否包含重定向到校园网登录页的 `<script>` 标签
        if "top.self.location.href='http://10.71.29.181" in response_text:
            print("未连接校园网，需要登录")
            return False
        else:
            print("已连接校园网，无需登录")
            return True

    except requests.RequestException as e:
        print(f"网络请求失败：{e}")
        return False


# 获取 query_string
def get_query_string(session):
    response = session.get("http://10.71.29.181/")
    query_string = response.text
    st = query_string.find("index.jsp?") + 10
    end = query_string.find("'</script>")
    query_string = query_string[st:end]
    print("获取到 query_string:", query_string)
    return query_string


# 提交登录请求
def login():
    session = requests.Session()
    jsessionid = cookies["JSESSIONID"]
    query_string = get_query_string(session)
    headers = {
        "Host": "10.71.29.181",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "JSESSIONID": jsessionid,
    }
    post_data = {
        "userId": cookies["EPORTAL_COOKIE_USERNAME"],
        "password": cookies["EPORTAL_COOKIE_PASSWORD"],
        "service": "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8",
        "queryString": query_string,
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "true"
    }
    response = session.post(login_url, headers=headers, data=post_data, cookies=cookies)
    if response.json().get("result") == "success":
        print("登录成功！")
    else:
        print("登录失败，原因:", response.json().get("message"))


# 运行检测和登录
if not check_network_status():
    login()
else:
    print("跳过登录")
