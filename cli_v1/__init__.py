from utils import get_operating_system

if get_operating_system() != "windows":
    raise Exception("cli_v1 is only supported on Windows. Please run this program on a Windows machine with outlook installed.")

