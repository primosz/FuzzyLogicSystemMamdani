from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from numpy import linspace
import numpy as np
import csv
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
root = Tk()
root.title("Fuzzy")
root.geometry("1440x800")


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
x_values = np.linspace(-5, 40, 150)

input_sets = []
output_sets = []
rules = []
temp1 = 0
temp2 = 0


# plot functions
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def updatePlots():
    global canvas
    canvas.get_tk_widget().destroy()
    fig = Figure(figsize=(9, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.set_ylim(ymin=0, ymax=1.1)
    plot.set_xlim(xmin=-20, xmax=50)
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
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(filename + ".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        selectedSets = [setsListbox.get(i) for i in setsListbox.curselection()]
        for i in setsObjects:
            if(i.data['name'] in selectedSets):
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
    if foundSet.data['function'] == 'Gaussian': slideB.config(from_=0)
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
    else:
        slideB.config(from_=0)

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
        setsListbox.delete(0, 'end')
        for i in list(setsNames):
            setsListbox.insert(END, i)

        setsDropdown['menu'].delete(0, 'end')
        for i in setsNames:
            setsDropdown['menu'].add_command(label=i, command=lambda x=i: pickSet(x))
        updatePlots()


#algorithm functions and classes

class Triangle:
    def __init__(self, name, start, peak, end, none=0):
        self.name = name
        self.a = start
        self.b = peak
        self.c = end

    def __str__(self):
        return ' ' + self.name + str(self.a) + str(self.b) + str(self.c)

    def __call__(self, x):
        if x < self.a or x > self.c:
            return {'set': self.name, 'value': 0}
        elif x == self.b:
            return {'set': self.name, 'value': 1}
        elif x < self.b:
            return {'set': self.name, 'value': (x - self.a) / (self.b - self.a)}
        elif x > self.b:
            return {'set': self.name, 'value': 1 - ((x - self.b) / (self.c - self.b))}


class Trapezoid:
    def __init__(self, name, start, peak_first, peak_second, end):
        self.name = name
        self.a = start
        self.b = peak_first
        self.c = peak_second
        self.d = end

    def __call__(self, x):
        if x < self.a or x > self.d:
            return {'set': self.name, 'value': 0}
        elif self.b <= x <= self.c:
            return {'set': self.name, 'value': 1}
        elif x < self.b:
            return {'set': self.name, 'value': (x - self.a) / (self.b - self.a)}
        elif x > self.c:
            return {'set': self.name, 'value': 1 - ((x - self.c) / (self.d - self.c))}


class Gaussian:
    def __init__(self, name, expected_value, sigma, none_1=0, none_2=0):
        self.name = name
        self.mu = expected_value
        self.sigma = sigma

    def __call__(self, x):
        return {'set': self.name, 'value': np.exp(-np.power(x - self.mu, 2.) / (2 * np.power(self.sigma, 2.)))}


# you can create rules by giving parameters:
# 1 - list of fuzze sets objects
# 2 - list of temperatures in rule
# 3 - what is target temperature (after 'AND')
# 4 - what is the actions (after 'THEN')
class Rule:
    def __init__(self, fuzzySets, currentTable, target, then):
        self.fuzzySets = fuzzySets
        self.currentTable = currentTable
        self.target = target
        self.then = then

    def __call__(self, currentTemp, targetTemp):
        currentTempsMemberships = []
        for fSet in self.currentTable:
            foundSet = next((x for x in self.fuzzySets if x.name == fSet), None)
            currentTempsMemberships.append(foundSet(currentTemp)['value'])

        foundSet = next((x for x in self.fuzzySets if x.name == self.target), None)
        targetMembership = foundSet(targetTemp)['value']

        result = min(max(currentTempsMemberships), targetMembership)
        return {'action': self.then, 'membership': result}

    def __str__(self):
        current_string = ' or '.join(self.currentTable)
        return f"If it's {current_string} and target is {self.target} then {self.then}."


def import_sets_from_csv(filename):
    sets = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp = [x.replace("\"", "") for x in row]
            if tmp[1] == "Triangle":
                sets.append(Triangle(tmp[0], int(tmp[2]), int(tmp[3]), int(tmp[4])))
            elif tmp[1] == "Trapeze":
                sets.append(Trapezoid(tmp[0], int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5])))
            elif tmp[1] == "Gaussian":
                sets.append(Gaussian(tmp[0], int(tmp[2]), int(tmp[3])))
    return sets


def loadRules(filename, fuzzySets):
    rules = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            currentTempslist = list(row[0].split(";"))
            rules.append(Rule(fuzzySets, currentTempslist, row[1], row[2]))
        return rules


def rulesAggregation(rules, outputFuzzySets):
    result = [0] * 200
    for set in outputFuzzySets:
        for i in range(200):
            if set(i)['value'] > 0:
                matches = [x['membership'] for x in rules if x['action'] == set.name and x['membership'] > 0]
                if len(matches) > 0:
                    tmp = set(i)['value']
                    if result[i] < min(max(matches), tmp):
                     result[i] = min(max(matches), tmp)
    return result

#defuzzification methods
def calulcateCentroid(plot):
    n = len(plot)
    x = list(range(n))
    num = 0
    denum = 0
    for i in range(n):
        num += x[i] * plot[i]
        denum += plot[i]
    return {'name': 'Centroid', 'value': num / denum}



def maxMembershipPrinciple(plot):
    n = len(plot)
    maxMem = 0
    x = list(range(n))
    for i in range(n):
        if plot[i] > maxMem:
            maxMem = plot[i]
            result = x[i]
    return {'name': 'Max Membership Principle', 'value': result}



def drawFinalPlot(outputFuzzySets, aggregatedRules, points):

    plt.figure(figsize=(12,6))
    plt.ylim(0, 1)
    for x in outputFuzzySets:
        plt.plot(np.linspace(0, 200, 200), [x(i)['value'] for i in range(0, 200)], '--', label=x.name, linewidth='0.5')

    plt.fill_between(np.linspace(0, 200, 200), aggregatedRules)
    plt.plot(np.linspace(0, 200, 200), aggregatedRules, label="Output membership", fillstyle='full')
    for point in points:
        plt.axvline(x=point['value'], label=f'{point["name"]}: {point["value"]}', color='black')

    plt.ylabel('memberships')
    plt.legend()
    plt.show()


def importInputSets():
    global input_sets
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    input_sets = import_sets_from_csv(root.filename)
    messagebox.showinfo("Import successful", "Imported file: " + root.filename +
                        "\nNumber of imported sets: " + str(len(input_sets)))


def importOutputSets():
    global output_sets
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    output_sets = import_sets_from_csv(root.filename)
    messagebox.showinfo("Import successful", "Imported file: " + root.filename +
                        "\nNumber of imported sets: " + str(len(output_sets)))


def importRulesFromCSV():
    global rules
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    rules = loadRules(root.filename, input_sets)
    messagebox.showinfo("Import successful", "Imported file: " + root.filename +
                        "\nNumber of imported rules: " + str(len(rules)))


def run():
    if currentTemp.get() != '' and targetTemp.get() != "" and len(input_sets) > 0 and len(output_sets) > 0 and len(rules) > 0:
        global temp1, temp2
        temp1 = int(currentTemp.get())
        temp2 = int(targetTemp.get())
        print(temp1, temp2)

        current = [x(temp1) for x in input_sets]
        target = [x(temp2) for x in input_sets]

        print(current)
        print(target)

        evaluatedRules = [x(temp1, temp2) for x in rules]
        for x in evaluatedRules:
            print(x)

        aggregatedRules = rulesAggregation(evaluatedRules, output_sets)
        centroid = calulcateCentroid(aggregatedRules)
        maxMembershipPrincipleResult = maxMembershipPrinciple(aggregatedRules)

        drawFinalPlot(output_sets, aggregatedRules, [centroid, maxMembershipPrincipleResult])
    else:
        messagebox.showerror("Error", "You did not provided valid data!")



def printS():
    for x in input_sets:
       print(x)

    for x in output_sets:
        print(x)

    for x in rules:
        print(x)

# dropDowns
setsNames = list(map(lambda x: x.data['name'], setsObjects))

setsDropdown = OptionMenu(root, clickedSet, *setsNames, command=pickSet)
setsDropdown.config(width=30)
setsDropdown.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

functionsDropdown = OptionMenu(root, clickedFunction, *functions, command=pickFun)
functionsDropdown.config(width=30)
functionsDropdown.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

setsListbox = Listbox(root, listvariable=setsNames, selectmode=MULTIPLE, width=20, height=10)
setsListbox.grid(column=6, row=0, padx=20, pady=20, columnspan=2, rowspan=10)
setsNamesList = list(setsNames)
for i in list(setsNames):
    setsListbox.insert(END, i)

btnUpdate = Button(root, command=updatePlots, text="Update")
btnUpdate.grid(row=7, column=6, columnspan=3)

# sliders
slideA = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slideAfun)
slideA.config(length=300, tickinterval=5)
slideA.grid(row=3, column=0, padx=20, columnspan=2)

slideB = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slideBfun)
slideB.config(length=300, tickinterval=5)
slideB.grid(row=5, column=0, padx=20, columnspan=2)

slideC = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slideCfun)
slideC.config(length=300, tickinterval=5)
slideC.grid(row=7, column=0, padx=20, columnspan=2)

slideD = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slideDfun)
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

#algorithm frame
algorithm_frame = Frame(root,relief='flat', borderwidth=30)
algorithm_frame.grid(row=18, column=0, columnspan=10)
algorithm_frame.config( pady=30, padx=20)

currentTempLabel = Label(algorithm_frame, text="Current Temperature")
currentTempLabel.grid(row=0, column=0, columnspan=2)
currentTemp = Entry(algorithm_frame)
currentTemp.grid(row=1, column=0, columnspan=2)

targetTempLabel = Label(algorithm_frame, text="Target Temperature")
targetTempLabel.grid(row=0, column=2, columnspan=2)
targetTemp = Entry(algorithm_frame)
targetTemp.grid(row=1, column=2, columnspan=2)

btnImportInput = Button(algorithm_frame, command=importInputSets, text="Pick input fuzzy sets file")
btnImportInput.grid(row=1, column=4, padx=5)

btnImportOutput = Button(algorithm_frame, command=importOutputSets, text="Pick output fuzzy sets file")
btnImportOutput.grid(row=1, column=5, padx=5)

btnImportRules = Button(algorithm_frame, command=importRulesFromCSV, text="Pick rules file")
btnImportRules.grid(row=1, column=6, padx=5)

btnRun = Button(algorithm_frame, command=run, text="Run Algorithm", bg='yellow')
btnRun.grid(row=1, column=8, padx=5)

updatePlots()
root.mainloop()
