from __future__ import print_function
from Pipx40 import *
import sys

base = pipx40_base()

count = base.CountFreeCards()

if count > 0:
    list = base.FindFreeCards()
    print("\nThere are ", count, "cards available", list)
else:
    print("No cards available")
ON = 1
OFF = 0
for c in range(count):   
    if(sys.version_info>(3,0,0)): 
        list[c] = str.encode(list[c])
    else:
        list[c] = str(list[c])
    #card = pipx40_card(list[c],0,0)
    card = pipx40_card(list[c],0,0);
    err, id = card.GetCardId()
    
    if (err != 0):
        print (err)
    else:
        print(id)

    err = card.ClearCard()
    if (err != 0):
        print (err)  

    err, inSub, outSub = card.GetSubCounts()
    if (err != 0):
        print (err)
    else:
        print("\nNumber of Input Sub-Units", inSub)
        print("Number of Output Sub-Units", outSub) 
        sub = 1
        while sub <= outSub:
            #sub starts from base 1
            err = card.ClearSub(sub)
            if err != 0:
                print (err)
                break
            err, subTypeDisplay = card.SubType(sub,1)
            if err != 0:
                print (err)
                break
            else:
                print(subTypeDisplay)              
            
            err, subType,rows,cols = card.SubInfo(sub,1)
            if err != 0:
                print(err)
                break
            else:
               print("SubType ",subType)
               print ("\nNumber of Rows:", rows, "Number of Columns",cols) 
            
            dwords, bits = card.SubSize(sub,1)
            print ("Number of DWORDS required:", dwords, " Number of bits: ", bits)

            err, status = card.SubStatus(sub)
            if err != 0:
                print(err)
                break
            MatrixSub = [4,5,11]
            if any (subType == mat for mat in MatrixSub):
                x = 1
                
                while x <= cols:
                    y = 1
                    while y <= rows:
                        err = card.SetCrosspointState(sub,y,x,ON)
                        #sleep(1)
                        err = card.SetCrosspointState(sub,y,x,OFF)
                        if err != 0:
                            err,stringg = card.ErrorMessage(err)
                            print("Unable to connect", err, stringg) 
                        else:                 
                            print("Successfully Connected Crosspoint: X-", x,"Y-", y)
                        y+=1
                    x+=1
            else:
                bit = 1
                while bit <= bits:
                    err = card.SetChannelState(sub,bit,ON)
                    #sleep(1)
                    err = card.SetChannelState(sub,bit,OFF)
                    if err != 0:
                        print("Unable to connect", card.ErrorMessage(err)) 
                    else:                 
                        print("Successfully Connected bit :", bit)
                    bit +=1
            sub+=1            
            #close card
    err = card.Close()



     


