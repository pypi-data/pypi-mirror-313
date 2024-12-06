import winreg
import enum

HIVES_MAP = {
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA
}


class RegistryKeyType(enum.IntEnum):
    # Binary data in any form
    REG_BINARY = 0

    # 32-bit number
    REG_DWORD = 1

    # A 32-bit number in little-endian format. Equivalent to REG_DWORD
    REG_DWORD_LITTLE_ENDIAN = 2

    # A 32-bit number in big-endian format
    REG_DWORD_BIG_ENDIAN = 3

    # Null-terminated string containing references to environment variables (%PATH%)
    REG_EXPAND_SZ = 4

    # A Unicode symbolic link
    REG_LINK = 5

    # A sequence of null-terminated strings, terminated by two null characters,
    # Python handles this termination automatically
    REG_MULTI_SZ = 6

    # No defined value type
    REG_NONE = 7

    # A 64-bit number
    REG_QWORD = 8

    # A 64-bit number in little-endian format. Equivalent to REG_QWORD
    REG_QWORD_LITTLE_ENDIAN = 9

    # A device-driver resource list
    REG_RESOURCE_LIST = 10

    # A hardware setting
    REG_FULL_RESOURCE_DESCRIPTOR = 11

    # A hardware resource list
    REG_RESOURCE_REQUIREMENTS_LIST = 12

    # A null-terminated string
    REG_SZ = 13


TYPES_MAP = {
    RegistryKeyType.REG_BINARY: winreg.REG_BINARY,
    RegistryKeyType.REG_DWORD: winreg.REG_DWORD,
    RegistryKeyType.REG_DWORD_LITTLE_ENDIAN: winreg.REG_DWORD_LITTLE_ENDIAN,
    RegistryKeyType.REG_DWORD_BIG_ENDIAN: winreg.REG_DWORD_BIG_ENDIAN,
    RegistryKeyType.REG_EXPAND_SZ: winreg.REG_EXPAND_SZ,
    RegistryKeyType.REG_LINK: winreg.REG_LINK,
    RegistryKeyType.REG_MULTI_SZ: winreg.REG_MULTI_SZ,
    RegistryKeyType.REG_NONE: winreg.REG_NONE,
    RegistryKeyType.REG_QWORD: winreg.REG_QWORD,
    RegistryKeyType.REG_QWORD_LITTLE_ENDIAN: winreg.REG_QWORD_LITTLE_ENDIAN,
    RegistryKeyType.REG_RESOURCE_LIST: winreg.REG_RESOURCE_LIST,
    RegistryKeyType.REG_FULL_RESOURCE_DESCRIPTOR: winreg.REG_FULL_RESOURCE_DESCRIPTOR,
    RegistryKeyType.REG_RESOURCE_REQUIREMENTS_LIST: winreg.REG_RESOURCE_REQUIREMENTS_LIST,
    RegistryKeyType.REG_SZ: winreg.REG_SZ
}


class Wow64RegistryEntry(enum.IntEnum):
    KEY_WOW32 = 0
    KEY_WOW64 = 1
    KEY_WOW32_64 = 2


WOW64_MAP = {
    Wow64RegistryEntry.KEY_WOW32: winreg.KEY_WOW64_32KEY,
    Wow64RegistryEntry.KEY_WOW64: winreg.KEY_WOW64_64KEY,
    Wow64RegistryEntry.KEY_WOW32_64: 0
}


def is_x64os():
    return True


def enumerate_key(key_hive, key_path, access_type=Wow64RegistryEntry.KEY_WOW64):
    key_hive_value = HIVES_MAP[key_hive]
    wow64_flags = WOW64_MAP[access_type]
    registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_READ))
    result = []
    for i in range(0, winreg.QueryInfoKey(registry_key)[1]):
        result.append(winreg.EnumValue(registry_key, i)[0])
    return result


def write_registry(key_hive, key_path, value_name, value_type, key_value, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        if is_x64os() and access_type == Wow64RegistryEntry.KEY_WOW32_64:
            write_registry(key_hive, key_path, value_name, value_type, key_value, Wow64RegistryEntry.KEY_WOW32)
            write_registry(key_hive, key_path, value_name, value_type, key_value, Wow64RegistryEntry.KEY_WOW64)
            return
        registry_key = None
        wow64_flags = WOW64_MAP[access_type]
        try:
            key_hive_value = HIVES_MAP[key_hive]
            value_type_value = TYPES_MAP[value_type]
            registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_WRITE))
            winreg.SetValueEx(registry_key, value_name, 0, value_type_value, key_value)
            winreg.CloseKey(registry_key)
            return True
        except:
            if registry_key is not None:
                winreg.CloseKey(registry_key)
            return False
    except:
        return False


def read_registry(key_hive, key_path, value_name, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        wow64_flags = WOW64_MAP[access_type]
        key_hive_value = HIVES_MAP[key_hive]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_READ))
        value, regtype = winreg.QueryValueEx(registry_key, value_name)
        winreg.CloseKey(registry_key)
        return value
    except:
        return ''


def create_key(key_hive, key_path, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        key_hive_value = HIVES_MAP[key_hive]
        wow64_flags = WOW64_MAP[access_type]
        registry_key = winreg.CreateKeyEx(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_WRITE))
        return registry_key
    except:
        return ''


def is_key_exist(key_hive, key_path, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        key_hive_value = HIVES_MAP[key_hive]
        wow64_flags = WOW64_MAP[access_type]
        winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_READ))
        return True
    except:
        return False


def remove_reg_key(key_hive, key_path, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        key_hive_value = HIVES_MAP[key_hive]
        wow64_flags = WOW64_MAP[access_type]
        winreg.DeleteKeyEx(key_hive_value, key_path, (wow64_flags | winreg.KEY_WRITE), 0)
        return True
    except:
        return False


def enumerate_key_values(key_hive, key_path, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        key_hive_value = HIVES_MAP[key_hive]
        wow64_flags = WOW64_MAP[access_type]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_READ))
        result = []
        for entry_num in range(0, winreg.QueryInfoKey(registry_key)[1]):
            result.append(winreg.EnumValue(registry_key, entry_num))
        return result
    except:
        return []


def enumerate_key_subkeys(key_hive, key_path, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        key_hive_value = HIVES_MAP[key_hive]
        wow64_flags = WOW64_MAP[access_type]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_READ))
        result = []
        for entry_num in range(0, winreg.QueryInfoKey(registry_key)[0]):
            result.append(winreg.EnumKey(registry_key, entry_num))
        return result
    except:
        return []


def create_value(key_hive, key_path, value_name, value_type, key_value, access_type=Wow64RegistryEntry.KEY_WOW64):
    registry_key = None
    wow64_flags = WOW64_MAP[access_type]
    try:
        key_hive_value = HIVES_MAP[key_hive]
        if isinstance(value_type, RegistryKeyType):
            value_type = TYPES_MAP[value_type]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_WRITE))
        winreg.SetValueEx(registry_key, value_name, 0, value_type, key_value)
        winreg.CloseKey(registry_key)
        return True
    except:
        if registry_key is not None:
            winreg.CloseKey(registry_key)
        return False


def delete_value(key_hive, key_path, value_name, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        key_hive_value = HIVES_MAP[key_hive]
        wow64_flags = WOW64_MAP[access_type]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_WRITE))
        winreg.DeleteValue(registry_key, value_name)
        return True
    except:
        return False


def read_value(key_hive, key_path, value_name, access_type=Wow64RegistryEntry.KEY_WOW64):
    if is_x64os() and access_type == Wow64RegistryEntry.KEY_WOW32_64:
        value32, regtype32 = read_value(key_hive, key_path, value_name, Wow64RegistryEntry.KEY_WOW32)
        value64, regtype64 = read_value(key_hive, key_path, value_name, Wow64RegistryEntry.KEY_WOW64)
        return (value32, regtype32), (value64, regtype64)
    wow64_flags = WOW64_MAP[access_type]
    registry_key = None
    try:
        key_hive_value = HIVES_MAP[key_hive]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_READ))
        value, regtype = winreg.QueryValueEx(registry_key, value_name)
        winreg.CloseKey(registry_key)
        return value, regtype
    except:
        if registry_key is not None:
            winreg.CloseKey(registry_key)
        return '', ''


def write_value(key_hive, key_path, value_name, value_type, key_value, access_type=Wow64RegistryEntry.KEY_WOW64):
    try:
        write_value(key_hive, key_path, value_name, value_type, key_value, Wow64RegistryEntry.KEY_WOW32)
        write_value(key_hive, key_path, value_name, value_type, key_value, Wow64RegistryEntry.KEY_WOW64)
    except:
        pass
    registry_key = None
    wow64_flags = WOW64_MAP[access_type]
    try:
        key_hive_value = HIVES_MAP[key_hive]
        if isinstance(value_type, RegistryKeyType):
            value_type = TYPES_MAP[value_type]
        registry_key = winreg.OpenKey(key_hive_value, key_path, 0, (wow64_flags | winreg.KEY_WRITE))
        winreg.SetValueEx(registry_key, value_name, 0, value_type, key_value)
        winreg.CloseKey(registry_key)
        return True
    except:
        if registry_key is not None:
            winreg.CloseKey(registry_key)
        return False