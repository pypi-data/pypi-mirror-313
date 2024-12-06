import os
import platform
import sys

def get_architecture():
    arch = platform.machine().lower()
    system = platform.system().lower()

    if arch == 'x86_64':
        if system == 'linux':
            return 'linux-amd64'
        elif system == 'windows':
            return 'win-i686.exe'
    if arch == 'amd64':
        if system == 'linux':
            return 'linux-amd64'
        elif system == 'windows':
            return 'win-i686.exe'
    elif arch == 'i686' or arch == 'x86':
        if system == 'windows':
            return 'win-i686.exe'
    elif arch == 'aarch64':
        if system == 'linux':
            return 'linux-arm64'
    elif arch == 'loongarch64':
        if system == 'linux':
            return 'linux-loongarch64'
    elif arch == 'riscv64':
        if system == 'linux':
            return 'linux-riscv64'
    elif arch.startswith('arm'):
        if system == 'linux':
            return 'linux-armbi'
    elif arch == 'sw_64':
        if system == 'linux':
            return 'linux-sw_64'

    return 'unknown'

def main():
    print("dfss python tool, version: v1.7.12")
    binary_arch = get_architecture()
    
    if binary_arch == 'unknown':
        arch = platform.machine().lower()
        system = platform.system().lower()
        print("Unsupported architecture or operating system")
        print("arch:" + arch)
        print("system:" + system)
        return 1
    print("Find architecture: " + binary_arch)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    binary_name = 'dfss-cpp-' + binary_arch
    binary_path = os.path.join(script_dir, 'output', binary_name)
    if not os.path.isfile(binary_path):
        print("Binary file for architecture " + binary_arch + " not found at " + binary_path)
        return 1
    args = sys.argv[1:]
    try:
        ret = os.system(binary_path + " " + ' '.join(args))
        print("Binary for architecture " + binary_arch + " ret: " + str(ret))
        if ret == 0:
            return 0
        else:
            return 1
    except Exception as e:
        print("Failed to execute binary for architecture " + binary_arch + " : " + str(e))
        return 1

if __name__ == '__main__':
    ret = main()
    exit(ret)
