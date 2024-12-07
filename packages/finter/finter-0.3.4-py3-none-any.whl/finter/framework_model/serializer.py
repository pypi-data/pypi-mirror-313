import re
import pickle


def is_serializer_target(identity_name):
    target = [
        "content.fnguide.ftp.financial*",
        "content\.fnguide\.ftp\.consensus\.krx-spot-[\w]+_[aq]\.1d",
        "content.fred.api.economy*"
    ]
    pattern = re.compile("|".join(target))

    if pattern.match(identity_name):
        return True
    return False


def deserialize_bytes(value):
    if not isinstance(value, bytes):
        return value
    try:
        return pickle.loads(value)
    except:
        return value


def apply_deserialization(df):
    for column in df.columns:
        df[column] = df[column].apply(deserialize_bytes)
    return df
