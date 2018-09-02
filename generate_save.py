import os

for savefile in 'Red', 'Blue-1.0', 'Blue-1.2':
    
    sav = [0x00] * 0x8000

    # Requirements for Stadium to acknowledge the file at all
    
    sav[0x260A] = 0x29 # map = poke center
    sav[0x29F7] = 0x20 # pokedex obtained (bit 5)
    sav[0x2598:0x2598+1] = [0x50] # name

    
    if savefile == 'Red':
        
        sav[0x2F2C] = 1 # number of pokemon in party
        sav[0x2F34:0x2F34+0x1] = [0x99] # pokemon = bulbasaur
        
    else:
        
        sav[0x284C] = 0x80 + 11 # current box: 12 (have changed boxes before)
        sav[0x30C0] = 23 # number of pokemon in current box (box 12)

        if savefile == 'Blue-1.0':
            
            sav[0x336A:0x33CD] = [     0x00,0x00,0x00,0x80,0x1E,0x4E,0xB0,0x00,0x00,0x00,0x00,0x00,     0x00,0x00,      0x00,0x00,0x00,
                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                       0x0C,0x00,0x78,0x00,0x00,0x01,0x04,0x01,0x0C,0x00,0x78,0x00,     0x01,0x8C,      0x0C,0x00,0x78,
                                  0x00,0x00,0x00,0x38,0x01,0xA4,0x02,0x10,0x00,0x00,0x00,0xCC,0x01,0x30,0x00,0xE8,
                                       0x80,0x00,0x00,0x3F,0x80,0x00,0x00,0x03,0x03,0x06,0xB0,0x16,     0x60,0x00,      0x13,0x5B,0x50,
                                  0x80,0x13,0x58,0x30,0x80,0x1E,0x09,0x84,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
            sav[0x3446:0x3467] = [0x00,0x00,0x00,0x00,0x00,0x40,0x00,0x8C,0x02,0x00,0x00,
                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00,0x00,0x3F,
                                  0x00,0x00,0xFF,0xFF,0xFF,0x00,0xFF,0xFF,0x00,0x00,0x00]
            sav[0x3522:0x3543] = [0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,
                                  0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,
                                  0x80,0x80,0x50,0x50,0x80,0x80,0x50,0x50,0x80,0x80,0x80]
        
            sav[0x33BD:0x33C1] = 0x80135830.to_bytes(4 ,'big') # don't crash
            sav[0x33C5:0x33C9] = 0x801E5E74.to_bytes(4 ,'big') # ptr to payload
            
        elif savefile == 'Blue-1.2':
            
            sav[0x336A:0x33CD] = [     0x00,0x00,0x00,0x80,0x1E,0x50,0xE0,0x00,0x00,0x00,0x00,0x00,     0x00,0x00,      0x00,0x00,0x00,
                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                       0x0C,0x00,0x78,0x00,0x00,0x01,0x04,0x01,0x0C,0x00,0x78,0x00,     0x01,0x8C,      0x0C,0x00,0x78,
                                  0x00,0x00,0x00,0x38,0x01,0xA4,0x02,0x10,0x00,0x00,0x00,0xCC,0x01,0x30,0x00,0xE8,
                                       0x80,0x00,0x00,0x3F,0x80,0x00,0x00,0x03,0x03,0x06,0xB0,0x16,     0x60,0x00,      0x13,0x5B,0x50,
                                  0x80,0x13,0x5A,0x40,0x80,0x1E,0x0B,0xB4,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
            sav[0x3446:0x3467] = [0x00,0x00,0x00,0x00,0x00,0x40,0x00,0x8C,0x02,0x00,0x00,
                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00,0x00,0x3F,
                                  0x00,0x00,0xFF,0xFF,0xFF,0x00,0xFF,0xFF,0x00,0x00,0x00]
            sav[0x3522:0x3543] = [0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,
                                  0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,0x50,
                                  0x80,0x80,0x50,0x50,0x80,0x80,0x50,0x50,0x80,0x80,0x80]
            
            sav[0x33BD:0x33C1] = 0x80135A40.to_bytes(4 ,'big') # don't crash
            sav[0x33C5:0x33C9] = 0x801E60A4.to_bytes(4 ,'big') # ptr to payload
        
        sav[0x344F] = 0x50 # don't crash
        
        if savefile == 'Blue-1.0':
            
            payload = [
                0x3c18800b, # enable final battle against mewtwo
                0x24020002,
                0xa302f732,
                
                0x03E00008 # ret
            ]
            
        elif savefile == 'Blue-1.2':
            
            payload = [
                0x3c18800b, # enable final battle against mewtwo
                0x24020002,
                0xa302f862,
                
                0x03E00008 # ret
            ]

        assert len(payload) < (0x1A60 - 4)

        for i,x in enumerate(payload):
            sav[0x4004 + i*4 : 0x4004 + (i+1)*4] = x.to_bytes(4 ,'big')

    checksum = 255
    for x in sav[0x2598:0x3523]:
        checksum -= x
        checksum %= 256
        
    sav[0x3523] = checksum

    assert len(sav) == 0x8000
    
    f=open(savefile + '.sav','wb')
    f.write(bytes(sav))
    f.close()

