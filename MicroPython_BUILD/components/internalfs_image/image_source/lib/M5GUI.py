from m5stack import lcd
import uos as os

class M5Widget():
  def __init__(self, x, y, w, h, fgcolor=None, bgcolor=None):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.fgcolor = fgcolor
    self.bgcolor = bgcolor

  def position(self, x=None, y=None):
    if x is None:
      return [self.x, self.y]
    else:
      self.x = x
      self.y = y

  def setSize(self, w=None, h=None):
    if w is None:
      return [self.w, self.h]
    else:
      self.w = w
      self.h = h

  def setColor(self, fgcolor, bgcolor=None):
    self.fgcolor = fgcolor
    if bgcolor:
      self.bgcolor = bgcolor
    self.update()

  def getColor(self):
    return [self.fgcolor, self.bgcolor]

  def draw(self):
    pass

  def clear(self):
      lcd.clear()

  # def fillrect(self):
  #   if self.bgcolor:
  #     lcd.rect(self.x, self.y, self.w, self.h, bgcolor, bgcolor)

  def update(self):
    self.draw()


class M5TextBox(M5Widget):
  def __init__(self, x=lcd.getCursor()[0], y=lcd.getCursor()[1], text=None, font=lcd.FONT_Default, fgcolor=lcd.get_fg(), bgcolor=lcd.get_bg()):
    super().__init__(x, y, 0, 0, fgcolor, bgcolor)
    self.text = ''
    self.font = font
    self.setText(text)

  def getTextWidth(self):
    return lcd.textWidth(self.text)

  def setText(self, text=None):
    if text == None:
      return self.text
    else:
      if not text == self.text:
        # lcd.font(self.font, transparent=True)
        # lcd.font(self.font)
        # lcd.setColor(self.fgcolor, self.bgcolor)
        # lcd.print(text, super().self.x, super().self.y, super().self.bgcolor)
        lcd.textClear(self.x, self.y, self.text, self.bgcolor)
        lcd.print(text, self.x, self.y, self.fgcolor)
        self.text = text

  def setFont(self, font=None):
    if font == None:
      font = lcd.FONT_Default
    self.font = font
    self.update()

  def clear(self):
    lcd.textClear(self.x, self.y, self.text, self.bgcolor)

  def draw(self):
    lcd.textClear(self.x, self.y, self.text, self.bgcolor)
    lcd.font(self.font, transparent=True)
    lcd.textClear(self.x, self.y, self.text, self.bgcolor)
    lcd.print(self.text, self.x, self.y, self.fgcolor)


class M5Listbox(M5TextBox):
  def __init__(self, x , y):
    pass


class M5DialogBox(M5Widget):
  def __init__(self, x , y):
    pass


class M5Button(M5Widget):
  def __init__(self, x=20, y=80, w=50, h=20, color=0x0055dd, bgcolor=lcd.get_bg()):
    super().__init__(x, y, w, h, color, bgcolor)
    self.r=3
    self.isSelected = False
    self.draw()

  def setSelected(self, select):
    if self.isSelected != select:
      self.isSelected = select
    self.update()

  def draw(self):
    if self.isSelected:
      lcd.roundrect(self.x, self.y, self.w, self.h, self.r, lcd.WHITE, lcd.DARKCYAN)
      lcd.roundrect(self.x+1, self.y+1, self.w-2, self.h-2, self.r, lcd.WHITE, lcd.DARKCYAN)
      lcd.roundrect(self.x+2, self.y+2, self.w-4, self.h-4, self.r, lcd.WHITE, lcd.DARKCYAN)
    else:
      lcd.roundrect(self.x, self.y, self.w, self.h, self.r, lcd.WHITE, lcd.CYAN)


class M5Checkbox(M5Widget):
  def __init__(self):
    pass


class M5ProgressBar(M5Widget):
  def __init__(self, x=20, y=180, w=280, h=32, color=0x0055dd, bgcolor=lcd.WHITE, padding=1):
    super().__init__(x, y, w, h, color, bgcolor)
    self.value = 100
    self.offset = padding
    self.miniValue = 0.0
    self.maxValue = 100.0
    self.draw()

  def setRange(self, miniValue, maxValue):
    pass

  def setValue(self, value):
    if value > 100:
      value = 100
    if value < 0:
      value = 0
    if not value == self.value:
      self.value = value
      pgs = int((self.w-self.offset*2) * (self.value / 100))
      print('PGS:%d' % pgs)
      lcd.rect(self.x+self.offset, self.y+self.offset, pgs, self.h-self.offset*2, self.fgcolor, self.fgcolor)
      lcd.rect(self.x+self.offset+pgs+1, self.y+self.offset, (self.w-self.offset*2)-pgs, self.h-self.offset*2, self.bgcolor, self.bgcolor)

  def draw(self):
    lcd.rect(self.x, self.y, self.w, self.h, self.bgcolor, self.bgcolor)
    val = self.value
    self.value = 0
    self.setValue(val)

  def drawPoint(self):
    if self.value == 0.0:
      return
    self.w = value

  def update(self):
    if self.value == value:
      return
    self.value = value
    drawPoint()
