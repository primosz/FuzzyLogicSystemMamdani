from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from numpy import linspace
import numpy as np
import csv
from datetime import datetime
from tkinter import messagebox

root= Tk()
root.title("Fuzzy")
root.geometry("1440x600")

class Set(object):
    def __init__(self, dict):
        self.data = dict

    def __str__(self):
        return str(self.data)


#global variables
veryColdParams = { "name": "veryCold", "function" : "Triangle", "a" : -5, "b" : 0, "c" : 7, "d" : 0}
coldParams = { "name": "cold", "function" : "Triangle", "a" : 5, "b" : 8, "c" : 12, "d" : 0}
warmParams = { "name": "warm", "function" : "Trapeze", "a" : 11, "b" : 15, "c" : 23, "d" : 27}
hotParams = { "name": "hot", "function" : "Gaussian", "a" : 27, "b" : 3, "c" : 0, "d" : 0}

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

#sets = ["Very cold", "Cold", "Warm", "Hot"]
clickedSet = StringVar()
clickedSet.set(setsObjects[0].data['name'])

functions = ["Triangle", "Trapeze", "Gaussian"]
clickedFunction = StringVar()
clickedFunction.set(functions[0])
x_values = np.linspace(-5, 40, 100)

#plot functions
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def updatePlots():
    global canvas
    canvas.get_tk_widget().destroy()
    fig= Figure(figsize=(9, 4), dpi=100)
    plot = fig.add_subplot(111)
   # plot.plot(linspace(0,40), [0] * 50, 'black')
    plot.set_ylim(ymin=0, ymax=1.1)
    plot.set_xlim(xmin=-5, xmax=40)
    plot.set_xlabel("Temperature")
    plot.set_ylabel("Membership")
    plot.set_xticks(linspace(-5,40), True)


    for i in (setsObjects):
        drawPlot(plot, i.data)
   # drawPlot(plot, set1)
  #  drawPlot(plot, set2)
   # drawPlot(plot, set3)
   # drawPlot(plot, set4)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=3, rowspan=12)

def drawPlot(figure, fSet):
    selectedSets = [setsListbox.get(i) for i in setsListbox.curselection()]
    print(selectedSets)
    if fSet['name'] in selectedSets:
         if fSet['function']=='Triangle': figure.plot([int(fSet['a']), int(fSet['b']), int(fSet['c'])], [0, 1, 0], label=fSet['name'])
         elif fSet['function']=='Trapeze': figure.plot( [int(fSet['a']), int(fSet['b']), int(fSet['c']), int(fSet['d'])], [0, 1, 1, 0], label=fSet['name'])
         elif fSet['function']=='Gaussian' and  int(fSet['b'])>0:  figure.plot(x_values, gaussian(x_values, int(fSet['a']), int(fSet['b'])), label=fSet['name'])
    figure.legend()

def export():
    for i in setsObjects:
        print(i.data)

    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(filename+".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for i in setsObjects:
            wr.writerow(i.data.values())
    messagebox.showinfo("Exported", "Exported sets to file: "+ filename)



#dropDowns functions
def pickSet(value):
    PickedSetText.set(value)

    foundSet = next((x for x in setsObjects if x.data['name']==value), None)

    clickedFunction.set(foundSet.data['function'])
    slideA.set(foundSet.data['a'])
    slideB.set(foundSet.data['b'])
    slideC.set(foundSet.data['c'])
    slideD.set(foundSet.data['d'])
    updateLegend(foundSet.data['function'])

    '''

    if PickedSetText.get()==sets[0]:
        clickedFunction.set(VeryCold.data['function'])
        slideA.set(VeryCold.data['a'])
        slideB.set(VeryCold.data['b'])
        slideC.set(VeryCold.data['c'])
        slideD.set(VeryCold.data['d'])
        updateLegend(VeryCold.data['function'])

    elif PickedSetText.get()==sets[1]:
        clickedFunction.set(Cold.data['function'])
        slideA.set(Cold.data['a'])
        slideB.set(Cold.data['b'])
        slideC.set(Cold.data['c'])
        slideD.set(Cold.data['d'])
        updateLegend(Cold.data['function'])

    elif PickedSetText.get()==sets[2]:
        clickedFunction.set(Warm.data['function'])
        slideA.set(Warm.data['a'])
        slideB.set(Warm.data['b'])
        slideC.set(Warm.data['c'])
        slideD.set(Warm.data['d'])
        updateLegend(Warm.data['function'])

    elif PickedSetText.get()==sets[3]:
        clickedFunction.set(Hot.data['function'])
        slideA.set(Hot.data['a'])
        slideB.set(Hot.data['b'])
        slideC.set(Hot.data['c'])
        slideD.set(Hot.data['d'])
        updateLegend(Hot.data['function'])
        '''

    updatePlots()

def pickFun(value):
    PickedFunText.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if  x.data['name']==PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['function']=value
    '''
    if PickedSetText.get()==sets[0]: VeryCold.data['function'] = value
    elif PickedSetText.get()==sets[1]: Cold.data['function'] = value
    elif PickedSetText.get()==sets[2]: Warm.data['function'] = value
    elif PickedSetText.get()==sets[3]: Hot.data['function'] = value
    '''

    updateLegend(value)
    updatePlots()

def updateLegend(value):

    if value=="Triangle": Legend.set("Triangle function:\nParameter a: point where triangle begins\n Parameter b: top of the triangle\nParameter c: point where triangle ends")
    elif value=="Trapeze": Legend.set("Trapeze function:\nParameter a: point where trapeze begins\n Parameter b: left top of the trapeze\nParameter c: right top of trapeze\nParameter d: point where trapeze ends")
    elif value=="Gaussian": Legend.set("Gaussian distribution function:\nParameter a: mean of distribution\n Parameter b: standard deviation ")



#Sliders functions
def slideA(value):
    PickedA.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    print("index")
    print(foundSetIndex)
    setsObjects[foundSetIndex].data['a']=value
    '''
    if PickedSetText.get()==sets[0]: VeryCold.data['a'] = value
    elif PickedSetText.get()==sets[1]: Cold.data['a'] = value
    elif PickedSetText.get()==sets[2]: Warm.data['a'] = value
    elif PickedSetText.get()==sets[3]: Hot.data['a'] = value
    '''
    updatePlots()

def slideB(value):
    PickedB.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['b'] = value

    '''
    if PickedSetText.get()==sets[0]: VeryCold.data['b'] = value
    elif PickedSetText.get()==sets[1]: Cold.data['b'] = value
    elif PickedSetText.get()==sets[2]: Warm.data['b'] = value
    elif PickedSetText.get()==sets[3]: Hot.data['b'] = value
    '''
    updatePlots()

def slideC(value):
    PickedC.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['c'] = value
    '''
    if PickedSetText.get()==sets[0]: VeryCold.data['c'] = value
    elif PickedSetText.get()==sets[1]: Cold.data['c'] = value
    elif PickedSetText.get()==sets[2]: Warm.data['c'] = value
    elif PickedSetText.get()==sets[3]: Hot.data['c'] = value
    '''
    updatePlots()

def slideD(value):
    PickedD.set(value)
    foundSetIndex = next((i for i, x in enumerate(setsObjects) if x.data['name'] == PickedSetText.get()), None)
    setsObjects[foundSetIndex].data['d'] = value

    '''
    if PickedSetText.get()==sets[0]: VeryCold.data['d'] = value
    elif PickedSetText.get()==sets[1]: Cold.data['d'] = value
    elif PickedSetText.get()==sets[2]: Warm.data['d'] = value
    elif PickedSetText.get()==sets[3]: Hot.data['d'] = value
    '''
    updatePlots()



#dropDowns
setsNames = list(map(lambda x: x.data['name'], setsObjects))

setsDropdown = OptionMenu(root, clickedSet, *setsNames, command=pickSet)
setsDropdown.config(width=30)
setsDropdown.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

functionsDropdown = OptionMenu(root, clickedFunction, *functions, command=pickFun)
functionsDropdown.config(width=30)
functionsDropdown.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

setsListbox = Listbox(root, listvariable=setsNames, selectmode=MULTIPLE, width=20, height=10)
setsListbox.grid(column=6, row=0,padx=20,pady=20, columnspan=2, rowspan=10)
setsNamesList = list(setsNames)
print(setsNames)
for i in list(setsNames):
    print(i)
    setsListbox.insert(END, i)

btnUpdate = Button(root, command=updatePlots, text="Update")
btnUpdate.grid(row=11, column=6)


#sliders
slideA = Scale(root, from_=-5, to=40, orient = HORIZONTAL, command = slideA)
slideA.config(length=300, tickinterval =5)
slideA.grid(row=3, column=0, padx=20, columnspan=2)

slideB = Scale(root, from_=-5, to=40, orient = HORIZONTAL, command = slideB)
slideB.config(length=300, tickinterval =5)
slideB.grid(row=5, column=0, padx=20, columnspan=2)

slideC = Scale(root, from_=-5, to=40, orient = HORIZONTAL, command = slideC)
slideC.config(length=300, tickinterval =5)
slideC.grid(row=7, column=0, padx=20, columnspan=2)

slideD = Scale(root, from_=-5, to=40, orient = HORIZONTAL, command = slideD)
slideD.config(length=300, tickinterval =5)
slideD.grid(row=9, column=0, padx=20, columnspan=2)

#labels
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
pickedC.grid(row=13, column =0)
pickedD.grid(row=13, column =1)

Legend = StringVar()
legendLabel = Label(root, textvariable=Legend, font=("Helvetica", 12))
legendLabel.grid(row=11, column = 3, columnspan = 5, rowspan=6)

btn = Button(root, command=export, text="Export to .CSV")
btn.grid(row=16, column=0)

fig=Figure(figsize=(14,8), dpi=200)
#fig.add_subplot(111).plot([VeryCold.data['a'],VeryCold.data['b'],VeryCold.data['c']],[0,1,0])
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=5, rowspan=15, columnspan=5)
updatePlots()
pickSet(setsObjects[1].data['name'])
pickFun(functions[0])

root.mainloop()
