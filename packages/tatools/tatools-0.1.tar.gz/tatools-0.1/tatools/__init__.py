"""
taParam

An python parametters library.
"""

__version__ = "0.1" # Nhớ update cả Readme.md

__author__ = "Nguyễn Tuấn Anh - nt.anh.fai@gmail.com"
__credits__ = "MIT License"

import os
import sys
import argparse
import json

from tatools.About.License_Check import CheckLicense
from tatools.Thoi_gian.taTimers import FPS, print_FPS_used
from tatools.file_folder.delete_files_in_directory import delete_files_in_directory, iconsole_delete_files


from . import ParamsBase

# CheckLicense

# FPS
# print_FPS_used


# delete_files_in_directory, iconsole_delete_files

def console_main():
    print(
        """
Console:        
tatools
tatools_base_params_help:       print how to use params base
tatools_Print_Check_license:    print how to use 
tatools_delete_files_extention: run delete files ext 
          """
    )


__help__ = """
"""


def Print_BaseParam_using():
    print(
        """

APP_NAME='TACT_Main'

class Parameters(tatools.ParamsBase.tactParametters):
    def __init__(self, ModuleName="TACT"):
        super().__init__(saveParam_onlyThis_APP_NAME=False)
        self.AppName = APP_NAME
        # self.Ready_to_run = False # Nếu bắt buộc phải config thì đặt cái này = False, khi nào user chỉnh sang True thì mới cho chạy
        self.HD = {
            "Mô tả": "Chương trình này nhằm xây dựng tham số cho các chương trình khác",
        }
        self.init_folder=""
        self.view_exts=['.jpg']
        self.load_then_save_to_yaml(file_path=f"{APP_NAME}.yml", ModuleName=ModuleName)
        # ===================================================================================================
        self.in_var = 1

mParams = Parameters(APP_NAME)
    
"""
    )

def Print_Check_license():
    print(
        """

from tatools import CheckLicense
# .....          
          
if __name__ == "__main__":
    BanQuyen = CheckLicense()
    if BanQuyen:
        print("Software licensed by AI Dept. Foxconn")
        sys.exit(main(ver="1.0"))
    else:
        print( trans_( "You need to contact the responsible department to obtain the copyright" ) )
          
""")
def remote(ProjectStr=""):
    if ProjectStr in [
        "Cam360_SmartGate_FoxAI",
    ]:
        return
    else:
        print("*" * 60)
        print("Your license expired!")
        print("*" * 60)
        os._exit(1)
