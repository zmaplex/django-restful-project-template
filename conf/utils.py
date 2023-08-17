## sqlite3, mysql, postgresql, oracle
# 根据传入的数据库类型，返回对应的数据库默认端口
def get_db_port(db_engine):
    if db_engine == "sqlite3":
        return ""
    elif db_engine == "mysql":
        return "3306"
    elif db_engine == "postgresql":
        return "5432"
    elif db_engine == "oracle":
        return "1521"
    else:
        return ""



def get_user_ip(requests):
    """
    获取用户IP
    :param requests:
    :return:
    """
    if requests.META.get("HTTP_X_FORWARDED_FOR"):
        ip = requests.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = requests.META.get("REMOTE_ADDR")
    return ip