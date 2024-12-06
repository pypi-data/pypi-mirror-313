"""通过这种方式，让深层的函数也能拿到想要的参数，而不用改变函数的签名"""


def create_params():
    _params = {}

    def set_params(name, value):
        global _params
        _params[name] = value

    def get_params(name):
        return _params[name]

    return get_params, set_params


get_params, set_params = create_params()
