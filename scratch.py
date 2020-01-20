import csv
import os
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from numpy import linspace

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


def update_plots():
    global canvas
    canvas.get_tk_widget().destroy()
    fig = Figure(figsize=(9, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.set_ylim(ymin=0, ymax=1.1)
    plot.set_xlim(xmin=-20, xmax=50)
    plot.set_xlabel("Temperature")
    plot.set_ylabel("Membership")
    plot.set_xticks(linspace(-5, 40), True)

    for i in setsObjects:
        draw_plot(plot, i.data)

    selected_sets = [setsListbox.get(i) for i in setsListbox.curselection()]
    if len(selected_sets) > 0:
        plot.legend()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=3, rowspan=12)


def draw_plot(figure, f_set):
    selected_sets = [setsListbox.get(i) for i in setsListbox.curselection()]
    if f_set['name'] in selected_sets:
        if f_set['function'] == 'Triangle':
            figure.plot([int(f_set['a']), int(f_set['b']), int(f_set['c'])], [0, 1, 0], label=f_set['name'])
        elif f_set['function'] == 'Trapeze':
            figure.plot([int(f_set['a']), int(f_set['b']), int(f_set['c']), int(f_set['d'])], [0, 1, 1, 0],
                        label=f_set['name'])
        elif f_set['function'] == 'Gaussian' and int(f_set['b']) > 0:
            figure.plot(x_values, gaussian(x_values, int(f_set['a']), int(f_set['b'])), label=f_set['name'])


def export():
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(filename + ".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        selected_sets = [setsListbox.get(i) for i in setsListbox.curselection()]
        for i in setsObjects:
            if i.data['name'] in selected_sets:
                wr.writerow(i.data.values())
    messagebox.showinfo("Exported", "Exported sets to file: " + filename)


def import_csv():
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
        setsDropdown['menu'].add_command(label=i, command=lambda x=i: pick_set(x))
    update_plots()
    pick_set(setsObjects[1].data['name'])
    pick_fun(functions[0])
    messagebox.showinfo("Import successful", "Imported file: " + root.filename)


# dropDowns functions
def pick_set(value):
    global setsDropdown
    clickedSet.set(value)
    PickedSetText.set(value)

    foundSet = next((x for x in setsObjects if x.data['name'] == value), None)

    clickedFunction.set(foundSet.data['function'])
    slideA.set(foundSet.data['a'])
    slideB.set(foundSet.data['b'])
    slideC.set(foundSet.data['c'])
    slideD.set(foundSet.data['d'])
    update_legend(foundSet.data['function'])
    if foundSet.data['function'] == 'Gaussian': slideB.config(from_=0)
    update_plots()


def pick_fun(value):
    PickedFunText.set(value)
    found_set_index = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[found_set_index].data['function'] = value
    if value != 'Gaussian':
        global slideD
        slideD.config(from_=setsObjects[found_set_index].data['c'], tickinterval=2)
        slide_d_fun(setsObjects[found_set_index].data['c'])
        slideC.config(from_=setsObjects[found_set_index].data['b'], tickinterval=2)
        slide_c_fun(setsObjects[found_set_index].data['b'])
        slideB.config(from_=setsObjects[found_set_index].data['a'], tickinterval=2)
        slide_b_fun(setsObjects[found_set_index].data['a'])
    else:
        slideB.config(from_=0)

    update_legend(value)
    update_plots()


def update_legend(value):
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
def slide_a_fun(value):
    PickedA.set(value)
    found_set_index = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[found_set_index].data['a'] = value
    if setsObjects[found_set_index].data['function'] != 'Gaussian':
        global slideB
        slideB.config(from_=value, tickinterval=2)

    update_plots()


def slide_b_fun(value):
    PickedB.set(value)
    found_set_index = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[found_set_index].data['b'] = value
    if setsObjects[found_set_index].data['function'] != 'Gaussian':
        global slideC
        slideC.config(from_=value, tickinterval=2)

    update_plots()


def slide_c_fun(value):
    PickedC.set(value)
    found_set_index = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[found_set_index].data['c'] = value
    if setsObjects[found_set_index].data['function'] == 'Trapeze':
        global slideD
        slideD.config(from_=value, tickinterval=2)

    update_plots()


def slide_d_fun(value):
    PickedD.set(value)
    found_set_index = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[found_set_index].data['d'] = value
    update_plots()


def add_set():
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
            setsDropdown['menu'].add_command(label=i, command=lambda x=i: pick_set(x))
        update_plots()


# algorithm functions and classes

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
    def __init__(self, fuzzy_sets, current_table, target, then):
        self.fuzzySets = fuzzy_sets
        self.currentTable = current_table
        self.target = target
        self.then = then

    def __call__(self, current_temp, target_temp):
        current_temps_memberships = []
        for fSet in self.currentTable:
            found_set = next((x for x in self.fuzzySets if x.name == fSet), None)
            current_temps_memberships.append(found_set(current_temp)['value'])

        found_set = next((x for x in self.fuzzySets if x.name == self.target), None)
        target_membership = found_set(target_temp)['value']

        result = min(max(current_temps_memberships), target_membership)
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


def load_rules(filename, fuzzy_sets):
    rules = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            current_tempslist = list(row[0].split(";"))
            rules.append(Rule(fuzzy_sets, current_tempslist, row[1], row[2]))
        return rules


def rules_aggregation(rules, output_fuzzy_sets):
    result = [0] * 200
    for out_set in output_fuzzy_sets:
        for i in range(200):
            if out_set(i)['value'] > 0:
                matches = [x['membership'] for x in rules if x['action'] == out_set.name and x['membership'] > 0]
                if len(matches) > 0:
                    tmp = out_set(i)['value']
                    if result[i] < min(max(matches), tmp):
                        result[i] = min(max(matches), tmp)
    return result


# defuzzification methods
def calulcate_centroid(plot):
    n = len(plot)
    x = list(range(n))
    num = 0
    denum = 0
    for i in range(n):
        num += x[i] * plot[i]
        denum += plot[i]
    return {'name': 'Centroid', 'value': num / denum}


def max_membership_principle(plot):
    n = len(plot)
    max_mem = 0
    x = list(range(n))
    result = 0
    for i in range(n):
        if plot[i] > max_mem:
            max_mem = plot[i]
            result = x[i]
    return {'name': 'Max Membership Principle', 'value': result}


def draw_final_plot(output_fuzzy_sets, aggregated_rules, points):
    plt.figure(figsize=(12, 6))
    plt.ylim(0, 1)
    for x in output_fuzzy_sets:
        plt.plot(np.linspace(0, 200, 200), [x(i)['value'] for i in range(0, 200)], '--', label=x.name, linewidth='0.5')

    plt.fill_between(np.linspace(0, 200, 200), aggregated_rules)
    plt.plot(np.linspace(0, 200, 200), aggregated_rules, label="Output membership", fillstyle='full')
    for point in points:
        plt.axvline(x=point['value'], label=f'{point["name"]}: {point["value"]}', color='black')

    plt.ylabel('memberships')
    plt.legend()
    plt.show()


def import_input_sets():
    global input_sets
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    input_sets = import_sets_from_csv(root.filename)
    messagebox.showinfo("Import successful", "Imported file: " + root.filename +
                        "\nNumber of imported sets: " + str(len(input_sets)))


def import_output_sets():
    global output_sets
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    output_sets = import_sets_from_csv(root.filename)
    messagebox.showinfo("Import successful", "Imported file: " + root.filename +
                        "\nNumber of imported sets: " + str(len(output_sets)))


def import_rules_from_csv():
    global rules
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select .CSV file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    rules = load_rules(root.filename, input_sets)
    messagebox.showinfo("Import successful", "Imported file: " + root.filename +
                        "\nNumber of imported rules: " + str(len(rules)))


def run():
    if currentTemp.get() != '' and targetTemp.get() != "" and len(input_sets) > 0 and len(output_sets) > 0 and len(
            rules) > 0:
        global temp1, temp2
        temp1 = int(currentTemp.get())
        temp2 = int(targetTemp.get())
        print(temp1, temp2)

        current = [x(temp1) for x in input_sets]
        target = [x(temp2) for x in input_sets]

        print(current)
        print(target)

        evaluated_rules = [x(temp1, temp2) for x in rules]
        for x in evaluated_rules:
            print(x)

        aggregated_rules = rules_aggregation(evaluated_rules, output_sets)
        centroid = calulcate_centroid(aggregated_rules)
        max_membership_principle_result = max_membership_principle(aggregated_rules)

        draw_final_plot(output_sets, aggregated_rules, [centroid, max_membership_principle_result])
    else:
        messagebox.showerror("Error", "You did not provided valid data!")


def print_s():
    for x in input_sets:
        print(x)

    for x in output_sets:
        print(x)

    for x in rules:
        print(x)


# dropDowns
setsNames = list(map(lambda x: x.data['name'], setsObjects))

setsDropdown = OptionMenu(root, clickedSet, *setsNames, command=pick_set)
setsDropdown.config(width=30)
setsDropdown.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

functionsDropdown = OptionMenu(root, clickedFunction, *functions, command=pick_fun)
functionsDropdown.config(width=30)
functionsDropdown.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

setsListbox = Listbox(root, listvariable=setsNames, selectmode=MULTIPLE, width=20, height=10)
setsListbox.grid(column=6, row=0, padx=20, pady=20, columnspan=2, rowspan=10)
setsNamesList = list(setsNames)
for i in list(setsNames):
    setsListbox.insert(END, i)

btnUpdate = Button(root, command=update_plots, text="Update")
btnUpdate.grid(row=7, column=6, columnspan=3)

# sliders
slideA = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slide_a_fun)
slideA.config(length=300, tickinterval=5)
slideA.grid(row=3, column=0, padx=20, columnspan=2)

slideB = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slide_b_fun)
slideB.config(length=300, tickinterval=5)
slideB.grid(row=5, column=0, padx=20, columnspan=2)

slideC = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slide_c_fun)
slideC.config(length=300, tickinterval=5)
slideC.grid(row=7, column=0, padx=20, columnspan=2)

slideD = Scale(root, from_=-20, to=50, orient=HORIZONTAL, command=slide_d_fun)
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

btnImport = Button(root, command=import_csv, text="Import from .CSV")
btnImport.grid(row=16, column=1)

addEntry = Entry(root)
addEntry.grid(row=2, column=6, columnspan=3)

btnAdd = Button(root, command=add_set, text="Add")
btnAdd.grid(row=2, column=6, columnspan=3, sticky=E)

fig = Figure(figsize=(14, 8), dpi=200)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=5, rowspan=15, columnspan=5)
pick_set(setsObjects[1].data['name'])
pick_fun(functions[0])

# algorithm frame
algorithm_frame = Frame(root, relief='flat', borderwidth=30)
algorithm_frame.grid(row=18, column=0, columnspan=10)
algorithm_frame.config(pady=30, padx=20)

currentTempLabel = Label(algorithm_frame, text="Current Temperature")
currentTempLabel.grid(row=0, column=0, columnspan=2)
currentTemp = Entry(algorithm_frame)
currentTemp.grid(row=1, column=0, columnspan=2)

targetTempLabel = Label(algorithm_frame, text="Target Temperature")
targetTempLabel.grid(row=0, column=2, columnspan=2)
targetTemp = Entry(algorithm_frame)
targetTemp.grid(row=1, column=2, columnspan=2)

btnImportInput = Button(algorithm_frame, command=import_input_sets, text="Pick input fuzzy sets file")
btnImportInput.grid(row=1, column=4, padx=5)

btnImportOutput = Button(algorithm_frame, command=import_output_sets, text="Pick output fuzzy sets file")
btnImportOutput.grid(row=1, column=5, padx=5)

btnImportRules = Button(algorithm_frame, command=import_rules_from_csv, text="Pick rules file")
btnImportRules.grid(row=1, column=6, padx=5)

btnRun = Button(algorithm_frame, command=run, text="Run Algorithm", bg='yellow')
btnRun.grid(row=1, column=8, padx=5)

update_plots()
root.mainloop()
