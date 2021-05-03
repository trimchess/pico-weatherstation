import picoexplorer as hat
import utime

class ExplorerHat:
    def __init__(self):
        self.smiley = [0x00,0x0A,0x00,0x04,0x11,0x0E,0x00,0x00]
        self.sad = [0x00,0x0A,0x00,0x04,0x00,0x0E,0x11,0x00]
        self.heart = [0,0,0,10,31,14,4,0]
        self.b_heart = [0,10,31,0,0,14,4,0]
        self.up_arrow =[0,4,14,21,4,4,0,0]
        self.down_arrow = [0,4,4,21,14,4,0,0]
        self.bits = [128,64,32,16,8,4,2,1]  # Powers of 2
        self.FORWARD = hat.FORWARD
        self.REVERSE = hat.REVERSE
        self.STOP = hat.STOP
        self.MOTOR1 = hat.MOTOR1
        self.MOTOR2 = hat.MOTOR2
        self.width = hat.get_width()
        self.height = hat.get_height()
        self.display_buffer = bytearray(self.width * self.height * 2)
        hat.init(self.display_buffer)
        self.black()
        
        '''HW Definitions    '''
        '''Button pins'''
        self.A = 12
        self.B = 13
        self.X = 14
        self.Y = 15
        '''AD Converters'''
        self.ADC0 = 0
        self.ADC1 = 1
        self.ADC2 = 2
        '''Motor id'''
        self.MOTOR1 = 0
        self.MOTOR2 = 1
        '''Motor control'''
        self.FORWARD = 0
        self.REVERSE = 1
        self.STOP    = 2
        '''GPIO numbering'''
        self.GP0 = 0
        self.GP1 = 1
        self.GP2 = 2
        self.GP3 = 3
        self.GP4 = 4
        self.GP5 = 5
        self.GP6 = 6
        self.GP7 = 7
    
    '''Display set methodes'''
    def black(self):
        '''Sets the display background to black'''
        hat.set_pen(0,0,0)
        hat.clear()
        hat.update()
  
    def white(self):
        '''Sets the display background to white'''
        hat.set_pen(255,255,255)
        hat.clear()
        hat.update()
  
    def color_bg(self,bg_r=0,bg_g=0,bg_b=0):
        '''Sets the display background to (r,b,g)
           r = red (0...255), g = green (0...255), b = blue (0...255)'''
        hat.set_pen(bg_r,bg_g,bg_b)
        hat.clear()
        hat.update()

    def color_pen(self,pen_r=255,pen_g=255,pen_b=255):
        '''Sets the display background to (r,b,g)
           r = red (0...255), g = green (0...255), b = blue (0...255)'''
        hat.set_pen(pen_r,pen_g,pen_b)
        hat.update()

    def color_bg_pen(self,bg_r=0,bg_g=0,bg_b=0,pen_r=255,pen_g=255,pen_b=255):
        '''Sets the display background to (bg_r,bg_b,bg_g)
           and the pen to (pen_r,pen_b,pen_g)
           r = red (0...255), g = green (0...255), b = blue (0...255)'''
        hat.set_pen(bg_r,bg_g,bg_b)
        hat.clear()
        hat.set_pen(pen_r,pen_g,pen_b)
        hat.update()

    def create_pen(self,pen_r=255,pen_g=255,pen_b=255):
        '''create pen and its it reference, r = red (0...255), g = green (0...255), b = blue (0...255)
           default pen is white'''
        return hat.create_pen(pen_r,pen_g,pen_b)

    def set_pen(self,pen):
        '''set a created pen)'''
        hat.set_pen(pen)

    def clear(self):
        '''Clears the display without changing bg and pen''' 
        hat.clear()
        hat.update()

    '''Display show and update methode'''
    def show(self,tt=2):
        '''Updates the display and waits for tt seconds (shows the display)'''
        hat.update()
        utime.sleep(tt)

    def update(self):
        '''Updates the explorer, no wait'''
        hat.update()
        
       
    '''Display Text methodes'''
   
    def text(self,msg,x=20,y=70,z=240,font_size=2):
        '''Displays a text at x,y, z (wrapping), with a font size of font_size '''
        hat.text(msg, x, y, z, font_size)

    def title(self,msg,x=10,y=10,z=240):
        '''Displays a text at x,y, z (wrapping), with a font size of 4 (tile font)'''
        hat.text(msg, x, y, z, 4)
    
    '''Display helper methodes'''
    def align(self,input, max_chars):
        '''Aligns string of n in max_chars'''
        '''see full class documentation for further info'''
        msg1 = str(input)
        space = max_chars - len(msg1)
        msg2 = ""
        for m in range(space):
            msg2 = msg2 +" "
        msg2 = msg2 + msg1
        return msg2  # String - ready for display


    '''Display draw methodes
      - horizontal()
      - vertical()
      - box()
      - line()
      - ring()
      - graph()
    '''
    def horiz(self,l,t,r):    # left, right, top
        '''Draws a horizontal line from point (l,t) to point(r,t)'''
        '''l = left value of position x, r = right value of position x, t = y value'''
        n = r-l+1
        for i in range(n):
            hat.pixel(l + i, t)
   
    def vert(self,l,t,b):   # left, top, bottom
        '''Draws a vertical line from point (l,t) to point(l,b)'''
        '''l = left value of position x, b = bottom value of position x, t = y value'''
        n = b-t+1      # Vertical line
        for i in range(n):
            hat.pixel(l, t+i)
    
    def box(self,l,t,r,b):  # left, top, right, bottom
        '''Draws a box from upper left point (l,t) to lower right point(r,b)'''
        self.horiz(l,t,r)   # Hollow rectangle
        self.horiz(l,b,r)
        self.vert(l,t,b)
        self.vert(r,t,b)
    
    def rect(self,x,y,w,h):
        '''Draws a rectangle from upper left point (x,y) with a width w and a height h'''
        hat.rectangle(x,y,w,h)
        
    def set_clip(self,x,y,w,h):
        '''Set a clip from upper left point (x,y) with a width w and a height h
           A clip defines a part of the screen which can be drawn on,
           and anything outside this area cannot be drawn on.
           ''' 
        hat.set_clip(x,y,w,h)
    
    def remove_clip(self):
        '''Removes a clip'''
        hat.remove_clip()
        
    def line(self,x,y,xx,yy): # (x,y) to (xx,yy)
        '''Draws a line from point(x,y) to point(xy,) to point (xx, yy)'''
        if x > xx:
            t = x  # Swap co-ordinates if necessary
            x = xx
            xx = t
            t = y
            y = yy
            yy = t
        if xx-x == 0:  # Avoid div by zero if vertical
            self.vert(x,min(y,yy),max(y,yy))
        else:          # Draw line one dot at a time L to R
            n=xx-x+1
            grad = float((yy-y)/(xx-x))  # Calculate gradient
            for i in range(n):
                y3 = y + int(grad * i)
                hat.pixel(x+i,y3)  # One dot at a time
                
    def circle(self,x,y,r):
        '''Draws a circle with the center point(x,y) and a radius r'''
        hat.circle(x,y,r)
    
    def ring(self,cx,cy,rr): # Centre and radius
        '''Draws a ring with the center point(x,y) and a radius r, ring thickness of 1'''
        hat.circle(cx,cy,rr)
        hat.set_pen(0,0,0) # background colour
        hat.circle(cx,cy,rr-1)

    def ring(self,cx,cy,rr,r_delta,bg_r,bg_g,bg_b,r_r,r_g,r_b): # Centre and radius
        '''Draws a ring with the center point(x,y) and a radius r, ring thickness of r_delta'''
        
        my_display.color_pen(255,255,255) #pen color white
        my_display.title("Title")
        my_display.circle(120,120,40)
        my_display.color_pen(0,0,0)
        my_display.circle(120,120,39)
        my_display.update()
        
        
        hat.circle(cx,cy,rr)
        hat.set_pen(0,0,0) # background colour
        hat.circle(cx,cy,rr-1)

        
    def ring2(self,cx,cy,r):   # Centre (x,y), radius
        for angle in range(0, 90, 2):  # 0 to 90 degrees in 2s
            y3=int(r*math.sin(math.radians(angle)))
            x3=int(r*math.cos(math.radians(angle)))
            hat.pixel(cx-x3,cy+y3)  # 4 quadrants
            hat.pixel(cx-x3,cy-y3)
            hat.pixel(cx+x3,cy+y3)
            hat.pixel(cx+x3,cy-y3)
    
    def showgraph(self,percentage):   # Bar graph
        '''Shows a bar graph, see class doc for more info'''
        hat.set_pen(255,0,0)
        hat.text("%", 8, 50, 240, 3)
        hat.set_pen(0,0,0)        # Blank old bar graph
        hat.rectangle(29, 50, 220, 16)
        hat.set_pen(200,200,0)    # New  bar graph
        hat.rectangle(29, 50, percentage, 15)
        hat.set_pen(255,255,255)  # Base line zero
        self.vert(28, 46, 68)             
        hat.set_pen(0,0,255)      # percentage
        hat.text(str(self.align(percentage,4)) + " %", 140, 48, 240, 3)

    def mychar(self,xpos, ypos, pattern, size=2):  # Print defined character
        '''Prints a defind character (pattern) at xpos, ypos with the given size'''
        for line in range(8):       # 5x8 characters
            for ii in range(5):     # Low value bits only
                i = ii + 3
                dot = pattern[line] & self.bits[i]  # Extract bit
                if dot:  # Only print WHITE dots
                    if size == 2:
                        hat.pixel(xpos+i*2, ypos+line*2)
                        hat.pixel(xpos+i*2, ypos+line*2+1)
                        hat.pixel(xpos+i*2+1, ypos+line*2)
                        hat.pixel(xpos+i*2+1, ypos+line*2+1)
                    elif size == 3:
                        hat.pixel(xpos+i*3, ypos+line*3)
                        hat.pixel(xpos+i*3, ypos+line*3+1)
                        hat.pixel(xpos+i*3, ypos+line*3+2)
                        hat.pixel(xpos+i*3+1, ypos+line*3)
                        hat.pixel(xpos+i*3+1, ypos+line*3+1)
                        hat.pixel(xpos+i*3+1, ypos+line*3+2)
                        hat.pixel(xpos+i*3+2, ypos+line*3)
                        hat.pixel(xpos+i*3+2, ypos+line*3+1)
                        hat.pixel(xpos+i*3+2, ypos+line*3+2)
                    
    def pixel(self, xpos, ypos, fact=1):
        '''Set a pixel at position x*fact, y*fact'''
        hat.pixel(xpos*fact, ypos*fact)
        
    def pixel_span(self,x,y,l):
        '''Draw a pixel span at position x, y with length l'''
        hat.pixel_span(x,y,l)        
        
    def character(self,char,x,y,font_size=2):
        '''Displays a character at position x,y with a size of font_size'''
        b = bytes(char, 'utf-8')
        hat.character(b[0], x,y,font_size)
        
    def get_width(self):
        '''returns the dysplay width'''
        return(self.width)
    
    def get_height(self):
        '''returns the dysplay height'''
        return(self.height)
    
    def get_dots(self):
        '''returns the amount of displays dots'''
        return(self.height*self.width)

    '''Piezo functions'''
    def set_audio_pin(self, pin=0):
        '''Sets the piezos audio pin'''
        hat.set_audio_pin(pin)
        
    def play_tone(self, frequency):
        '''Plays the tone'''
        hat.set_tone(frequency)
    
    '''Motor functions'''
    def control_motor(self, id, direction, speed=0.0):
        hat.set_motor(id, direction, speed)
    
    '''Button functions'''
    def is_pressed_btn_A(self):
        '''check if button A is pressed'''
        return hat.is_pressed(hat.BUTTON_A)
    
    def is_pressed_btn_B(self):
        '''check if button B is pressed'''
        return hat.is_pressed(hat.BUTTON_B)
    
    def is_pressed_btn_X(self):
        '''check if button X is pressed'''
        return hat.is_pressed(hat.BUTTON_X)
    
    def is_pressed_btn_Y(self):
        '''check if button Y is pressed'''
        return hat.is_pressed(hat.BUTTON_Y)
    
    '''ADC functions'''
    def getADC(self, channel):
        return hat.get_adc(channel)
