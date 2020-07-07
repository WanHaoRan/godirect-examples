from godirect import GoDirect
import matplotlib.pyplot as plt
import queue
import numpy as np
from matplotlib.animation import FuncAnimation
from gdx import gdx

sample_rate = 10
gdx = gdx.gdx()
gdx.open_usb()
gdx.select_sensors(sensors=gdx.devices[0].list_sensors())
gdx.start(period=1000/sample_rate) # the unit is millisecond 
data = queue.Queue()
 
# for i in range(0,40):
#     measurements = gdx.read()
#     if measurements == None: 
#         break 
#     print(data)
#     data.put(measurements)

# animation script
fig, ax = plt.subplots()
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-')
time = 0

def init():
    ax.set_xlim(0, 20)
    ax.set_ylim(10, 50)
    return ln,

def update(frame):
    measurements = gdx.read()[0]
    time = len(xdata) / sample_rate
    xdata.append(time)
    ydata.append(measurements)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    if time >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    if measurements >= ymax:
        ax.set_ylim(ymin, measurements + 5)
        ax.figure.canvas.draw()
    if measurements <= ymin:
        ax.set_ylim(measurements - 5, ymax)
        ax.figure.canvas.draw()
    ln.set_data(xdata, ydata)

    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 200),
                    init_func=init, blit=True)
plt.show()
gdx.stop()
gdx.close()