import math, time, random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

def parse_line (line: str) -> tuple[float, float, float] | None:
    """takes in a string "1234,512.3,-3.7" (milliseconds, W/m², Pa) and return three numbers or None if malformed"""

    string = line.strip()
    list_serial = string.split(",")

    if len(list_serial) != 3:
        return None
    try: 
        t = float(list_serial[0])
        flux = float(list_serial[1])
        pressure = float(list_serial[2])
    except ValueError:
        return None
    return t, flux, pressure

def fake_serial():
    """popping garbage data per millisecond for testing"""

    t0 = time.time()

    while True:
        ms = int((time.time() - t0) * 1000)
        flux = 100 * math.sin(ms/1000)
        pressure = random.uniform(-50,50)
        yield f"{ms}, {flux:.1f}, {pressure:.1f}\n" 
        time.sleep(0.1)

def read_serial(lines):
    for line in lines:
        serial = parse_line(line)
        print(serial)

def plot_live(lines):
    ts = deque(maxlen = 300)
    fluxes = deque(maxlen = 300)
    pressures = deque(maxlen = 300)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    (l1,) = ax1.plot([], [])
    (l2,) = ax2.plot([], [])
    ax1.set_ylabel("W/m²")
    ax2.set_ylabel("Pa")
   
    def update(_):
        sample = parse_line(next(lines))
        if sample is None:
            return l1, l2
        t, flux, pressure = sample
        ts.append(t)
        fluxes.append(flux)
        pressures.append(pressure)
        l1.set_data(ts, fluxes)
        l2.set_data(ts, pressures)
        ax1.relim()
        ax2.relim()
        ax1.autoscale_view()
        ax2.autoscale_view()
        return l1, l2

    ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    plot_live(fake_serial())
