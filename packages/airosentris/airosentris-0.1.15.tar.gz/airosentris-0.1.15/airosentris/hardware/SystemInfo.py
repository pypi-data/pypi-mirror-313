import platform
import psutil
import GPUtil
import socket
import cpuinfo


class SystemInfo:
    def __init__(self):
        self.cpu_info = self.get_cpu_info()
        self.gpu_info = self.get_gpu_info()
        self.system_info = self.get_system_info()

    @staticmethod
    def get_common_info():
        cpu = SystemInfo.get_cpu_info()
        gpus = SystemInfo.get_gpu_info()
        system = SystemInfo.get_system_info()

        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "gpu_uuid": gpu['gpu_uuid'],
                "gpu_name": gpu['gpu_name'],
                "gpu_total_memory": gpu['gpu_total_memory'],
            })

        common_info = {
            "cpu_processor": cpu['processor'],
            "cpu_physical_core": cpu['physical_cores'],
            "cpu_total_core": cpu['total_cores'],
            "system_platform": system['platform'] + " " + system['platform_release'],
            "system_platform_version": system['platform_version'],
            "system_ram": system['ram'],
            "gpu": gpu_info
        }

        return common_info

    @staticmethod
    def get_cpu_info():
        cpu = cpuinfo.get_cpu_info()
        cpu_info = {
            "processor": cpu.get('brand_raw', 'Unknown'),
            "physical_cores": str(psutil.cpu_count(logical=False)),
            "total_cores": str(psutil.cpu_count(logical=True)),
            "max_frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
            "min_frequency": f"{psutil.cpu_freq().min:.2f}Mhz",
            "current_frequency": f"{psutil.cpu_freq().current:.2f}Mhz",
            "cpu_usage": f"{psutil.cpu_percent(interval=1)}%"
        }
        return cpu_info

    @staticmethod
    def get_gpu_info():
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "gpu_name": gpu.name,
                "gpu_total_memory": f"{gpu.memoryTotal / 1024:.0f}GB",
                "gpu_used_memory": f"{gpu.memoryUsed / 1024:.2f}GB",
                "gpu_free_memory": f"{gpu.memoryFree / 1024:.2f}GB",
                "gpu_utilization": f"{gpu.load * 100:.2f}%",
                "gpu_temperature": f"{gpu.temperature} °C",
                "gpu_uuid": gpu.uuid
            })
        return gpu_info

    @staticmethod
    def get_windows_version():
        if platform.system() != "Windows":
            return "Not applicable for non-Windows platforms"
        
        try:
            import winreg  # Only import winreg on Windows
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            release_id, _ = winreg.QueryValueEx(key, "ReleaseId")
            current_build, _ = winreg.QueryValueEx(key, "CurrentBuild")
            ubr, _ = winreg.QueryValueEx(key, "UBR")
            return f"{product_name} (Version {release_id}, Build {current_build}.{ubr})"
        except Exception as e:
            print(f"Error retrieving Windows version: {e}")
            return platform.version()

    @staticmethod
    def get_system_info():
        uname = platform.uname()
        system_info = {
            "platform": uname.system,
            "platform_release": uname.release,
            "platform_version": SystemInfo.get_windows_version() if uname.system == "Windows" else uname.version,
            "architecture": uname.machine,
            "hostname": uname.node,
            "ip_address": SystemInfo.get_ip_address(),
            "mac_address": SystemInfo.get_mac_address(),
            "ram": f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
        }
        return system_info

    @staticmethod
    def get_ip_address():
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    return addr.address
        return "N/A"

    @staticmethod
    def get_mac_address():
        for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    # Use psutil's address family for MAC address (AF_LINK for macOS and Linux)
                    if addr.family == psutil.AF_LINK:  # AF_LINK works across macOS and Linux
                        return addr.address

    def print_info(self, info, title):
        print(f"\n{title}:")
        for key, value in info.items():
            print(f"{key}: {value}")

    def display_all_info(self):
        self.print_info(self.cpu_info, "CPU Info")
        self.print_info(self.system_info, "System Info")

        if self.gpu_info:
            print("\nGPU Info:")
            for i, gpu in enumerate(self.gpu_info):
                print(f"\nGPU {i + 1}:")
                for key, value in gpu.items():
                    print(f"{key}: {value}")
        else:
            print("\nGPU Info: No GPU found")


if __name__ == "__main__":
    system_info = SystemInfo()
    system_info.display_all_info()
