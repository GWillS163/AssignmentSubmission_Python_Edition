import uuid
from db.macLib import mac_dict


def get_mac_address():
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = mac.upper()
    except Exception as E:
        return "\n无法识别:" + str(E)

    try:
        factory = mac_dict[mac[:6]]
    except:
        try:
            factory = mac_dict[mac[:5]]
        except Exception as E:
            factory = str(E)
    return "\n" + factory + "\n" + mac


if __name__ == "__main__":
    print(get_mac_address())
