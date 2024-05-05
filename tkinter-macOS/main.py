import tkinter as tk
from PIL import Image, ImageTk
from math import floor


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
        self.error = self.get_image("./error.png", 64, 64)
        self.warning = self.get_image("./warning.png", 64, 64)

    def get_image(self, filename, width, height):  # type: (str, int, int) -> Image
        return Image.open(filename).resize((width, height))


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
            self.get_image("./BigButton.png", width, height))
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
        self.config(bg="SystemTransparent")
        self.attributes("-transparent", True)

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

            self.bind("<ButtonPress-1>", self.start_drag)
            self.bind("<ButtonRelease-1>", self.stop_drag)
            self.bind("<B1-Motion>", self.on_drag)
        else:
            print('Drag disabled')

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def stop_drag(self, _event):
        self.offset_x = 0
        self.offset_y = 0

    def on_drag(self, _event):
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
            "./NormalButton-normal.png", self.width, self.height))
        self.bg_primary = ImageTk.PhotoImage(self.get_image(
            "./NormalButton-primary.png", self.width, self.height))
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

        self.images = [ImageTk.PhotoImage(self.get_image("./not-check.png", 16, 16)),
                       ImageTk.PhotoImage(self.get_image("./checked.png", 16, 16))]

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

        self.images = [ImageTk.PhotoImage(self.get_image("./not-radio.png", 16, 16)),
                       ImageTk.PhotoImage(self.get_image("./radioed.png", 16, 16))]

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
            self.command(_event)
            self.canvas.tag_bind(self.image, "<Button-1>", self.click)
            self.click_status = True
