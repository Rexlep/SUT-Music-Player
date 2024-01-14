"""
Hover for python interface
Author: REXLEP
"""


from tkinter import *


class HoverWindow(object):
    """This class use for hover window"""

    def __init__(self, widget, duration=1, font=None, bg="#2B2B2B", fg="#ffffff", border_width=1, border_color="#000000",
                 move_with_mouse=True):
        """Initialize hover window elements"""
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.duration = duration * 1000
        self.font = font if font else ("tahoma", "12", "normal")
        self.bg = bg
        self.fg = fg
        self.border_width = border_width
        self.border_color = border_color
        self.move_with_mouse = move_with_mouse

    def showtip(self, text):
        """This function display text in tooltip window"""
        self.text = text

        # Cancel any scheduled tooltip display
        if self.id:
            self.widget.after_cancel(self.id)

        # Schedule the tooltip to be displayed after the duration
        self.id = self.widget.after(self.duration, lambda: self._showtip(text))

    def _showtip(self, text):
        """This function make hover window"""
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x_pos, y_pos = self.widget.winfo_pointerxy()  # Get current mouse position
        x = x_pos + 10
        y = y_pos + 10
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            tw,
            text=text,
            justify=LEFT,
            background=self.bg,
            foreground=self.fg,
            relief=SOLID,
            borderwidth=self.border_width,
            font=self.font
        )
        label.pack(ipadx=1)
        if self.move_with_mouse:
            tw.bind('<Motion>', self.on_tooltip_motion)  # Bind <Motion> event

    def on_tooltip_motion(self, event):
        """This function make your hover window move with your mouse movement"""
        if not self.tipwindow:
            return

        x = event.x_root + 10
        y = event.y_root + 10
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))

    def hidetip(self):
        """This function hide the window"""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None


def Hover(widget, text, duration=0, font=None, bg="#2B2B2B", fg="#ffffff", border_width=1, move_with_mouse=True):
    toolTip = HoverWindow(widget, duration, font, bg, fg, border_width, move_with_mouse)
    """This function allow you to make a hover window for your interface widget"""

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    widget.bind('<Motion>', toolTip.on_tooltip_motion)