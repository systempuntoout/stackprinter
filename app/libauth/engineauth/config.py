from engineauth import utils
try:
    from appengine_config import engineauth as user_config
except ImportError:
    user_config = None

default_config = {
    'base_uri': '/auth',
    'login_uri': '/',
    'success_uri': '/myse',
    }

def load_config(cust_config=None):
    """

    :param cust_config:
    :return:
    """
    global user_config
    if cust_config is not None:
        user_config = cust_config
    return utils.load_config(default_config, user_config)