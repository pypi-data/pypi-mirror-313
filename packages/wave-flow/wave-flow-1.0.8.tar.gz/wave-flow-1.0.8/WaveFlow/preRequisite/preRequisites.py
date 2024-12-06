import subprocess
import sys

class PreRequisitesWave:
    
    @staticmethod
    def __check_and_install(package_name):
        try:
            __import__(package_name)
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", package_name])
    
    @classmethod
    def VerifyRequirements(cls):
        packages = ['openpyxl', 'pandas', 'python-docx']
        for package in packages:
            cls.__check_and_install(package)

