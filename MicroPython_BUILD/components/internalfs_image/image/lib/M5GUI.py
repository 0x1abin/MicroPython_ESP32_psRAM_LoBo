from m5stack import lcd
import uos as os

class M5Background():
  def __init__(self, bgcolor):
    self.bgcolor = bgcolor
    self.draw()

  def draw():
    lcd.fillREct(0, 0, 320, 240, self.bgcolor)

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

  def CBFunc(self):
    pass

  def draw(self):
    pass

  def clear(self):
    pass

  def update(self):
    self.draw()


class M5TextBox(M5Widget):
  def __init__(self, x=lcd.getCursor()[0], y=lcd.getCursor()[1], text='TextBox', font=lcd.FONT_Default, fgcolor=lcd.get_fg(), bgcolor=lcd.get_bg()):
    super().__init__(x, y, 0, 0, fgcolor, bgcolor)
    self.text = text
    self.font = font
    lcd.font(self.font, transparent=True)
    self.w = lcd.fontSize()[0]
    self.h = lcd.fontSize()[1]
    self.update()

  def getTextWidth(self):
    return lcd.textWidth(self.text)

  def setText(self, text=None):
    if text == None:
      return self.text
    else:
      if not text == self.text:
        lcd.textClear(self.x, self.y, self.text, self.bgcolor)
        self.text = text
        self.update()

  def setFont(self, font=None):
    if font == None:
      font = lcd.FONT_Default
    lcd.textClear(self.x, self.y, self.text, self.bgcolor)
    self.font = font
    self.update()

  def getFont(self):
    return self.font

  def draw(self):
    # lcd.textClear(self.x, self.y, self.text, self.bgcolor)
    lcd.font(self.font, transparent=True)
    lcd.textClear(self.x, self.y, self.text, self.bgcolor)
    lcd.print(self.text, self.x, self.y, self.fgcolor)

  def clear(self):
    lcd.textClear(self.x, self.y, self.text, self.bgcolor)

#can not change the size of box and the font of the content
class M5InputBox(M5Widget):
  def __init__(self, x=lcd.getCursor()[0], y=lcd.getCursor()[1], w=200, h=22, title='Inputbox', text='', fgcolor=lcd.get_fg(), bgcolor=lcd.get_bg()):
    super().__init__(x, y, w, h, fgcolor, bgcolor)
    self.font = lcd.FONT_Default
    lcd.font(lcd.FONT_Default, transparent=True)
    self.title = M5TextBox(x=x,y=y,text=title)
    self.text = M5TextBox(x=x+2,y=y+(lcd.fontSize()[1])+int((h-lcd.fontSize()[1])/2),text=text)
    lcd.drawRect(self.x, self.y+(lcd.fontSize()[1]), self.w, self.h, self.fgcolor)

  def setTitleContent(self, title):
      self.title.setText(title)

  def setTitleColor(self, color):
      self.title.setColor(color)

  def setTextContent(self, text):
      self.text.setText(text)

  def setTextColor(self, color):
      self.text.setColor(color)

  def clear(self):
      lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor)


# class M5Listbox(M5TextBox):
  # def __init__(self, x , y):M5TextBox.__init__(self)
    # pass


# class M5Button(M5TextBox):
#   def __init__(self, x=lcd.getCursor()[0], y=lcd.getCursor()[1], w=80, h=25, text='button', fgcolor=lcd.get_fg(), bgcolor=lcd.get_bg()):
#     super().__init__(x, y, w, h, fgcolor, bgcolor)
#     lcd.font(lcd.FONT_Default, transparent=True)
#     lcd.textWidth(text)
#     self.text=M5TextBox(x=x+int((w-lcd.textWidth(text))/2),y=y+int((h-lcd.fontSize()[1])/2),text=text, bgcolor=lcd.LIGHTGREY)
#     self.isSelected = False
#     self.update()

#   def Selected(self):
#     self.isSelected = True
#     self.update()

#   def Unselected(self):
#     self.isSelected = False
#     self.update()

#   def CBFunc(self, cb_event, cb_event_para=None):
#     if cb_event is None:
#       return
#     return cb_event(cb_event_para)

#   def draw(self):
#     if self.isSelected:
#       lcd.fillRoundRect(self.x, self.y, self.w, self.h, 3, lcd.DARKCYAN)
#       lcd.fillRoundRect(self.x+1, self.y+1, self.w-2, self.h-2, 3, lcd.DARKCYAN)
#       lcd.fillRoundRect(self.x+2, self.y+2, self.w-4, self.h-4, 3, lcd.DARKCYAN)
#       self.text.draw()
#     else:
#       lcd.fillRoundRect(self.x, self.y, self.w, self.h, 3, lcd.LIGHTGREY)
#       self.text.draw()

class M5Title(M5Widget):
  def __init__(self, x=0, y=0, w=320, h=20, fgcolor=0xffffff, bgcolor=0x0000ff, title='Title'):
    super().__init__(x, y, w, h, fgcolor, bgcolor)
    self.title = title
    self.update()

  def show(self):
    self.update()

  def hide(self):
    lcd.fillRect(self.x, self.y, self.w, self.h, lcd.get_bg())
  
  def setTitle(self, title=None):
    if title == None:
      return self.title
    else:
      if not title == self.title:
        lcd.textClear(3, 6, self.title, self.bgcolor)
        self.title = title
        self.update()

  def setFgColor(self, fgcolor=None):
    if fgcolor == None:
      return self.fgcolor
    else:
      if not fgcolor == self.fgcolor:
        lcd.textClear(3, 6, self.title, self.bgcolor)
        self.fgcolor = fgcolor
        lcd.print(self.title, 3, 6, self.fgcolor)

  def setBgColor(self, bgcolor=None):
    if bgcolor == None:
      return self.bgcolor
    else:
      if not bgcolor == self.bgcolor:
        lcd.fillRect(self.x, self.y, self.w, self.h, lcd.get_bg())
        self.bgcolor = bgcolor
        self.update()

  def draw(self):
    lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor)
    lcd.setTextColor(self.fgcolor, self.bgcolor)
    lcd.print(self.title, 3, 6)

class M5ButtonA(M5Widget):
  def __init__(self, x=34, y=216, w=70, h=30, fgcolor=0xffffff, bgcolor=lcd.get_bg(), text='ButtonA', visibility=True):
    super().__init__(x, y, w, h, fgcolor, bgcolor)
    self.text = text
    self.visibility = visibility
    self.update()

  def setText(self, text=None):
    if text == None:
      return self.text
    else:
      if not text == self.text:
        self.text = text
        lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)
        self.update()

  def show(self):
    if not self.visibility == True:
      self.visibility = True
      self.update()
  
  def hide(self):
    if self.visibility == True:
      self.visibility =  False
      lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)

  def draw(self):
    if self.visibility:
      lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)
      lcd.drawRoundRect(self.x, self.y, self.w, self.h, 5, self.fgcolor)
      lcd.setTextColor(self.fgcolor, self.bgcolor)
      lcd.print(self.text, 62 - len(self.text) * 3, 224)

class M5ButtonB(M5Widget):
  def __init__(self, x=126, y=216, w=70, h=30, fgcolor=0xffffff, bgcolor=lcd.get_bg(), text='ButtonB', visibility=True):
    super().__init__(x, y, w, h, fgcolor, bgcolor)
    self.text = text
    self.visibility = visibility
    self.update()

  def setText(self, text=None):
    if text == None:
      return self.text
    else:
      if not text == self.text:
        self.text = text
        lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)
        self.update()

  def show(self):
    if not self.visibility == True:
      self.visibility = True
      self.update()
  
  def hide(self):
    if self.visibility == True:
      self.visibility =  False
      lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)

  def draw(self):
    if self.visibility:
      lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)
      lcd.drawRoundRect(self.x, self.y, self.w, self.h, 5, self.fgcolor)
      lcd.setTextColor(self.fgcolor, self.bgcolor)
      lcd.print(self.text, 154 - len(self.text) * 3, 224)

class M5ButtonC(M5Widget):
  def __init__(self, x=222, y=216, w=70, h=30, fgcolor=0xffffff, bgcolor=lcd.get_bg(), text='ButtonC', visibility=True):
    super().__init__(x, y, w, h, fgcolor, bgcolor)
    self.text = text
    self.visibility = visibility
    self.update()

  def setText(self, text=None):
    if text == None:
      return self.text
    else:
      if not text == self.text:
        self.text = text
        lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)
        self.update()

  def show(self):
    if not self.visibility == True:
      self.visibility = True
      self.update()
  
  def hide(self):
    if self.visibility == True:
      self.visibility =  False
      lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)

  def draw(self):
    if self.visibility:
      lcd.fillRoundRect(self.x, self.y, self.w, self.h, 5, self.bgcolor)
      lcd.drawRoundRect(self.x, self.y, self.w, self.h, 5, self.fgcolor)
      lcd.setTextColor(self.fgcolor, self.bgcolor)
      lcd.print(self.text, 250 - len(self.text) * 3, 224)

class M5Rect(M5Widget):
  def __init__(self, x=0, y=0, w=30, h=30, bordercolor=0xffffff, bgcolor=0xffffff):
    super().__init__(x, y, w, h, bordercolor, bgcolor)
    self.update()

  def setSize(self, width, height):
    if not width == self.w and not height == self.h:
      lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor)
      lcd.drawRect(self.x, self.y, self.w, self.h, self.bordercolor)
      self.w = width
      self.h = height
      self.update()

  def setPosition(self, x, y):
    if not x == self.x and not y == self.y:
      lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor)

class M5CheckBox(M5Widget):
  def __init__(self, x=lcd.getCursor()[0], y=lcd.getCursor()[1], text='Checkbox', fgcolor=lcd.get_fg(), bgcolor=lcd.get_bg()):
    super().__init__(x, y, 22, 22, fgcolor, bgcolor)
    self.font = lcd.FONT_Default
    lcd.font(lcd.FONT_Default, transparent=True)
    self.w = lcd.fontSize()[1]
    self.h = lcd.fontSize()[1]
    self.text = M5TextBox(x=x+self.w+1,y=y,text=text)
    lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor)

  def setText(self, text):
    self.text.setText(text)

  def Checked(self):
    lcd.drawRect(self.x+3, self.y+3, self.w-6, self.h-6, self.fgcolor, self.fgcolor)

  def Unchecked(self):
    lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor)

class M5RadioButton(M5CheckBox):
  def __init__(self):
    pass

class M5ProgressBar(M5Widget):
  def __init__(self, x=lcd.getCursor()[0], y=lcd.getCursor()[1], w=200, h=22, fgcolor=lcd.get_fg(), bgcolor=lcd.get_bg()):
    super().__init__(x, y, w, h, fgcolor, bgcolor)
    self.miniValue = 0
    self.maxValue = 100
    self.isPrintValue = True
    self.value = self.miniValue
    lcd.fillRoundRect(self.x, self.y, self.w, self.h, 2, self.bgcolor)

  def setRange(self, miniValue=None, maxValue=None):
    if miniValue is None:
      if maxValue is None:
        return [self.miniValue, self.maxValue]
      else:
        self.maxValue = maxValue
    else:
      self.miniValue = miniValue
      self.maxValue = maxValue

  def disablePrint(self):
    self.isPrintValue = False
    self.update()

  def setValue(self, value):
    if value < self.miniValue:
      value = self.miniValue
    elif value > self.maxValue:
      value = self.maxValue
    self.value = value

  def getValue(self):
    return self.value

  def drawProgress(self, value):
    # if value <= self.miniValue:
    #   value = self.miniValue
    #   self.setValue(value)
    #   self.clear()
    #   return
    # elif value > self.maxValue:
    #   value = self.maxValue

    # diffPrg = value - self.value
    # diffPrg = int(diffPrg/self.maxValue*self.w)
    # if diffPrg>=0:
    #   x = self.x+int(self.value/self.maxValue*self.w)
    #   lcd.drawRect(x+1, self.y+1, diffPrg-2, self.h-2, lcd.ORANGE, lcd.ORANGE)
    #   print('positive %d', x)
    # else:
    #   x = self.x+int(value/self.maxValue*self.w)
    #   lcd.drawRect(x+1, self.y+1, (-diffPrg)-2, self.h-2, self.bgcolor, self.bgcolor)
    #   print('negative %d', x)
    # self.setValue(value)

    self.setValue(value)
    if self.value == 0:
      self.clear()
      return
    progressWidth = int(self.value/self.maxValue*self.w)
    lcd.drawRect(self.x+2, self.y+1, progressWidth-2, self.h-2, lcd.ORANGE, lcd.ORANGE)
    if self.isPrintValue:
      pgText = str(self.value)
      lcd.font(lcd.FONT_Default, transparent=True)
      tw = lcd.textWidth(pgText)
      th = lcd.fontSize()[1]  # get font height
      # pgTextX = int(self.x+(value-tw)-2)
      pgTextX = int(self.x+(progressWidth-tw)-2)
      if pgTextX < (self.x+6):
        pgTextX = self.x+6
      lcd.print(pgText, pgTextX, int(2+self.y+(self.h+2-th)/2), lcd.BLUE)

  def clear(self):
    lcd.fillRoundRect(self.x, self.y, self.w, self.h, 2, self.bgcolor)

  # def update(self):
  #   if self.value == value:
  #     return
  #   self.value = value
  #   drawPoint()


class M5Image(M5Widget):
  def __init__(self, x=lcd.getCursor()[0] , y=lcd.getCursor()[1], file=None, scale=0):
    self.x = x
    self.y = y
    self.w = 48
    self.h = 48
    self.file = file
    self.scale = scale
    self.update()

  def setScale(self, scale=None):
    if scale is None:
      scale = 0
    self.w = 1/(2**scale)*48
    self.h = 1/(2**scale)*48
    self.scale = scale
    self.update()

  def changeImage(self, file=None):
    if file is None:
      print('no file')
      return
    else:
      self.file = file
    self.update()

  def draw(self):
    lcd.image(self.x, self.y, self.file, self.scale)

  def clear(self):
    lcd.fillRect(self.x, self.y, self.w, self.h, self.bgcolor, self.bgcolor)


