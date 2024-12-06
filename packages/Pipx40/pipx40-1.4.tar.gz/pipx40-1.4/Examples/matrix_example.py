from Pipx40 import *

ON = 1
OFF = 0
RsrcString = 'PXI3::6::INSTR'

#Initializing card
print(" Opening card")

card = pipx40_card(RsrcString,0,0);

#Getting Card ID
err, id = card.GetCardId()

print("\n",id)

sub = 1 # Sub-Unit 1
#Getting Sub-Unit Information
err, subType,rows,cols = card.SubInfo(sub,1)
if err != 0:
    print(err)
else:
    print ("\nNumber of Rows:", rows, "Number of Columns",cols)

x = 1
#Operating Switch
while x <= cols:
    y = 1
    while y <= rows:
        err = card.SetCrosspointState(sub,y,x,ON)
        err = card.SetCrosspointState(sub,y,x,OFF)
        if err != 0:
            err,string = card.ErrorMessage(err)
            print("Unable to connect", err, string) 
        else:
            print("Successfully Connected Crosspoint: X-", x,"Y-", y)
        y+=1
    x+=1

error = 0

errors = { "ERROR_GEN": 1+error, "ANOTHER_ERROR": 2+error}

print("\n Closing card")
err = card.Close()