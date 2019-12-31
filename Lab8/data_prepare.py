import numpy as np
import glob
import os


def load_file(training_index,validation_index,testing_index,path):
    names = glob.glob("../HR Data/*")
    training_sets = []
    validation_sets = []
    testing_sets = []
    for i in range(len(names)):
        names[i] = names[i].replace("\\","/")

    for x in training_index:
        training_sets.append(names[x])
    for x in validation_index:
        validation_sets.append(names[x])
    for x in testing_index:
        testing_sets.append(names[x])

    tr_t, tr_ir= generate_set("",training_sets)
    va_t, va_ir = generate_set("", validation_sets)
    te_t, te_ir = generate_set("", testing_sets)

    return tr_t, tr_ir,va_t, va_ir,te_t, te_ir

def generate_set(path,names):
    t = []
    ir = []
    offset_value = 0
    print(names)
    for i in range(len(names)):
        names[i] = path + names[i]

        training_sets = os.listdir(names[i])

        for j in range(len(training_sets)):
            dest = names[i] + "/" + training_sets[j]
            training_t, training_ir = read_file(dest)

            for k in range(0, len(training_t)):
                training_t[k] = training_t[k] + offset_value

            t.extend(training_t)
            offset_value = t[-1]
            ir.extend(training_ir)
    return t, ir

def read_file(path):
    t_array = []
    ir_array = []
    with open(path) as file:
        t_array = []
        ir_array = []
        while 1:
            text = file.readline()
            if text == "":
                break
            else:
                t,ir = text.strip().split(",")
                t_array.append(int(t))
                ir_array.append(int(ir))
    ir_array = normalize(ir_array)
    t_array = offset_time(t_array)
    return t_array, ir_array

def normalize(array):
    max = np.amax(array)
    min = np.amin(array)
    for i in range(0,len(array)):
        array[i] = (array[i] - min)/(max - min)
    return array

def offset_time(array):
    offset = array[0]
    for i in range(0,len(array)):
        array[i] = array[i] - offset
    return array

