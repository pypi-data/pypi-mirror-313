import logging
from src.python_package import misc

# Set up logging
logging.basicConfig(level=logging.INFO)

class TestMisc:
    def __init__(self):
        pass

    def ip(self):
        try:
            return misc.getip()
        except Exception as e:
            logging.error(f"Error getting IP: {e}")
            return None

    def geo(self):
        try:
            ip = self.ip()
            if ip:
                return misc.getgeo(ip)
            else:
                logging.error("IP address not available.")
                return None
        except Exception as e:
            logging.error(f"Error getting geolocation: {e}")
            return None

    def hwid(self):
        try:
            return misc.gethwid()
        except Exception as e:
            logging.error(f"Error getting HWID: {e}")
            return None

    def user(self):
        try:
            return misc.getuser()
        except Exception as e:
            logging.error(f"Error getting username: {e}")
            return None

    def cpuinfo(self):
        try:
            return misc.getcpuinfo()
        except Exception as e:
            logging.error(f"Error getting CPU info: {e}")
            return None

    def gpuinfo(self):
        try:
            return misc.getgpuinfo()
        except Exception as e:
            logging.error(f"Error getting GPU info: {e}")
            return None

    def raminfo(self):
        try:
            return misc.getraminfo()
        except Exception as e:
            logging.error(f"Error getting RAM info: {e}")
            return None

    def osinfo(self):
        try:
            return misc.getosinfo()
        except Exception as e:
            logging.error(f"Error getting OS info: {e}")
            return None

    def diskinfo(self):
        try:
            return misc.getdiskinfo()
        except Exception as e:
            logging.error(f"Error getting disk info: {e}")
            return None

    def batteryinfo(self):
        try:
            return misc.getbatteryinfo()
        except Exception as e:
            logging.error(f"Error getting battery info: {e}")
            return None

    def motherboardinfo(self):
        try:
            return misc.getmotherboardinfo()
        except Exception as e:
            logging.error(f"Error getting motherboard info: {e}")
            return None

    def uptime(self):
        try:
            return misc.getuptime()
        except Exception as e:
            logging.error(f"Error getting uptime: {e}")
            return None

    def allinfos(self):
        try:
            return misc.getallinfo()
        except Exception as e:
            logging.error(f"Error getting all system info: {e}")
            return None


test = TestMisc()
cpu_info = test.cpuinfo()
print(f"CPU Info: {cpu_info}")

all_system_info = test.allinfos()
print(f"All System Info: {all_system_info}")
