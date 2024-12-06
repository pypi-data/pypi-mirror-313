"""Sample program for Pickering PCI/PXI Resistor Cards using the Pipx40 VISA Python Wrapper"""

from __future__ import print_function
from Pipx40 import *

if __name__ == "__main__":

    RsrcString = 'PXI21::3::INSTR'
    subunit = 1

    # Initializing card
    print("Opening card")
    card = pipx40_card(RsrcString,0,0)

    # Getting Card ID
    error, id = card.GetCardId()
    print(id)

    # Check for errors
    if error:
        # This function will take an error code and return a string description of the error
        error, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    print("Successfully connected to specified card.")
    print("Card ID: ", id)

    err, ins, outs = card.GetSubCounts()
    print("Number of Subunits:", ins, "inputs,", outs, "outputs.")

    # This function clears (de-energises) all outputs of a subunit
    card.ClearSub(subunit)

    # This function obtains the capabilities and characteristics of the specified resistor card
    error, \
    minResistance, \
    maxResistance, \
    referenceResistance, \
    precisionPercent, \
    precisionDelta, \
    int1, \
    internalPrecision, \
    capabilities \
        = card.ResGetInfo(subunit)

    print("Min Resistance: ", minResistance)
    print("Max Resistance: ", maxResistance)
    print("Reference resistance: ", referenceResistance)
    print("Precision %: ", precisionPercent)
    print("Precision delta: ", precisionDelta)
    print("Internal Precision: ", internalPrecision)

    # Read card calibration date and interval
    error, year, day, interval = card.ReadCalibrationDate(subunit, 0)
    print("Calibration year {} day {} interval {}".format(year, day, interval))

    # Set the resistance of the card as close as possible to a specified value
    resistance = 330    # Value in Ohms
    mode = 0

    print("Setting resistance value of", resistance,"Ohms...")
    card.ResSetResistance(subunit, mode, resistance)

    # Obtain the actual resistance of the same subunit
    error, actualResistance = card.ResGetResistance(subunit)
    print("Got resistance value of", actualResistance," Ohms.")

    print("Closing card")
    err = card.Close()
