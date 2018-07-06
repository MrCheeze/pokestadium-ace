import os

for savefile in 'Red', 'Blue':
    
    sav = [0x00] * 0x8000

    # Requirements for Stadium to acknowledge the file at all
    
    sav[0x260A] = 0x29 # map = poke center
    sav[0x29F7] = 0x20 # pokedex obtained (bit 5)
    sav[0x2598:0x2598+1] = [0x50] # name

    
    if savefile == 'Red':
        
        sav[0x2F2C] = 1 # number of pokemon in party
        sav[0x2F34:0x2F34+0x1] = [0x99] # pokemon = bulbasaur
        
    if savefile == 'Blue':
        
        sav[0x284C] = 0x80 + 11 # current box: 12 (have changed boxes before)
        sav[0x30C0] = 23 # number of pokemon in current box (box 12)
        
        sav[0x33BD:0x33C1] = 0x80135830.to_bytes(4 ,'big') # don't crash
        sav[0x33C5:0x33C9] = 0x801E5E74.to_bytes(4 ,'big') # ptr to payload
        sav[0x344F] = 0x50 # don't crash
        
        payload = [

            # 0x3C188003, # warp to credits on return to main menu
            # 0x2402A982, #  A982 can also be A981 or A478
            # 0xA702B432, #  game will crash at end of credits

            0x3c18800b, # enable final battle against mewtwo
            0x24020002,
            0xa302f732,
            
            0x03E00008 # ret
        ]

        assert len(payload) < (0x1A60 - 4)

        # Payload can be moved to whatever location is easiest to set up,
        #  but the ptr needs to be adjusted to match

        # 801E4EA0-801E5E60 second cart main data
        # 801E5E70-801E78D0 second cart box 1-6
        # 801E78D0-801E9330 second cart box 7-12

        for i,x in enumerate(payload):
            sav[0x4004 + i*4 : 0x4004 + (i+1)*4] = x.to_bytes(4 ,'big')

        # The above is sufficient for a credits warp on emulator, but will crash on console.
        #  On console, something in the data of Pokemon 21-23 needs to be modified to
        #  prevent this crash, but exactly what has not been identified.

    checksum = 255
    for x in sav[0x2598:0x3523]:
        checksum -= x
        checksum %= 256
        
    sav[0x3523] = checksum

    assert len(sav) == 0x8000
    
    f=open(savefile + '.sav','wb')
    f.write(bytes(sav))
    f.close()

