from Pipx40 import *

RsrcString = "PXI1::6::INSTR"
subunit = 1

print("Opening card")
card = pipx40_card(RsrcString, 0, 0)

data = [0x1F, 0x2F, 0x3F, 0x4F, 0x5F, 0x6F]

err = card.SetAttributeDWORDArray(subunit, 2, 0x100A, data)
err, str  = card.ErrorMessage(err)
print(str)

err, value = card.GetAttributeDWORDArray(subunit, 2, 0x100A, 6)
print(value)

error, id = card.GetCardId()
print(id)

err = card.Close()