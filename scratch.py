from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from numpy import linspace
import numpy as np
import csv
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.title("Fuzzy")
root.geometry("1440x600")


class Set(object):
    def __init__(self, dict):
        self.data = dict

    def __str__(self):
        return str(self.data)


# global variables
veryColdParams = {"name": "veryCold", "function": "Triangle", "a": -5, "b": 0, "c": 7, "d": 0}
coldParams = {"name": "cold", "function": "Triangle", "a": 5, "b": 8, "c": 12, "d": 0}
warmParams = {"name": "warm", "function": "Trapeze", "a": 11, "b": 15, "c": 23, "d": 27}
hotParams = {"name": "hot", "function": "Gaussian", "a": 27, "b": 3, "c": 0, "d": 0}

paramsObjects = [veryColdParams, coldParams, warmParams, hotParams]
setsObjectsMap = map(Set, paramsObjects)
setsObjects = list(setsObjectsMap)
for i in setsObjects:
    print(i)

VeryCold = Set(veryColdParams)
Cold = Set(coldParams)
Warm = Set(warmParams)
Hot = Set(hotParams)

PickedA = IntVar()
PickedB = IntVar()
PickedC = IntVar()
PickedD = IntVar()

clickedSet = StringVar()
clickedSet.set(setsObjects[0].data['name'])

functions = ["Triangle", "Trapeze", "Gaussian"]
clickedFunction = StringVar()
clickedFunction.set(functions[0])
x_values = np.linspace(-5, 40, 100)


# plot functions
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def updatePlots():
    global canvas
    canvas.get_tk_widget().destroy()
    fig = Figure(figsize=(9, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.set_ylim(ymin=0, ymax=1.1)
    plot.set_xlim(xmin=-5, xmax=40)
    plot.set_xlabel("Temperature")
    plot.set_ylabel("Membership")
    plot.set_xticks(linspace(-5, 40), True)


    for i in (setsObjects):
        drawPlot(plot, i.data)

    selectedSets = [setsListbox.get(i) for i in setsListbox.curselection()]
    if len(selectedSets) > 0:
        plot.legend()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=3, rowspan=12)


def drawPlot(figure, fSet):
    selectedSets = [setsListbox.get(i) for i in setsListbox.curselection()]
    if fSet['name'] in selectedSets:
        if fSet['function'] == 'Triangle':
            figure.plot([int(fSet['a']), int(fSet['b']), int(fSet['c'])], [0, 1, 0], label=fSet['name'])
        elif fSet['function'] == 'Trapeze':
            figure.plot([int(fSet['a']), int(fSet['b']), int(fSet['c']), int(fSet['d'])], [0, 1, 1, 0],
                        label=fSet['name'])
        elif fSet['function'] == 'Gaussian' and int(fSet['b']) > 0:
            figure.plot(x_values, gaussian(x_values, int(fSet['a']), int(fSet['b'])), label=fSet['name'])


def export():
    for i in setsObjects:
        print(i.data)

    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(filename + ".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for i in setsObjects:
            wr.writerow(i.data.values())
    messagebox.showinfo("Exported", "Exported sets to file: " + filename)


def importCSV():
    global setsObjects
    global setsNames
    global setsDropdown
    setsObjects = []
    root.filename = filedialog.askopenfilename(initialdir="C:\\Users\Primosz\Documents\repo\fuzzy\Fuzzy",
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    with open(root.filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            setsObjects.append(Set(
                {"name": row[0], "function": row[1], "a": int(row[2]), "b": int(row[3]), "c": int(row[4]),
                 "d": int(row[5])}))
    setsNames = list(map(lambda x: x.data['name'], setsObjects))
    print(setsNames)
    setsListbox.delete(0, 'end')
    for i in list(setsNames):
        print(i)
        setsListbox.insert(END, i)

    setsDropdown['menu'].delete(0, 'end')
    for i in setsNames:
        setsDropdown['menu'].add_command(label=i, command=lambda x=i: pickSet(x))
    updatePlots()
    pickSet(setsObjects[1].data['name'])
    pickFun(functions[0])
    messagebox.showinfo("Import successful", "Imported file: " + root.filename)


# dropDowns functions
def pickSet(value):
    global setsDropdown
    clickedSet.set(value)
    PickedSetText.set(value)

    foundSet = next((x for x in setsObjects if x.data['name'] == value), None)

    clickedFunction.set(foundSet.data['function'])
    slideA.set(foundSet.data['a'])
    slideB.set(foundSet.data['b'])
    slideC.set(foundSet.data['c'])
    slideD.set(foundSet.data['d'])
    updateLegend(foundSet.data['function'])
    updatePlots()


def pickFun(value):
    PickedFunText.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['function'] = value
    if value != 'Gaussian':
        global slideD
        slideD.config(from_=setsObjects[foundSetIndex].data['c'], tickinterval=2)
        slideDfun(setsObjects[foundSetIndex].data['c'])
        slideC.config(from_=setsObjects[foundSetIndex].data['b'], tickinterval=2)
        slideCfun(setsObjects[foundSetIndex].data['b'])
        slideB.config(from_=setsObjects[foundSetIndex].data['a'], tickinterval=2)
        slideBfun(setsObjects[foundSetIndex].data['a'])

    updateLegend(value)
    updatePlots()


def updateLegend(value):
    if value == "Triangle":
        Legend.set(
            "Triangle function:\nParameter a: point where triangle begins\n Parameter b: top of the "
            "triangle\nParameter c: point where triangle ends")
    elif value == "Trapeze":
        Legend.set(
            "Trapeze function:\nParameter a: point where trapeze begins\n Parameter b: left top of the "
            "trapeze\nParameter c: right top of trapeze\nParameter d: point where trapeze ends")
    elif value == "Gaussian":
        Legend.set(
            "Gaussian distribution function:\nParameter a: mean of distribution\n Parameter b: standard deviation ")


# Sliders functions
def slideAfun(value):
    PickedA.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    print(foundSetIndex)
    setsObjects[foundSetIndex].data['a'] = value
    if setsObjects[foundSetIndex].data['function'] != 'Gaussian':
        global slideB
        slideB.config(from_=value, tickinterval=2)

    updatePlots()


def slideBfun(value):
    PickedB.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['b'] = value
    if setsObjects[foundSetIndex].data['function'] != 'Gaussian':
        global slideC
        slideC.config(from_=value, tickinterval=2)

    updatePlots()


def slideCfun(value):
    PickedC.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['c'] = value
    if setsObjects[foundSetIndex].data['function'] == 'Trapeze':
        global slideD
        slideD.config(from_=value, tickinterval=2)

    updatePlots()


def slideDfun(value):
    PickedD.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['d'] = value
    updatePlots()


def addSet():
    global setsObjects
    global setsNames
    global setsDropdown
    if addEntry.get() != '':
        setsObjects.append(Set(
            {"name": addEntry.get(), "function": "Triangle", "a": 0, "b": 0, "c": 0, "d": 0}))
        setsNames = list(map(lambda x: x.data['name'], setsObjects))
        print(setsNames)
        setsListbox.delete(0, 'end')
        for i in list(setsNames):
            print(i)
            setsListbox.insert(END, i)

        setsDropdown['menu'].delete(0, 'end')
        for i in setsNames:
            setsDropdown['menu'].add_command(label=i, command=lambda x=i: pickSet(x))
        updatePlots()


# dropDowns
setsNames = list(map(lambda x: x.data['name'], setsObjects))

setsDropdown = OptionMenu(root, clickedSet, *setsNames, command=pickSet)
setsDropdown.config(width=30)
setsDropdown.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

functionsDropdown = OptionMenu(root, clickedFunction, *functions, command=pickFun)
functionsDropdown.config(width=30)
functionsDropdown.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

setsListbox = Listbox(root, listvariable=setsNames, selectmode=EXTENDED, width=20, height=10)
setsListbox.grid(column=6, row=0, padx=20, pady=20, columnspan=2, rowspan=10)
setsNamesList = list(setsNames)
print(setsNames)
for i in list(setsNames):
    print(i)
    setsListbox.insert(END, i)

btnUpdate = Button(root, command=updatePlots, text="Update")
btnUpdate.grid(row=7, column=6, columnspan=3)

# sliders
slideA = Scale(root, from_=-5, to=40, orient=HORIZONTAL, command=slideAfun)
slideA.config(length=300, tickinterval=5)
slideA.grid(row=3, column=0, padx=20, columnspan=2)

slideB = Scale(root, from_=-5, to=40, orient=HORIZONTAL, command=slideBfun)
slideB.config(length=300, tickinterval=5)
slideB.grid(row=5, column=0, padx=20, columnspan=2)

slideC = Scale(root, from_=-5, to=40, orient=HORIZONTAL, command=slideCfun)
slideC.config(length=300, tickinterval=5)
slideC.grid(row=7, column=0, padx=20, columnspan=2)

slideD = Scale(root, from_=-5, to=40, orient=HORIZONTAL, command=slideDfun)
slideD.config(length=300, tickinterval=5)
slideD.grid(row=9, column=0, padx=20, columnspan=2)

# labels
PickedFunText = StringVar()
pickedFun = Label(root, textvariable=clickedSet)
PickedSetText = StringVar()
pickedSet = Label(root, textvariable=clickedFunction)
pickedSet.grid(row=11, column=0)
pickedFun.grid(row=11, column=1)

paramALabel = Label(root, text="Parameter a")
paramALabel.grid(row=4, column=0, columnspan=2)

paramBLabel = Label(root, text="Parameter b")
paramBLabel.grid(row=6, column=0, columnspan=2)

paramCLabel = Label(root, text="Parameter c")
paramCLabel.grid(row=8, column=0, columnspan=2)

paramDLabel = Label(root, text="Parameter d")
paramDLabel.grid(row=10, column=0, columnspan=2)

pickedA = Label(root, textvariable=PickedA)
pickedB = Label(root, textvariable=str(PickedB))
pickedC = Label(root, textvariable=str(PickedC))
pickedD = Label(root, textvariable=str(PickedD))
pickedA.grid(row=12, column=0)
pickedB.grid(row=12, column=1)
pickedC.grid(row=13, column=0)
pickedD.grid(row=13, column=1)

Legend = StringVar()
legendLabel = Label(root, textvariable=Legend, font=("Helvetica", 12))
legendLabel.grid(row=11, column=3, columnspan=5, rowspan=6)

btnExport = Button(root, command=export, text="Export to .CSV")
btnExport.grid(row=16, column=0)

btnImport = Button(root, command=importCSV, text="Import from .CSV")
btnImport.grid(row=16, column=1)

addEntry = Entry(root)
addEntry.grid(row=2, column=6, columnspan=3)

btnAdd = Button(root, command=addSet, text="Add")
btnAdd.grid(row=2, column=6, columnspan=3, sticky=E)

fig = Figure(figsize=(14, 8), dpi=200)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=5, rowspan=15, columnspan=5)
pickSet(setsObjects[1].data['name'])
pickFun(functions[0])
updatePlots()
root.mainloop()
