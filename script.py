import re
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, patches
from scipy.interpolate import make_interp_spline
import numpy as np

SCRIPT_PATH = "scripts/SCRIPTNAME.html"
GRAPH_SUPTITLE = "TITLE"
GRAPH_TITLE = "Episde Number: EPNUMBER / Original Air Date: AIRDATE"

plt.rcParams["figure.figsize"] = [18.00, 8.00]
plt.rcParams["figure.autolayout"] = True

with open(SCRIPT_PATH) as f:
    lines = [l.strip() for l in f.readlines()]

class Location(object):
    def __init__(self, name, scenes):
        self.name = name
        self.scenes = scenes
        self.order = None

    def set_order(self, order):
        self.order = order

    def __str__(self):
        return "<<%s: %s lines across %s scenes>>" % (self.name, self.total_time(), len(self.scenes))

    def __repr__(self):
        return str(self)

    def total_time(self):
        return sum([s.end-s.start for s in self.scenes])

class Scene(object):
    def __init__(self, location, start, end, characters):
        self.location = location
        self.start = start
        self.end = end
        self.characters = characters

    def __str__(self):
        return "<<Scene %s lines @ %s (%s characters) >>" % (self.end-self.start, self.location, len(self.characters))

    def __repr__(self):
        return str(self)


scenes = []
location = None
characters = set([])
all_characters = set([])
x_indicies = []
start = None

for i, line in enumerate(lines):
    # get scene
    match = re.match("^\[(.*)\]$", line)
    if match:
        if location:
            s = Scene(location, start, i, characters)
            scenes.append(s)
            #x_indicies.append(start)
            #x_indicies.append(i)
            x_indicies.append((start+i)/2.0)
            characters = set([])

        location = match.group(1)
        start = i

    # Get character
    match = re.match("^([A-Z]+): ", line)
    if match:
        char = match.group(1)
        characters.add(char)
        all_characters.add(char)

locations = []
for location_name in set([s.location for s in scenes]):
    my_scenes = [s for s in scenes if s.location == location_name]
    l = Location(location_name, my_scenes)
    locations.append(l)

#locations = sorted(locations, key=lambda l: l.scenes[0].start)
locations = sorted(locations, key=lambda l: l.total_time(), reverse=True)
offset = 5
for i in range(len(locations)):
    locations[i].set_order(i+offset)


fig = plt.figure()
ax = fig.add_subplot(111)

all_scenes = []
for location in locations:
    all_scenes.extend(location.scenes)


all_scenes = sorted(all_scenes, key=lambda s: s.start)

for c, character in enumerate(all_characters):
    y_indicies = []
    count = 0
    for scene in all_scenes:
        order = next(l for l in locations if scene in l.scenes).order
        if character in scene.characters:
            #print("%s is in %s (scene %s" % (character, location, scene))
            count += 1
            y_indicies.append(order+c/10.0)
            #y_indicies.append(order-0.5+c/10.0)
        else:
            #print("%s is NOT in %s" % (character, location))
            #y_indicies.append(c/10.0)
            #y_indicies.append(-c/5.0)
            y_indicies.append(0)

    # At least two appearances
    if count > 1:
        plt.plot(x_indicies, y_indicies, label=character, marker='o')
        #x = x_indicies
        #y = y_indicies
        #X_Y_Spline = make_interp_spline(x, y)
        #X_ = np.linspace(min(x), max(x), 1000)
        #Y_ = X_Y_Spline(X_)
        #plt.plot(X_, Y_, label=character)

# Add locations:
for location in locations:
    order = location.order
    for scene in location.scenes:
        start = scene.start
        end = scene.end
        height = 1
        rectangle = patches.Rectangle((start, order), end-start, height, edgecolor="blue", linewidth=1)
        ax.add_patch(rectangle)
        rx, ry = rectangle.get_xy()
        cx = rx + rectangle.get_width()/2.0
        cy = ry + rectangle.get_height()/2.0
        ax.annotate(location.name, (cx, cy), color='black', fontsize=10, ha='center', va='center')

plt.legend()
plt.suptitle(GRAPH_SUPTITLE)
plt.title(GRAPH_TITLE)
plt.show()


