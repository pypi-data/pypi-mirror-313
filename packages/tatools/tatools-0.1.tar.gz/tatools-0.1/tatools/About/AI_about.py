import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkscrolled

Version = "1.0"
gioithieu = """
Chương trình ghi hình nhiều RTSP, lưu vào file, 

- Có thể cấu hình các tham số được
- Có thể lưu trữ các tham số và tự load lại khi khởi động
"""


class AboutForm(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.geometry("650x480")
        self.title("About")

        # Create a frame for the title
        frame_title = tk.Frame(self, height=120)
        frame_title.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Add a label for the title
        lbl_title = tk.Label(frame_title, text="AI IVIS - Intelligent Visual Inspection System of AI Department", font=("Helvetica", 16))
        lbl_title.pack(pady=10)
        frame_text = tk.Frame(self)
        frame_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        nrowtxt = 20
        COMtxt = tkscrolled.ScrolledText(frame_text, height=nrowtxt, bg='AliceBlue', wrap='none', undo=True)
        COMtxt.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        xsb = tk.Scrollbar(frame_text, orient="horizontal", command=COMtxt.xview, width=20)
        xsb.pack(pady=5, padx=5, fill='x', expand=True)

        COMtxt.configure(xscrollcommand=xsb.set,width=20)
        COMtxt.insert(tk.END, gioithieu)

        # Create a frame for the version number
        frame_version = tk.Frame(self, height=120)
        frame_version.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Add a label for the version number
        lbl_version = tk.Label(frame_version, text=f"Version {Version}", font=("Helvetica", 12))
        lbl_version.pack(pady=5)

        # Add a button to close the form
        btn_close = ttk.Button(frame_version, text="Close", command=self.destroy)
        btn_close.pack(pady=10)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("400x300")

    # Add a button to open the About form
    btn_about = ttk.Button(root, text="About", command=lambda: AboutForm(root))
    btn_about.pack(pady=10)

    root.mainloop()
