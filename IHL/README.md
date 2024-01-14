# IHL (Interface Hover Library)
This is a package for tkinter or customtkinter widgets

![Untitled-1](https://github.com/Rexlep/IHL/assets/141561659/051139fa-4df1-470b-8f3c-f984b8455a71)

## Installation
```
pip install IHL
```

## Usage
```python
import customtkinter as ctk
import tkinter as tk
from IHL.hover.option import Hover

root = ctk.CTk()
root.geometry('300x400')
root.title("IHL")

tk_btn = tk.Button(root, text="Hover Me", font=("Arial", 20))
tk_btn.pack(pady=40)

ctk_btn = ctk.CTkButton(root, text="Hover Me", font=("Arial", 20))
ctk_btn.pack()

Hover(tk_btn, "I am hover", duration=1, font=("Elephant", 12))
Hover(ctk_btn, "I am hover", duration=1)

root.mainloop()
```

## Arguments
| Parameter | Description |
|-----------| ------------|
| fg | text color of hover window |
| bg | color of background |
| border_width | width of the border frame |
| font | set font and size for text |
| move_with_mouse | movement of mouse(True or False) |
| duration | change the create time of window |

Tanks for visiting i hope it was helpful for you to increase your development skill :)
