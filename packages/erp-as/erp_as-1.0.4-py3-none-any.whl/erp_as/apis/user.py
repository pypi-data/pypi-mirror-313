from erp_as.erpRequest import Request

def login(username: str, password: str):
    '''
    登录
    :param username: 账号
    :param password: 密码
    :return:
    '''
    return Request(
        method='post',
        url='https://api.erp321.com/erp/webapi/UserApi/WebLogin/Passport',
        json={
            "data": {
                "account": username,
                "password": password,
                "j_d_3": "",
                "v_d_144": "",
                "isApp": False
            },
            "ipAddress": ""
        },
        callback='login',
        hostType='erpApi'
    )

def getUserInfo(coid: int,uid: int):
    '''
    获取用户信息
    :return:
    '''
    return Request(
        method='post',
        url='https://api.erp321.com/erp/webapi/UserApi/Passport/GetUserInfo',
        json={
          "data": {},
          "uid": uid,
          "coid": coid
        },
        hostType='erpApi'
    )



# 获取售后极速版验证码
def get_auth_code(uid: int, u_co_name: str, u_name: str, u_lid: int):
    '''
    获取验证码
    :return:
    '''
    return Request(
        method='post',
        url='https://api.erp321.com/epaas/union/login/getAuthCode',
        json={
            "data": {
                "serviceKey": "after_sales",
                "loginType": "1",
                "uid": uid,
                "userId": uid,
                "coName": u_co_name,
                "coId": 10174711,
                "userName": u_name,
                "loginName": u_lid
            },
            "uid": uid,
            "coid": 10174711
        },
        hostType='erpApi'
    )


# 获取售后极速版token
def get_epaas_joint_login_gyl(auth_code: str):
    '''
    获取售后极速版token
    :return:
    '''
    return Request(
        method='post',
        url='https://sc.scm121.com/api/auth/open/epaasJointLoginGyl',
        json={
            "eTicket": auth_code,
            "serviceKey": "after_sales",
            "fromSource": "erp_menu_after_sale"
        },
        hostType='erpApi'
    )
