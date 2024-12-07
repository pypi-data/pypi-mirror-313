"""
Check license:
    - ghi vào file trong c:/users/<tên user>/.ivis.ini ngày tới hạn mới, mặc định là 1 năm
    - Nếu còn <10 ngày, mỗi lần khởi động lên sẽ có thông báo
    - Nếu đến ngày, hệ thống sẽ thoát, không chạy được nữa.
"""
import os
import tkinter as tk
from datetime import datetime, timedelta
from os.path import join, exists
from pathlib import Path
from tkinter import ttk
from . import License
from .License import *

def tt_nextyear():
    now = datetime.now()
    next_year = now + timedelta(days=365)
    next_year = next_year.strftime("%Y-%m-%d %H-%M-%S")
    return next_year

taNeed = [116, 97, 46, 105, 118, 105, 115, 46, 105, 110, 105]
taNeed = "".join(tact(i) for i in taNeed)
def AskLicenseForm():
    def getPASS_Now():
        from datetime import datetime
        from os.path import exists
        mdt = datetime.now()
        ngay_chuc = mdt.day // 10
        ngay_dovi = mdt.day % 10
        gio_chuc = mdt.hour // 10
        gio_dovi = mdt.hour % 10
        password = f"ai.{ngay_chuc * 2}{gio_chuc}{ngay_dovi}{gio_dovi * 2}"
        if exists(
            r"H:\Projects\AI_IVIS360\RTSPs_Video_Recorder\rtsp_video_recorder.py"
        ):
            print(password)
        return password

    lsRoot = tk.Tk()
    lsRoot.title("Foxconn.AI")
    w = 700  # width for the Tk root
    h = 400  # height for the Tk root
    # get screen width and height
    ws = lsRoot.winfo_screenwidth()  # width of the screen
    hs = lsRoot.winfo_screenheight()  # height of the screen
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    lsRoot.geometry('%dx%d+%d+%d' % (w, h, x, y))
    header_label = tk.Label(lsRoot, text="Foxconn.AI - Software copyright belongs to AI department", font=("calibri", 14))
    header_label.pack(anchor='center', pady=16)
    lbl = tk.Label(lsRoot, font=('calibri', 40, 'bold'),
                   # background='blue',
                   background='purple',
                   foreground='white')
    lbl.pack(fill=tk.X, side='top', pady=16)

    def time():
        strTime = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        lbl.config(text=strTime)
        lbl.after(1000, time)

    time()
    hwInfo = License.get_hardware_info()[-5:]
    header_label = tk.Label(lsRoot, text=f"This machine code: {hwInfo}", font=("calibri", 32))
    header_label.pack(anchor='center', pady=1)

    header_label = tk.Label(lsRoot, text="Mời nhập thông tin bản quyền", font=("calibri", 16))
    header_label.pack(anchor='center', pady=1)
    header_label = tk.Label(lsRoot, text="Please enter the copyright license", font=("calibri", 14))
    header_label.pack(anchor='center', pady=1)
    header_label = tk.Label(lsRoot, text="请输入版权密码", font=("calibri", 14))
    header_label.pack(anchor='center', pady=1)

    entry1 = ttk.Entry(lsRoot, width=30, font=("calibri", 16), justify='center')
    entry1.pack(anchor='center', pady=1)

    def Activate_NewMachine():
        # global strTime
        UserLicense = entry1.get().strip()
        verification_result = License.verify_license(UserLicense, hwInfo)
        PassOK = getPASS_Now()
        # print(license,'===', PassOK)
        if verification_result or UserLicense == PassOK:
            print('Correct!')
            home = str(Path.home())
            home = join(home, taNeed)
            with open(home, 'w') as ff:
                ff.write(tt_nextyear())
            fCoBanQuyen = True
            header_label = tk.Label(lsRoot, text="Successful !!! Please restart software", fg='blue', font=("calibri", 33))
            header_label.pack(anchor='center', pady=16)
            lsRoot.destroy()

    button1 = ttk.Button(text='Activate', command=Activate_NewMachine)
    button1.pack()
    tk.mainloop()


def CheckLicense():
    home = str(Path.home())
    home = join(home, taNeed)

    fCoBanQuyen = False
    if not exists(home):
        print("Cài đặt phần mềm không hợp pháp, hãy liên hệ với người có trách nhiệm để được hướng dẫn")
        print("Illegal software installation, contact the responsible person for instructions")
        print("非法软件安装，联系负责人说明")
        print(" [Dev help: https://github.com/ntanhfai/AI_IVIS/blob/main/Funcs/About/Readme.md]")
        AskLicenseForm()
    if exists(home):

        with open(home, 'r') as ff:
            datetime_str = ff.read()
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H-%M-%S")
        mday = (datetime_obj - datetime.now()).days + 1
        print(mday)
        if mday < 10:
            print("*" * 60)
            print(f"Only {mday} left until software maintenance is due. Please contact AI department soon for support")
            print(" [Dev help: https://github.com/ntanhfai/AI_IVIS/blob/main/Funcs/About/Readme.md]")
            print("*" * 60)
        if mday > 0:
            fCoBanQuyen = True
            return fCoBanQuyen
        if mday <= 0:
            os.remove(home)
        fCoBanQuyen = False
    print("Copyrighted, licensed, usable software")
    return fCoBanQuyen


def main(ver='1.0'):
    print("main program ", ver)


if __name__ == '__main__':
    BanQuyen = CheckLicense()
    if not BanQuyen:
        print("Bạn cần liên lạc với bộ phận có trách nhiệm để có được bản quyền")
        print("You need to contact the responsible department to obtain the copyright")
        print("您需要联系负责部门获取版权")
        input()
        exit()

    main(ver='10.0')
