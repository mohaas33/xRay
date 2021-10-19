#! /usr/bin/python3

from request_status import request_status
import datetime as dt
import tkinter as tk
import tkinter.font as tkFont

import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import tmp102
#import apds9301
import psutil

###############################################################################
# Parameters and global variables

# Parameters
update_interval = 5000 # Time (ms) between polling/animation updates
max_elements = 1440     # Maximum number of elements to store in plot lists

# Declare global variables
root = None
dfont = None
frame = None
canvas = None
ax1 = None
temp_plot_visible = None


# Global variable to remember various states
fullscreen = False
temp_plot_visible = True
light_plot_visible = True

###############################################################################
# Functions

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)   

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

# Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 15)))
    dfont.configure(size=new_size)

# Toggle the temperature plot
def toggle_temp():

    global canvas
    global ax1
    global temp_plot_visible

    # Toggle plot and axis ticks/label
    temp_plot_visible = not temp_plot_visible
    ax1.collections[0].set_visible(temp_plot_visible)
    ax1.get_yaxis().set_visible(temp_plot_visible)
    canvas.draw()

# Toggle the light plot
def toggle_light():

    global canvas
    global ax2
    global light_plot_visible

    # Toggle plot and axis ticks/label
    light_plot_visible = not light_plot_visible
    ax2.get_lines()[0].set_visible(light_plot_visible)
    ax2.get_yaxis().set_visible(light_plot_visible)
    canvas.draw()

# This function is called periodically from FuncAnimation
def animate(i, ax1, ax2, xs, temps, lights, temp_c, temp_c_hv):

    # Update data to display temperature and light values
    try:
        t_Control_Board , V_Supply_Monitor , kV , mA , filament_I , filament_V , t_High_Voltage_Board = request_status()
        cb_temp = round(t_Control_Board, 2)
        hv_temp = round(t_High_Voltage_Board, 2)
        v_sm = round(V_Supply_Monitor, 2)
        sp_kv = round(kV, 2)
        sp_i = round(mA, 2)
        f_i = round(filament_I, 2)
        f_v = round(filament_V, 2)
    except:
        pass

    # Update our labels
    temp_c.set(cb_temp)
    temp_c_hv.set(hv_temp)
    volt_sm.set(v_sm)  
    volt_sp_kv.set(sp_kv) 
    curr_sp_i.set(sp_i)
    curr_f_i.set(f_i) 
    volt_f_v.set(f_v) 

    # Append timestamp to x-axis list
    timestamp = mdates.date2num(dt.datetime.now())
    xs.append(timestamp)

    # Append sensor data to lists for plotting
    temps.append(cb_temp)
    lights.append(hv_temp)

    # Limit lists to a set number of elements
    xs = xs[-max_elements:]
    temps = temps[-max_elements:]
    lights = lights[-max_elements:]

    # Clear, format, and plot light values first (behind)
    color = 'tab:red'
    ax1.clear()
    ax1.set_ylabel('Temperature (C)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.fill_between(xs, temps, 0, linewidth=2, color=color, alpha=0.3)

    # Clear, format, and plot temperature values (in front)
    color = 'tab:blue'
    ax2.clear()
    ax2.set_ylabel('Temperature (C)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(xs, lights, linewidth=2, color=color)

    # Format timestamps to be more readable
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()

    # Make sure plots stay visible or invisible as desired
    ax1.collections[0].set_visible(temp_plot_visible)
    ax2.get_lines()[0].set_visible(light_plot_visible)

# Dummy function prevents segfault
def _destroy(event):
    pass

###############################################################################
# Main script

# Create the main window
root = tk.Tk()
root.title("xRay Monitor")

# Create the main container
frame = tk.Frame(root)
frame.configure(bg='white')

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Create figure for plotting
fig = figure.Figure(figsize=(2, 2))
fig.subplots_adjust(left=0.1, right=0.8)
ax1 = fig.add_subplot(1, 1, 1)

# Instantiate a new set of axes that shares the same x-axis
ax2 = ax1.twinx()

# Empty x and y lists for storing data to plot later
xs = []
temps = []
lights = []

# Variables for holding temperature and light data
temp_c = tk.DoubleVar()
temp_c_hv = tk.DoubleVar()
volt_sm = tk.DoubleVar()
volt_sp_kv = tk.DoubleVar()
curr_sp_i = tk.DoubleVar()
curr_f_i = tk.DoubleVar()
volt_f_v = tk.DoubleVar()


# Create dynamic font for text
dfont = tkFont.Font(size=-12)

# Create a Tk Canvas widget out of our figure
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_plot = canvas.get_tk_widget()

degree_sign = u"\N{DEGREE SIGN}"

# Create other supporting widgets
label_temp = tk.Label(frame, text='Temperature:', font=dfont, bg='white')
label_celsius = tk.Label(frame, textvariable=temp_c, font=dfont, bg='white')
label_unitc = tk.Label(frame, text=degree_sign+"C", font=dfont, bg='white')

label_temp_hv = tk.Label(frame, text="HV Temperature:", font=dfont, bg='white')
label_temp_c_hv = tk.Label(frame, textvariable=temp_c_hv, font=dfont, bg='white')
label_unitc_hv = tk.Label(frame, text=degree_sign+"C", font=dfont, bg='white')

#volt_sm    
label_low_volt = tk.Label(frame, text="Low Voltage Supply Monitor:", font=dfont, bg='white')
label_volt_sm = tk.Label(frame, textvariable=volt_sm, font=dfont, bg='white')
label_unit_v = tk.Label(frame, text="V", font=dfont, bg='white')

#volt_sp_kv 
label_k_volt = tk.Label(frame, text="kV Feedback:", font=dfont, bg='white')
label_volt_sp_kv = tk.Label(frame, textvariable=volt_sp_kv, font=dfont, bg='white')
label_unit_kv = tk.Label(frame, text="kV", font=dfont, bg='white')

#curr_sp_i  
label_mA = tk.Label(frame, text="mA Feedback:", font=dfont, bg='white')
label_curr_sp_i = tk.Label(frame, textvariable=curr_sp_i, font=dfont, bg='white')
label_unit_mA = tk.Label(frame, text="mA", font=dfont, bg='white')

#curr_f_i   
label_A = tk.Label(frame, text="Filament Current:", font=dfont, bg='white')
label_curr_f_i = tk.Label(frame, textvariable=curr_f_i, font=dfont, bg='white')
label_unit_A = tk.Label(frame, text="A", font=dfont, bg='white')

#volt_f_v   
label_A = tk.Label(frame, text="Filament Voltage:", font=dfont, bg='white')
label_curr_f_i = tk.Label(frame, textvariable=volt_f_v, font=dfont, bg='white')
label_unit_V = tk.Label(frame, text="V", font=dfont, bg='white')


button_temp = tk.Button(    frame, 
                            text="Toggle Temperature", 
                            font=dfont,
                            command=toggle_temp)
button_light = tk.Button(   frame,
                            text="Toggle HV Temperature",
                            font=dfont,
                            command=toggle_light)
button_quit = tk.Button(    frame,
                            text="Quit",
                            font=dfont,
                            command=root.destroy)

# Lay out widgets in a grid in the frame
canvas_plot.grid(   row=0, 
                    column=0, 
                    rowspan=14, 
                    columnspan=4, 
                    sticky=tk.W+tk.E+tk.N+tk.S)

N=0
label_temp   .grid(row=N  , column=4, columnspan=2)
label_celsius.grid(row=N+1, column=4, sticky=tk.E)
label_unitc  .grid(row=N+1, column=5, sticky=tk.W)

N+=2
label_temp_hv.grid  (row=N  , column=4, columnspan=2)
label_temp_c_hv.grid(row=N+1, column=4, sticky=tk.E)
label_unitc_hv.grid (row=N+1, column=5, sticky=tk.W)


#volt_sm    
N+=2
label_low_volt .grid(row=N  , column=4, columnspan=2)
label_volt_sm  .grid(row=N+1, column=4, sticky=tk.E)
label_unit_v   .grid(row=N+1, column=5, sticky=tk.W)

#volt_sp_kv 
N+=2
label_k_volt     .grid(row=N  , column=4, columnspan=2)
label_volt_sp_kv .grid(row=N+1, column=4, sticky=tk.E)
label_unit_kv    .grid(row=N+1, column=5, sticky=tk.W)

#curr_sp_i  
N+=2
label_mA        .grid(row=N  , column=4, columnspan=2)
label_curr_sp_i .grid(row=N+1, column=4, sticky=tk.E)
label_unit_mA   .grid(row=N+1, column=5, sticky=tk.W)

#curr_f_i   
N+=2
label_A        .grid(row=N  , column=4, columnspan=2)
label_curr_f_i .grid(row=N+1, column=4, sticky=tk.E)
label_unit_A   .grid(row=N+1, column=5, sticky=tk.W)

#volt_f_v   
N+=2
label_A        .grid(row=N  , column=4, columnspan=2)
label_curr_f_i .grid(row=N+1, column=4, sticky=tk.E)
label_unit_V   .grid(row=N+1, column=5, sticky=tk.W)

N+=2
button_temp    .grid(row=N  , column=0, columnspan=2)
button_light   .grid(row=N+1, column=2, columnspan=2)
button_quit    .grid(row=N+1, column=4, columnspan=2)

# Add a standard 5 pixel padding to all widgets
for w in frame.winfo_children():
    w.grid(padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 14):
    frame.rowconfigure(i, weight=1)
for i in range(0, 14):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Call empty _destroy function on exit to prevent segmentation fault
root.bind("<Destroy>", _destroy)

# Initialize our sensors
#tmp102.init()
#apds9301.init()

# Call animate() function periodically
fargs = (ax1, ax2, xs, temps, lights, temp_c, temp_c_hv)
ani = animation.FuncAnimation(  fig, 
                                animate, 
                                fargs=fargs, 
                                interval=update_interval)               

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()