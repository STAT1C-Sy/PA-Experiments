import requests
import time
from common import load_dataset_from_folder

BASE_URL  = "http://localhost:8080"
SINGLE_DB = True
TWO_DB    = True
POSTGRES  = True

if __name__ == "__main__":
    l, m, h, vh, vvh = load_dataset_from_folder("17-01-2022_09-59-33-913650")

    data_length = len(h)
    step_size = int(data_length/20)
    steps = [i*step_size for i in range(1, 21)]

    print("Performing Test...")

    for z in range(15):
        print("Test run: " + str(z))
        for i, d in enumerate(h):
            id = d["uuid"]

            #if SINGLE_DB:
            #    r = requests.get(BASE_URL + "/" + id + "/valueoptions1")
            if TWO_DB:
                r = requests.get(BASE_URL + "/" + id + "/valueoptions2")
            #if POSTGRES:
            #    r = requests.get(BASE_URL + "/" + id + "/valueoptions3")
            
            if i in steps:
                print("Test: " + str((steps.index(i) + 1) * 5) + "% done (" + str(i) + " of " + str(data_length) + ")")
    
        print("Finished Test run: " + str(z))

    print("Done Performing Test!")
