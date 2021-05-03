from machine import Pin, Timer
import explorer_hat as my_hat
import uasyncio as asyncio
from dht_jurassic import DTH
import time
import ring_buffer as buffer

gpio_dht = Pin(2, mode=Pin.OPEN_DRAIN)
d = DTH(gpio_dht,0)
my_display = my_hat.ExplorerHat()

led_builtin = Pin(25, Pin.OUT)

the_temp = 0
the_hum = 0
size = 60
the_temp_list = buffer.CRingBuffer(size)
the_humy_list = buffer.CRingBuffer(size)

key_A = False
key_B = False
key_X = False
key_Y = False
key_A_changed = False
key_B_changed = False
key_X_changed = False
key_Y_changed = False

def init_display():
    if (the_temp < 20):
        my_display.color_pen(0,0,255)
        my_display.clear() #sets the bg
        my_display.color_pen(255,255,255)
    elif (the_temp >= 20 and the_temp < 23):
        my_display.color_pen(0,255,0)
        my_display.clear() #sets the bg
        my_display.color_pen(0,0,0)
    elif (the_temp >= 23):
        my_display.color_pen(255,0,0)
        my_display.clear() #sets the bg
        my_display.color_pen(255,255,255)

def draw_graph(list, factor):
    draw_obj = [0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00]
    for i in range(0,len(list)-1):
        if not list[i] == None:
            my_display.mychar(25 +3*i,200-int(factor*list[i]) -6, draw_obj)

def disp_std_menu():
    my_display.text('Menu [S]',20,10,220,3)
    my_display.text('Temp: {:3.2f}'.format(the_temp),20,60,220,3)
    my_display.text('Hum : {:3.2f}'.format(the_hum),20,110,220,3)

def grid():
    my_display.horiz(30,200,235)
    my_display.vert(30,50,200)
    
    my_display.horiz(25,170,35)
    my_display.horiz(25,140,35)
    my_display.horiz(25,110,35)
    my_display.horiz(25,80,35)
    my_display.horiz(25,50,35)
        
    my_display.vert(70,195,205)
    my_display.vert(110,195,205)
    my_display.vert(150,195,205)
    my_display.vert(190,195,205)
    my_display.vert(230,195,205)
    
def disp_A_menu():
    my_display.color_pen(63,127,255)
    my_display.clear() #sets the bg
    my_display.color_pen(0,0,0)
    my_display.text('Temp [0-50C]',20,10,220,3)
    grid()
    my_display.text('T',10,50,220)
    my_display.text('50 C',40,50,220)
    my_display.text('Time',190,210,2)
    my_temp_list = the_temp_list.get_all()
    draw_graph(my_temp_list, 3)
    
def disp_B_menu():
    my_display.color_pen(255,127,63)
    my_display.clear() #sets the bg
    my_display.color_pen(0,0,0)
    my_display.text('Hum [0-100%]',20,10,220,3)
    grid()
    my_display.text('H',10,50,220)
    my_display.text('100 %',40,50,220)
    my_display.text('Time',190,210,2)
    my_hum_list = the_humy_list.get_all()
    draw_graph(my_hum_list, 1.5)
    
def disp_X_menu():
    my_display.text('Menu [X]',20,10,220,3)
    
def disp_Y_menu():
    my_display.text('Menu [Y]',20,10,220,3)
    

def display_updater():
    init_display()
    if key_A:
        disp_A_menu()
    elif key_B:
        disp_B_menu()
    elif key_X:
        disp_X_menu()
    elif key_Y:
        disp_Y_menu()
    else:
        disp_std_menu()    
    my_display.update()


async def disp_handler(display_trigger_evt):
    while True:
        display_updater()
        await display_trigger_evt.wait()
        display_trigger_evt.clear()
   
async def key_handler(to, display_trigger_evt):
    global key_A
    global key_B
    global key_X
    global key_Y
    global key_A_changed
    global key_B_changed
    global key_X_changed
    global key_Y_changed
    
    def key_upd(key_1, key_1_changed, key_2, key_3, key_4):
        key_1 = not key_1
        key_1_changed = False
        key_2 = False
        key_3 = False
        key_4 = False
       
    while True:
        update_display = False
        if my_display.is_pressed_btn_A():
            key_A_changed = True
        elif key_A_changed:
            key_A = not key_A
            key_A_changed = False
            key_B = False
            key_X = False
            key_Y = False
            update_display = True            
        if my_display.is_pressed_btn_B():
            key_B_changed  = True
        elif key_B_changed:
            key_B = not key_B
            key_B_changed = False
            key_A = False
            key_X = False
            key_Y = False
            update_display = True
        if my_display.is_pressed_btn_X():
            key_X_changed  = True
        elif key_X_changed:
            key_X = not key_X
            key_X_changed = False
            key_A = False
            key_B = False
            key_Y = False
            update_display = True
        if my_display.is_pressed_btn_Y():
            key_Y_changed  = True
        elif key_Y_changed:
            key_Y = not key_Y
            key_Y_changed = False
            key_A = False
            key_B = False
            key_X = False
            update_display = True
        if update_display:
            display_trigger_evt.set()
        await asyncio.sleep_ms(to)
            
def actualize_temp_hum():
    global the_temp
    global the_hum
    global the_temp_list
    global the_humy_list
    result = d.read()
    if result.is_valid():
        the_temp = result.temperature
        the_hum = result.humidity
        the_temp_list.add(the_temp)
        the_humy_list.add(the_hum)

async def temp_hum_handler(to, display_trigger_evt):
    while True:
        actualize_temp_hum()
        display_trigger_evt.set()
        await asyncio.sleep_ms(to)

async def led_handler(device,t_on, t_off):
    while True:
        device.on()
        await asyncio.sleep_ms(t_on)
        device.off()
        await asyncio.sleep_ms(t_off)


async def main():
    tasks = []
    display_trigger_evt = asyncio.Event()
    temp_hum_hdlr = asyncio.create_task(temp_hum_handler(5000, display_trigger_evt)) #measure temp every 5 minutes
    disp_hdlr = asyncio.create_task(disp_handler(display_trigger_evt)) #display is triggered by a change event
    led_hdlr = asyncio.create_task(led_handler(led_builtin,50,2000))
    key_hdlr = asyncio.create_task(key_handler(100, display_trigger_evt))
    tasks.append(temp_hum_hdlr)
    tasks.append(disp_hdlr)
    tasks.append(led_hdlr)
    tasks.append(key_hdlr)
    display_trigger_evt.set()
    res = await asyncio.gather(*tasks, return_exceptions=True)

def init_app():
    init_display()
    actualize_temp_hum()

if __name__ =="__main__":
    init_app()
    asyncio.run(main())

