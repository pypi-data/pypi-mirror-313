"""Sample program for Pickering PCI/PXI Non Precision Resistor Cards using the Pipx40 VISA Python Wrapper"""

from __future__ import print_function
from Pipx40 import *

if __name__ == "__main__":

    RsrcString = 'PXI1::4::INSTR'
    subunit = 1

    # Initializing card.
    print("Opening card")
    card = pipx40_card(RsrcString,0,0)
    
    # Getting Card ID.
    error, id = card.GetCardId()
    print(id)

    # Check for errors.
    if error:
        # This function will take an error code and return a string description of the error.
        error, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    print("Successfully connected to specified card.")
    print("Card ID: ", id)

    err, ins, outs = card.GetSubCounts()
    print("Number of Subunits:", ins, "inputs,", outs, "outputs.")

    # This function clears (de-energises) all outputs of a subunit.
    card.ClearSub(subunit)

    # This is the resistance value that is going to be set.
    resistance = 100

    # This function will get the state of our output subunit.
    data = card.GetChannelPattern(subunit)
    data = data[1].tolist()

    data[0] = resistance

    # Now we will set a resistance value by writing a binary resistor pattern directly.
    print("Setting resistor value of {} ohms with binary pattern 0b{}".format(data[0],"{0:b}".format(data[0])))
    card.SetChannelPattern(subunit, data)

    # Obtain the actual resistance of the same subunit.
    data = card.GetChannelPattern(subunit)
    data = data[1].tolist()
    print("Got resistance value of {} ohms - 0b{}".format(data[0],"{0:b}".format(data[0])))

    # This function clears (de-energises) all outputs of a subunit.
    card.ClearSub(subunit)
    print("Closing card")
    err = card.Close()
