#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This little app generates your TOTP from your secret (you can use
#    secret as password in a password manager), you don't need any phone or
#    other device
#    Copyright (C) 2024  TotpApp

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This little app generates your TOTP from your secret (you can use
secret as password in a password manager), you don't need any phone or
other device
"""

__version__ = "0.0.7"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This little app generates your TOTP from your secret (you can use
secret as password in a password manager), you don't need any phone or
other device
"""
__url__ = "https://github.com/mauricelambert/TotpApp"

__all__ = ["TotpApp"]

__license__ = "GPL-3.0 License"
__copyright__ = """
TotpApp  Copyright (C) 2024  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

print(copyright)

from tkinter.ttk import Style, Label, Entry, Progressbar, Button
from os.path import dirname, join, exists
from tempfile import TemporaryDirectory
from base64 import b32decode, b85decode
from struct import pack, unpack
from tkinter import Frame, Tk
from threading import Thread
from time import time, sleep
from hmac import new
from sys import exit


class TotpApp:
    def __init__(
        self, master, duration=30, character_number=6, algorithm="sha1"
    ):
        self.master = master
        self.duration = duration
        self.character_number = character_number
        self.algorithm = algorithm

        master.title("TOTP")
        master.geometry("450x150")
        master.configure(bg="#2E2E2E")
        master.iconbitmap(get_ico_file())

        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure(
            "TLabel", background="#2E2E2E", foreground="white"
        )
        self.style.configure(
            "TEntry", fieldbackground="#3E3E3E", foreground="white"
        )
        self.style.configure(
            "TProgressbar", background="#dd8a12", troughcolor="#3E3E3E",
        )
        self.style.configure(
            "TButton", background="#3E3E3E", foreground="white"
        )
        self.style.map(
            "TButton",
            background=[("active", "#4E4E4E")],
            foreground=[("active", "white")],
        )

        self.secret_frame = Frame(master, bg="#2E2E2E")
        self.secret_frame.pack(pady=10, fill="x", padx=20)

        self.secret_label = Label(self.secret_frame, text="Enter secret:")
        self.secret_label.pack(side="left", padx=(0, 10))

        self.secret_entry = Entry(self.secret_frame, show="*")
        self.secret_entry.pack(side="left")
        self.secret_entry.bind("<KeyRelease>", self.totp)

        self.secret_display = Label(self.secret_frame, text="")
        self.secret_display.pack(side="left", padx=(10, 0))

        self.clipboard_button = Button(
            self.secret_frame, text="Copy", command=self.copy_to_clipboard
        )
        self.clipboard_button.pack(side="left", padx=(10, 0))

        self.progress = Progressbar(master, length=410, mode="determinate")
        self.progress.pack(pady=20)

        self.progress_thread = Thread(target=self.update_progress)
        self.progress_thread.daemon = True
        self.progress_thread.start()

    def copy_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.secret_display["text"])

    def update_progress(self):
        start_time = time()
        duration = self.duration
        start_time = start_time - (start_time % duration)

        while True:
            elapsed_time = time() - start_time
            if elapsed_time >= duration:
                self.totp()
                start_time = time()

            progress_value = (elapsed_time / duration) * 100
            self.progress["value"] = progress_value

            sleep(0.1)
            self.master.update_idletasks()

    def totp(self, *args):
        secret = self.secret_entry.get()
        remainder = len(secret) % 8
        if remainder == 1 or remainder == 3 or remainder == 6:
            return
        secret = b32decode(secret.upper() + "=" * ((8 - len(secret)) % 8))
        time_counter = pack(">Q", int(time() / self.duration))
        hash_ = new(secret, time_counter, self.algorithm).digest()
        index = hash_[-1] & 0x0F
        value = unpack(">L", hash_[index : index + 4])[0] & 0x7FFFFFFF
        self.secret_display.config(
            text=str(value)[-self.character_number :].zfill(
                self.character_number
            )
        )


def get_ico_file():
    filename = join(dirname(__file__), "TotpApp.ico")
    if exists(filename):
        return filename

    data = b'000310RTKa00031AOK_n000&M004<lPDc$28VUda01Zh<L{b0%06YKy06Yi=0000w{Mm8<00JvXL_t(&f$dxCZG<ok4prx24_4>`VGAV02<;wSgK63g=%1$Q-NlLDq$Qtpe}LHj;zyjog>W$p&iW4Ex|<!IgdwsCF19>*C}|0oBm8`}0Sx3)1Dy^i50B%R6y5yRb$!Jusu+be7^(xc`k<zWA_I~|885b@=P(0DfM*vIYNDK^LL;Q_Wufy439MYbkRHboBP<m&ZD8c0BSIQF76h?i+0HIn(=>61iZM+S+fm$sXL|NG$o6vxw?a07#6j9Lv;vc&)hgKp6c^2PxCK=CxbBvYBR_A$;CBvzZ79Tm$o?3jN4hAexDIdIM%n&>sFB4!gTcP<FQxmnX%$<MBa*yXx+erE1oUu>@k6S$Mkq&4!_y_(OVcURO!40RvzA_VI{=`N(8}i=vV`Y(7KJm_V2fo5;vhMx0KpAWgV25u;L><lhA0*N5YHO-Ve0LDR}bfM(zA~a!JueyHwYz93nt}ZpsI(h!c$YO8e!{P)ROO(!zF_~3zuur$`Sk5RXT)Qf@d@&muozr&BLd+A=-dAsO^U-;aNKIz>LE_p1asXIw8hL3Tx^H-_pCwvb=+GDr3oI)S~h-T1)yNUI@J6rM(%T%G<W>ttby6gXJ;}PctX4IOuZkmM&MN`|HvQS|x4z6;ErVO+R@^XoWP{es0kksGXQ5zIE%bSx9($TV%6lTVze#_QkOPRv(wPCoBUldGEg$b#(kyd;#*Ex5O&}Q?dX6002ovPDHLkV1f'

    try:
        with open(filename, "wb") as file:
            file.write(b85decode(data))
    except PermissionError:
        filename = join(TemporaryDirectory(), "TotpApp.ico")
        with open(filename, "wb") as file:
            file.write(b85decode(data))

    return filename


def main():
    root = Tk()
    app = TotpApp(root)
    root.mainloop()

if __name__ == "__main__":
    exit(main())
