import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from math import floor
from modules.location import *
import animate as animate
import animate.controllers as controller

class Window(tk.Tk):

    def __init__(self, title: str = "macOS Window", width: int = 200, height: int = 200,
                 top: int = 20, left: int = 20):
        super().__init__()

        self.wm_geometry(f"{width}x{height}+{top}+{left}")
        self.wm_title(title)
        self.wm_overrideredirect(True)

        self.font = tkFont.Font(family="PingFang", font=("PingFang", 10), file="./fonts/pingfang0.ttf")
        self.option_add("*Font", self.font)



class Canvas(tk.Canvas):

    """
    Main Canvas
    `master`: Parent window
    `width`: Canvas width
    `height`: Canvas height
    """

    def __init__(self, master: tk.Tk | tk.Toplevel, width, height):
        super().__init__(master, width=width, height=height)


class Misc:

    """
    Misc class
    `get_image()`: Use `PIL.Image` get Image
        `filename`: Image file's path
        `width`: Image width
        `height`: Image height
    """

    def __init__(self, *args):
        self.error = self.get_image("./images/error.png", 64, 64)
        self.warning = self.get_image("./images/warning.png", 64, 64)

    def get_image(self, filename, width, height):  # type: (str, int, int) -> Image
        return Image.open(filename).resize((width, height))

    def percentage_to_int(self, percentage: str, main: int):
        if percentage.endswith("%"):
            percentage.replace("%", "")
            percentage = int(percentage) / 100
            return main * percentage


class BigButton(Misc):

    """
    BigButton
    `canvas`: Parent Canvas
    `width`: Button width
    `height`: Button height
    `top`: Button's y
    `left`: Button's x
    `text`: Text on Button
    `color`: Text color
    `command`: Click Button's command    
    """

    def __init__(self, canvas: tk.Canvas, width: int = 228, height: int = 28, top: int = 20,
                 left: int = 20, text: str = "BigButton", color: str = "#ffffff", command=None):
        super().__init__()
        self.canvas = canvas
        self.text = text
        self.x = floor(left + (width / 2))
        self.y = floor(top + (height / 2))
        self.bg_pic = ImageTk.PhotoImage(
            self.get_image("./images/BigButton.png", width, height))
        self.bg = self.canvas.create_image(
            self.x, self.y, image=self.bg_pic)
        self.txt = self.canvas.create_text(
            self.x, self.y, text=self.text, fill=color)
        self.canvas.tag_bind(self.bg, "<Button-1>", command)
        self.canvas.tag_bind(self.txt, "<Button-1>", command)


class Notification(Misc, tk.Toplevel):

    """
    Notification (Toast)

    Show a notification in the screen
    `title`: Notification title
    `message`: Notification message
    `icon`: Notification icon
    `command`: Click it's command
    """

    def __init__(self, *, title: str | None, message: str | None,
                 icon: str | tk.PhotoImage, command=None):
        super().__init__()
        tk.Toplevel.__init__(self)

        self.overrideredirect(True)

        self.x = floor(self.winfo_screenwidth() - 346 - 12)
        self.y = 40
        self.wm_geometry(f"346x76+{self.x}+{self.y}")

        self.title = title
        self.message = message
        self.icon = icon
        self.command = command

        if self.icon == 'error':
            self.usr_image = ImageTk.PhotoImage(self.error.resize((40, 40)))
        elif self.icon == 'warning':
            self.usr_image = ImageTk.PhotoImage(self.warning.resize((40, 40)))
        else:
            self.usr_image = ImageTk.PhotoImage(
                self.get_image(self.icon, 40, 40))

        self.canvas = tk.Canvas(self, width=346, height=76)
        self.canvas.pack(fill='both')

        self._img = self.canvas.create_image(30, 37.5, image=self.usr_image)
        self._title = self.canvas.create_text(
            58 + (255 / 2), 25, text=self.title)
        self._text = self.canvas.create_text(
            58 + (255 / 2), 46.5, text=self.message)

        self.bind_all("<Button-1>", self.command)


class Dialog(Misc, tk.Toplevel):

    """
    macOS Dialog
    `title`: Dialog title
    `text`: Dialog text
    `button`: Dialog's button text
    `command`: Click button's command
    `image`: Dialog's image
    `drag`: Can it drag
    """

    def __init__(self, *, title: str, text: str, button: str, command=None,
                 image: str | tk.PhotoImage = 'warning', drag: bool = True):
        super().__init__()
        tk.Toplevel.__init__(self)

        self._command = command
        self.title = title
        self.text = text
        self.button = button

        self.overrideredirect(True)

        if image == 'error':
            self.usr_image = ImageTk.PhotoImage(self.error)
        elif image == 'warning':
            self.usr_image = ImageTk.PhotoImage(self.warning)
        else:
            self.usr_image = ImageTk.PhotoImage(self.get_image(image, 64, 64))

        self.top = floor((self.winfo_screenwidth() - 265) / 2)
        self.left = floor((self.winfo_screenheight() - 260) / 2)
        self.wm_geometry(f"260x265+{self.top}+{self.left}")

        self.canvas = tk.Canvas(
            self, width=260, height=265, relief='flat', bd=0)
        self.canvas.pack(fill='both')
        self.canvas.create_image(130, 52, image=self.usr_image)
        self.canvas.create_text(130, 112, text=self.title, fill="#000000")
        self.canvas.create_text(
            130, 151, text=self.text, fill="#000000", width=225)
        self.btn = BigButton(self.canvas, text=self.button,
                             command=self._command, top=188, left=16)

        if drag:
            self.offset_x = 0
            self.offset_y = 0

            self.bind("<ButtonPress-1>", self.__start_drag)
            self.bind("<ButtonRelease-1>", self.__stop_drag)
            self.bind("<B1-Motion>", self.__on_drag)
        else:
            print('Drag disabled')

    def __start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def __stop_drag(self, _event):
        self.offset_x = 0
        self.offset_y = 0

    def __on_drag(self, _event):
        x = self.winfo_pointerx() - self.offset_x
        y = self.winfo_pointery() - self.offset_y
        self.geometry(f"+{x}+{y}")


class Button(Misc):

    """
    macOS Button
    `canvas`: Parent Canvas
    `style`: Change style (Primary style and Normal style)
    `text`: Button text
    `width`: Button width
    `height`: Button height
    `top`: Button's y
    `left`: Button's x
    `command`: Click it's command
    """

    def __init__(self, canvas: tk.Canvas, style: str = "primary", text: str = None,
                 width: int = 47, height: int = 22, top: int = 20, left: int = 20, command=None):
        super().__init__()

        self.canvas = canvas
        self.width = width
        self.height = height
        self.style = style
        self.top = top
        self.left = left
        self.text = text
        self.command = command

        self.bg_normal = ImageTk.PhotoImage(self.get_image(
            "./images/NormalButton-normal.png", self.width, self.height))
        self.bg_primary = ImageTk.PhotoImage(self.get_image(
            "./images/NormalButton-primary.png", self.width, self.height))
        self.x = left + width / 2
        self.y = top + height / 2

        if style == 'primary':
            self.bg = self.canvas.create_image(
                self.x, self.y, image=self.bg_primary)
            self.btn = self.canvas.create_text(
                self.x, self.y, text=self.text, fill="#ffffff")
        elif style == 'normal':
            self.bg = self.canvas.create_image(
                self.x, self.y, image=self.bg_normal)
            self.btn = self.canvas.create_text(
                self.x, self.y, text=self.text, fill="#000000")
        else:
            raise ValueError(f"Unknown style: {self.style}")

        self.canvas.tag_bind(self.bg, "<Button-1>", self.command)
        self.canvas.tag_bind(self.btn, "<Button-1>", self.command)


class CheckBox(Misc):

    """
    macOS CheckBox
    `canvas`: Parent Canvas
    `text`: CheckBox's text
    `width`: CheckBox's width
    `height`: CheckBox's height
    `top`: CheckBox's y
    `left`: CheckBox's x
    `command`: Click it's command
    """

    def __init__(self, canvas: tk.Canvas, text: str = None, width: int = 53, height: int = 16,
                 top: int = 20, left: int = 20, command=None):
        super().__init__()

        self.canvas = canvas
        self.text = text
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.command = command

        self.click_status = False

        self.images = [ImageTk.PhotoImage(self.get_image("./images/not-check.png", 16, 16)),
                       ImageTk.PhotoImage(self.get_image("./images/checked.png", 16, 16))]

        self.image_x = self.left + 16 / 2
        self.image_y = self.top + 16 / 2
        self.text_x = self.left + 20 + 33 / 2
        self.text_y = self.top + 16 / 2

        self.image = self.canvas.create_image(
            self.image_x, self.image_y, image=self.images[0])
        self.canvas.create_text(self.text_x, self.text_y, text=self.text)

        self.canvas.tag_bind(self.image, "<Button-1>", self.click)

    def click(self, _event):
        if self.click_status:
            self.canvas.delete(self.image)
            self.image = self.canvas.create_image(
                self.image_x, self.image_y, image=self.images[0])
            self.canvas.tag_bind(self.image, "<Button-1>", self.click)
            self.click_status = False
        else:
            self.canvas.delete(self.image)
            self.image = self.canvas.create_image(
                self.image_x, self.image_y, image=self.images[1])
            if self.command:
                self.command(_event)
            self.canvas.tag_bind(self.image, "<Button-1>", self.click)
            self.click_status = True


class RadioButton(Misc):

    """
    macOS RadioButton
    `canvas`: Parent Canvas
    `text`: RadioButton's text
    `width`: RadioButton's width
    `height`: RadioButton's height
    `top`: RadioButton's y
    `left`: RadioButton's x
    `command`: Click it's command
    """

    def __init__(self, canvas: tk.Canvas, text: str = None, width: int = 53, height: int = 16,
                 top: int = 20, left: int = 20, command=None):
        super().__init__()

        self.canvas = canvas
        self.text = text
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.command = command

        self.click_status = False

        self.images = [ImageTk.PhotoImage(self.get_image("./images/not-radio.png", 16, 16)),
                       ImageTk.PhotoImage(self.get_image("./images/radioed.png", 16, 16))]

        self.image_x = self.left + 16 / 2
        self.image_y = self.top + 16 / 2
        self.text_x = self.left + 20 + 33 / 2
        self.text_y = self.top + 16 / 2

        self.image = self.canvas.create_image(
            self.image_x, self.image_y, image=self.images[0])
        self.canvas.create_text(self.text_x, self.text_y, text=self.text)

        self.canvas.tag_bind(self.image, "<Button-1>", self.click)

    def click(self, _event):
        if self.click_status:
            self.canvas.delete(self.image)
            self.image = self.canvas.create_image(
                self.image_x, self.image_y, image=self.images[0])
            self.canvas.tag_bind(self.image, "<Button-1>", self.click)
            self.click_status = False
        else:
            self.canvas.delete(self.image)
            self.image = self.canvas.create_image(
                self.image_x, self.image_y, image=self.images[1])
            if self.command:
                self.command(_event)
            self.canvas.tag_bind(self.image, "<Button-1>", self.click)
            self.click_status = True


class ProcessBar(Misc):
    ...


class List(Misc):

    """
    List

    `canvas`: Parent Canvas
    `width`: List's width
    `height`: List's height
    `text`: Items text (list)
    `top`: List's y
    `left`: List's x

    """

    def __init__(self, canvas: tk.Canvas, width: int = 170, height: int = 281,
                 text: list[str] = [], top: int = 20, left: int = 20):
        super().__init__()

        self.canvas = canvas
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.text = text
        self.x = left + width / 2
        self.y = top + height / 2
        self.first_text_y = self.top + 16
        self.text_x = 12 + 33 / 2

        self.bg = ImageTk.PhotoImage(self.get_image(
            "./images/List-Background.png", self.width, self.height))
        self.footer = ImageTk.PhotoImage(
            self.get_image("./images/List-Footer.png", 41, 20))
        self.checked = ImageTk.PhotoImage(
            self.get_image("./images/List-Checked.png", 162, 24))

        self.canvas.create_image(self.x, self.y, image=self.bg)
        self.draw_text()

        self.canvas.bind("<Button-1>", self.on_click)

    def draw_text(self):
        self.text_labels = []
        for text_item in self.text:
            if len(text_item) > 1:
                self.text_x += 2 * len(text_item)
                print(111)
            label = self.canvas.create_text(
                self.text_x, self.first_text_y, text=text_item, fill="#000000")
            self.text_labels.append(label)
            self.first_text_y += 24
            self.text_x = 12 + 33 / 2

    def on_click(self, event):
        for label in self.text_labels:
            x0, y0, x1, y1 = self.canvas.bbox(label)
            if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                try:
                    self.canvas.itemconfigure(
                        self.selected_label, fill="#000000")
                    self.canvas.delete(self.check)
                except:
                    pass
                self.canvas.itemconfigure(label, fill="#ffffff")
                self.selected_label = label
                self.check = self.canvas.create_image(
                    x0 + 81, y1 - 8, image=self.checked)
                self.canvas.lift(label, self.check)


class Entry(Misc):

    """
    # Coding
    """

    def __init__(self, canvas: tk.Canvas, *, text: str = None, width: int = 206, height: int = 22,
                 top: int = 20, left: int = 20):
        super().__init__()

        self.canvas = canvas
        self.text = text
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.x = self.left + self.width / 2
        self.y = self.top + self.height / 2
        self.text_x = 7 + 36

        self.images = [ImageTk.PhotoImage(self.get_image("./images/TextEntry-Background.png", self.width, self.height)),
                       ImageTk.PhotoImage(self.get_image(
                           "./images/TextEntry-Background-Filled.png", self.width, self.height))
                       ]

        self.bg = self.canvas.create_image(
            self.x, self.y, image=self.images[0])

        self.canvas.tag_bind(self.bg, "<Button-1>", self.__click)
        self.canvas.bind("<Button-1>", self.__unclick_outside)

    def __click(self, _event: tk.Event):
        if self.canvas.itemcget(self.bg, 'image') == str(self.images[1]):
            return
        self.canvas.delete(self.bg)
        self.bg = self.canvas.create_image(
            self.x, self.y, image=self.images[1])
        self.canvas.bind("<Button-1>", self.__unclick_outside)
        self.canvas.tag_bind(self.bg, "<Key>", self.__key)

    def __unclick(self, _event: tk.Event):
        self.canvas.delete(self.bg)
        self.bg = self.canvas.create_image(
            self.x, self.y, image=self.images[0])
        self.canvas.tag_bind(self.bg, "<Button-1>", self.__click)

    def __unclick_outside(self, event: tk.Event):
        x, y = event.x, event.y
        bg_bbox = self.canvas.bbox(self.bg)
        if bg_bbox[0] <= x <= bg_bbox[2] and bg_bbox[1] <= y <= bg_bbox[3]:
            return
        self.__unclick(None)

    def __key(self, event: tk.Event):
        keys = event.keysym
        print(keys)


class Switch(Misc):

    """
    Switch

    `canvas`: Parent Canvas
    `width`: Switch's width
    `height`: Switch's height
    `top`: Switch's y
    `left`: Switch's x
    `status`: Switch's status (ON | OFF)
    `command`: Switch on and off's commands (list)

    """

    def __init__(self, canvas: tk.Canvas, *, width: int = 26, height: int = 15,
                 top: int = 20, left: int = 20, status: str = OFF, command: list = None):
        super().__init__()

        self.canvas = canvas
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.status = status
        self.command = command
        self.x = self.left + self.width / 2
        self.knob_x = [self.left + 1 + 13 / 2, self.left + 12 + 13 / 2]
        self.y = self.top + self.height / 2
        self.knob_y = self.top + 1 + 13 / 2

        self.images = [ImageTk.PhotoImage(self.get_image("./images/Switch-On.png", self.width, self.height)),
                       ImageTk.PhotoImage(self.get_image(
                           "./images/Switch-Off.png", self.width, self.height))
                       ]
        self.knob_img = [ImageTk.PhotoImage(self.get_image("./images/Switch-Off-Knob.png", 13, 13)),
                         ImageTk.PhotoImage(self.get_image(
                             "./images/Switch-On-Knob.png", 13, 13))
                         ]

        self.fill_img = [ImageTk.PhotoImage(self.get_image("./images/Switch-Off-Fill.png", self.width, self.height)),
                         ImageTk.PhotoImage(self.get_image(
                             "./images/Switch-On-Fill.png", self.width, self.height))
                         ]

        if self.status == 'off':
            # self.switch = self.canvas.create_image(
            #    self.x, self.y, image=self.images[1])
            self.fill = self.canvas.create_image(
                self.x, self.y, image=self.fill_img[0])
            self.knob = self.canvas.create_image(
                self.knob_x[0], self.knob_y, image=self.knob_img[0])
        elif self.status == 'on':
            # self.switch = self.canvas.create_image(
            #    self.x, self.y, image=self.images[0])
            self.fill = self.canvas.create_image(
                self.x, self.y, image=self.fill_img[1])
            self.knob = self.canvas.create_image(
                self.knob_x[1], self.knob_y, image=self.knob_img[1])
        else:
            raise SyntaxError(f"Unknown status: {self.status}")

        self.canvas.tag_bind(self.fill, "<Button-1>", self.__click)
        self.canvas.tag_bind(self.knob, "<Button-1>", self.__click)

    def __click(self, _event):
        if self.status == 'off':
            '''self.canvas.delete(self.switch)
            self.switch = self.canvas.create_image(self.x, self.y, image=self.images[0])'''
            self.canvas.delete(self.fill)
            self.fill = self.canvas.create_image(
                self.x, self.y, image=self.fill_img[1])
            self.canvas.lift(self.knob, self.fill)
            animate.Animation(
                300,
                controller.rebound,
                callback=lambda x: self.canvas.move(self.knob, x*0.6, 0),
                end=None,
                fps=60
            ).start(delay=0)

            if self.command:
                self.command[0]()
            self.status = ON
        elif self.status == 'on':
            '''self.canvas.delete(self.switch)
            self.switch = self.canvas.create_image(
                self.x, self.y, image=self.images[1])'''
            self.canvas.delete(self.fill)
            self.fill = self.canvas.create_image(
                self.x, self.y, image=self.fill_img[0])
            self.canvas.lift(self.knob, self.fill)
            animate.Animation(
                300,
                controller.rebound,
                callback=lambda x: self.canvas.move(self.knob, x*-0.6, 0),
                end=None,
                fps=60
            ).start(delay=0)

            if self.command:
                self.command[1]()
            self.status = OFF

        self.canvas.tag_bind(self.fill, "<Button-1>", self.__click)
        self.canvas.tag_bind(self.knob, "<Button-1>", self.__click)
