# Enterprise-level OS Environment Detector
# This class provides comprehensive system information gathering capabilities
# suitable for large-scale deployments and complex infrastructure environments.

import platform
import os
import distro
import subprocess
import shutil

class OSEnvironmentDetector:
    def __init__(self):
        # Initialize os_data as empty string, will be populated on first get_all_info call
        self.os_data = ""

    def _gather_os_info(self):
        """
        The OSEnvironmentDetector gathers comprehensive OS information for any platform (Windows, macOS, Linux, etc.) to support AI for dependency installation.
        """
        os_info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Architecture": platform.architecture(),
            "Python Version": platform.python_version(),
            "Python Implementation": platform.python_implementation(),
            "Python Compiler": platform.python_compiler(),
            "Python Build": platform.python_build(),
            "OS Environment Variables": dict(os.environ),
            "User Home": os.path.expanduser('~'),
        }

        # The OSEnvironmentDetector adds more detailed information based on the OS
        if os_info["System"].lower() == "linux":
            os_info.update({
                "Linux Distribution Name": distro.name(),
                "Linux Distribution Version": distro.version(),
                "Linux Distribution ID": distro.id(),
                "Linux Distribution Codename": distro.codename(),
                "Linux Distribution Like": distro.like(),
                "Package Managers": {
                    "apt": self._get_version("apt"),
                    "yum": self._get_version("yum"),
                    "dnf": self._get_version("dnf"),
                    "pacman": self._get_version("pacman"),
                    "zypper": self._get_version("zypper"),
                },
            })
        elif os_info["System"].lower() == "darwin":
            os_info.update({
                "macOS Version": platform.mac_ver()[0],
                "Xcode Command Line Tools": self._get_xcode_cli_tools_version(),
            })
        elif os_info["System"].lower() == "windows":
            os_info.update({
                "Windows Version": platform.win32_ver()[0],
                "PowerShell Version": self._get_powershell_version(),
                "Chocolatey": self._get_version("choco"),
                "Scoop": self._check_scoop_installed(),
            })

        # The OSEnvironmentDetector adds information about common package managers and development tools
        os_info.update({
            "Package Managers": {
                "pip": self._get_version("pip"),
                "npm": self._get_version("npm"),
                "yarn": self._get_version("yarn"),
                "pnpm": self._get_version("pnpm"),
                "brew": self._get_version("brew"),
                "conda": self._get_version("conda"),
                "poetry": self._get_version("poetry"),
                "cargo": self._get_version("cargo"),
                "gem": self._get_version("gem"),
                "composer": self._get_version("composer"),
            },
            "Development Tools": {
                "git": self._get_version("git"),
                "docker": self._get_version("docker"),
                "kubectl": self._get_version("kubectl"),
                "terraform": self._get_version("terraform"),
                "ansible": self._get_version("ansible"),
                "vagrant": self._get_version("vagrant"),
            },
            "Build Tools": {
                "make": self._get_version("make"),
                "cmake": self._get_version("cmake"),
                "gradle": self._get_version("gradle"),
                "maven": self._get_version("mvn"),
            },
        })

        # The OSEnvironmentDetector removes None values
        os_info["Package Managers"] = {k: v for k, v in os_info["Package Managers"].items() if v is not None}
        os_info["Development Tools"] = {k: v for k, v in os_info["Development Tools"].items() if v is not None}
        os_info["Build Tools"] = {k: v for k, v in os_info["Build Tools"].items() if v is not None}

        return os_info

    def _get_version(self, command):
        """Generic method to get version of a command-line tool."""
        try:
            result = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def _get_xcode_cli_tools_version(self):
        """Get Xcode Command Line Tools version on macOS."""
        try:
            result = subprocess.run(["xcode-select", "--version"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def _get_powershell_version(self):
        """Get PowerShell version on Windows."""
        try:
            result = subprocess.run(["powershell", "$PSVersionTable.PSVersion"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def _check_scoop_installed(self):
        """Check if Scoop is installed on Windows."""
        return "Installed" if shutil.which("scoop") else None

    def get_os_info(self):
        """
        The OSEnvironmentDetector returns a dictionary with detailed OS information.
        """
        if self.os_data == "":
            self.os_data = self._gather_os_info()
        return self.os_data

    def get_all_info(self):
        """
        A function to return all necessary OS information in one call.
        """
        if self.os_data == "":
            self.os_data = self._gather_os_info()
        return self.os_data

    def __str__(self):
        """
        The OSEnvironmentDetector returns a formatted string of the OS information.
        """
        if self.os_data == "":
            self.os_data = self._gather_os_info()
        return '\n'.join([f'{key}: {value}' for key, value in self.os_data.items()])
