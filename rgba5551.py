from PIL import Image

im = Image.open('cosmog.png')

for y in range(im.size[1]):
    for x in range(0,im.size[0],2):

        if x==0:
            if y==0:
                print('    ',end='')
            else:
                print('\n    ',end='')
            
        r,g,b = im.getpixel((x,y))

        if (r,g,b) == (56,56,128):
            r,g,b,a = (0,0,0,0)
        else:
            r = round(r * 0x1F / 0xFF)
            g = round(g * 0x1F / 0xFF)
            b = round(b * 0x1F / 0xFF)
            a = 1
        
        r2,g2,b2 = im.getpixel((x+1,y))

        if (r2,g2,b2) == (56,56,128):
            r2,g2,b2,a2 = (0,0,0,0)
        else:
            r2 = round(r2 * 0x1F / 0xFF)
            g2 = round(g2 * 0x1F / 0xFF)
            b2 = round(b2 * 0x1F / 0xFF)
            a2 = 1

        rgba5551 = ((r<<27) + (g<<22) + (b<<17) + (a<<16) +
                    (r2<<11) + (g2<<6) + (b2<<1) + a2)

        print('0x%08X'%rgba5551,end=',')
