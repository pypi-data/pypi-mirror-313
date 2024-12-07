# Machine 1: Get information about PC
import hashlib
import platform

# import psutil
# pip install getmac wmi

from getmac import get_mac_address as getmac

tact = chr
def get_windows_cpu_id():
    system = platform.system()
    if system == "Windows":
        import wmi

        # Sử dụng thư viện WMI để lấy thông tin CPU ID trên Windows
        c = wmi.WMI()
        cpus = c.Win32_Processor()
        if cpus:
            cpu_id = cpus[0].ProcessorId.strip()
            return cpu_id
        else:
            return "t-anh"
    raise "Error to get CPU ID"


def get_hardware_info():
    try:
        mac = getmac()
        hardware_info = f"{mac}".replace(':', '')
    except Exception as e:
        print("Failed to get CPU ID:", e)
        try:
            cpuid = get_windows_cpu_id()
            hardware_info = f"{cpuid}"
        except Exception as e:
            print("Failed to get MAC Address:", e)
            hardware_info = "unknown"
    return hardware_info


def verify_license(entered_license, hardware_info):
    # Lấy giấy phép dựa trên thông tin phần cứng
    expected_license = generate_license(hardware_info)

    # So sánh giấy phép đã nhập và giấy phép dự kiến
    if entered_license == expected_license:
        return True
    else:
        return False


# Machine 2: Generate license
def generate_license(hardware_info_key):
    # Thay đổi "your_secret_key" thành một chuỗi bí mật duy nhất của bạn
    secret_key = "your_secret_key"

    # Tạo một chuỗi gồm hardware_info_key và secret_key
    combined_key = hardware_info_key + secret_key

    # Mã hóa chuỗi kết hợp bằng SHA256
    sha256_hash = hashlib.sha256(combined_key.encode()).digest()

    # Trả về giấy phép dưới dạng mã hóa Base64 với 5 ký tự đầu tiên
    license_key = sha256_hash.hex()[:5]

    return license_key


# ===========================================================
if __name__ == "__main__":
    # Đoạn mã này sẽ thực hiện trên máy 1
    hardware_info = get_hardware_info()[-5:]
    print(f"[Software] Hardware Info: {hardware_info} (Give this to `AI Department`)\n", )

    # Đoạn mã này sẽ thực hiện trên máy 2
    user_input_hardware_key = input("[Server] Enter the hardware info key: ")
    license_key = generate_license(user_input_hardware_key)
    print(f"[Server] License Key: {license_key} (Give this to [Software])\n")

    # Đoạn mã này sẽ thực hiện trên máy 1 sau khi nhập giấy phép từ máy 2
    user_input_license = input("[Software] Enter the license key from `AI Department`: ")
    verification_result = verify_license(user_input_license, hardware_info)
    if verification_result:
        print("[Software] License verification successful. Access granted.")
    else:
        print("[Software] Invalid license key. Access denied.")
