def to_bool(v):
    if v in ["True", "true", True]:
        return True
    elif v in ["False", "false", False]:
        return False
    else:
        return None


def toType(val, typ):
    val_type = type(val)
    if typ in [str, float]:
        return typ(val) if val_type != list else [typ(item) for item in val]
    elif typ == int:
        try:
            return typ(val) if val_type != list else [typ(item) for item in val]
        except:
            return float(val) if val_type != list else [float(item) for item in val]
    elif typ == bool:
        return to_bool(val) if val_type != list else [to_bool(item) for item in val]


def useDefaultType(val, default):
    val_type = type(val)
    default_type = type(default)

    # 根据 default 的类型进行转换
    if default_type in [str, int, float, bool]:
        try:
            val = toType(val, default_type)
            if val_type == list:
                try:
                    val = val[0]
                except:
                    return default
        except:
            return None
    elif default_type == list:
        try:
            if len(default) > 0:
                if val_type != list:
                    val = [useDefaultType(val, default[0])]
                # 判断 default 列表中元素的类型，假设所有元素类型相同
                if len(val) > 0:
                    element_type = type(default[0])
                    if type(val[0]) is element_type:
                        val = toType(val, element_type)
                else:
                    val = []
            else:
                if val_type != list:
                    val = [val]
        except:
            return None
    return val

