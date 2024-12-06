"""Sample program for Pickering PCI/PCI Thermocouple simulator cards using the Pipx40 VISA Python Wrapper"""

from __future__ import print_function
from Pipx40 import *

if __name__ == "__main__":

    # Set the resource string of the card to connect to
    # This can be obtained from the Pickering General Soft Front Panel
    resourceString = "PXI21::1::INSTR"

    # To access the first subunit of a card, set subUnit to 1
    subunit = 1

    print("Sample program for Pickering PXI/PCI Thermocouple simulator cards using the Pipx40 VISA Python Wrapper")
    print()

    # Open a specific card using pipx40_card()
    card = pipx40_card(resourceString, 0 , 0)

    # This function returns information about the card,
    # Model name, Serial number and Firmware revision
    error, cardId = card.GetCardId()

    # Check for errors, ideally after every function call:
    if error:
        # This function will take an error code and return a string description of the error
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    print("Successfully connected to specified card at {}".format(resourceString))
    print("Card ID: ", cardId)

    # Thermocouple specific functions:

    # Set subunit voltage range to auto
    print("Setting range to auto...")

    range = card.TS_RANGE["AUTO"]
    error = card.VSourceSetRange(subunit, range)

    if error:
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    # Get voltage range of a subunit
    error, range = card.VSourceGetRange(subunit)

    if error:
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    if range == card.TS_RANGE["AUTO"]:
        print("Set subunit ", subunit, " range to auto.")

    # Set voltage to 19.5 mV on the subunit
    mvolts = 19.5

    print("Setting voltage to ", mvolts, " mV...")

    error = card.VSourceSetVoltage(subunit, mvolts)

    if error:
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    # Read the voltage of a subunit
    error, mvolts = card.VSourceGetVoltage(subunit)

    if error:
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    print("Voltage set to ", mvolts, " mV.")

    # 41-760-001 Example; Setting channel isolation switches
    # Please refer to your thermocouple manual to find the subunit for
    # your specific isolation switch subunit.
    isolation_subunit = 33

    if "41-760-001" in cardId:
        # Turn Vo1 on
        error = card.SetChannelState(isolation_subunit, 1, 1)

        # Turn Vcold1 on
        error = card.SetChannelState(isolation_subunit, 2, 1)

        # Turn Vo1 off
        error = card.SetChannelState(isolation_subunit, 1, 0)

        # Turn Vcold1 off
        error = card.SetChannelState(isolation_subunit, 2, 0)

    if error:
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()


    # Get compensation block temperatures
    error, temperatures = card.VSourceGetTemperature(card.ATTR["TS_TEMPERATURES_C"])

    if error:
        err, errorString = card.ErrorMessage(error)
        print("Error: ", errorString)
        exit()

    index = 0
    for index, temperature in enumerate(temperatures):
        print("Compensation block temperature ", index, ": ", temperature, "C")

    # Get Thermocouple subunit information
    err, low_range_min, \
    low_range_med, \
    low_range_max, \
    low_range_max_dev, \
    low_range_prec_pc, \
    low_range_prec_delta, \
    med_range_min, \
    med_range_med, \
    med_range_max, \
    med_range_max_dev, \
    med_range_prec_pc, \
    med_range_prec_delta, \
    max_range_min, \
    max_range_med, \
    max_range_max, \
    max_range_max_dev, \
    max_range_prec_pc, \
    max_range_prec_delta = card.VSourceInfo(subunit)

    # Close card
    error = card.Close()