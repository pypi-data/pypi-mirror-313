from __future__ import print_function
from Pipx40 import *

ON = 1
OFF = 0
RsrcString = 'PXI78::13::INSTR'

#Initializing card
print(" Opening card")

card = pipx40_card(RsrcString,0,0)

#Getting Card ID
err, id = card.GetCardId()

print("\n",id)
#Operating Switch

sub = 1 # Sub-Unit 1
bit = 2 # bit 1

err = card.SetChannelState(sub,bit,ON)
if err != 0:
    print("Unable to connect", card.ErrorMessage(err))
else:                 
    print("\n Successfully Connected bit :", bit)

bit = 51
err = card.SetChannelState(sub,bit,ON)
if err != 0:
    print("Unable to connect", card.ErrorMessage(err)) 
else:                 
    print("\n Successfully Connected bit :", bit)

err, d = card.GetChannelPattern(sub)
print(err, d)

print("\n Closing card")
err = card.Close()
