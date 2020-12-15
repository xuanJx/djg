from django.utils.html import escape

def set_url_parameter(url, name, value):
    if not isinstance(name, str):
        name = str(name)
    if not isinstance(value, str):
        value = str(value)

    url_split = url.split('?')
    if len(url_split) == 1:
        url += "?" + name + "=" + value
    else:
        ori_param = url_split[1].split("&")
        ori_param_map = dict()
        for item in ori_param:
            v = item.split('=')
            ori_param_map[v[0]] = v[1]
        ori_param_map[name] = value

        new_param = [k+"="+v for k, v in ori_param_map.items()]
        url = url_split[0] + "?"
        url += '&'.join(new_param)
    return escape(url)