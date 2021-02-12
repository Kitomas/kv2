import time
t0=time.time()
from cconfig import *
import sys
import cv2
import os
import math
from PIL import Image
testing=0
PALETTE = [
    240, 240, 240,	#01 white
    242, 178, 51,	#02 orange
    229, 127, 216,	#03 magenta
    153, 178, 242,	#04 lightblue
    222, 222, 108,	#05 yellow
    127, 204, 25,	#06 lime
    242, 178, 204,	#07 pink
    76, 76, 76,		#08 gray
    153, 153, 153,	#09 lightgray
    76, 153, 178,	#10 cyan
    178, 102, 229,	#11 purple
    51, 102, 204,	#12 blue
    127, 102, 76,	#13 brown
    87, 166, 78,	#14 green
    204, 76, 76,	#15 red
    25, 25, 25,		#16 black
] + [25, ] * 240 * 3 #filling in the 768 requirement
PALETTEtype1 = [
    PALETTE[0], PALETTE[1], PALETTE[2],	#01 white
    PALETTE[45],PALETTE[46],PALETTE[47],#16 black
] + [PALETTE[45],PALETTE[46],PALETTE[47], ] * 254 #filling in the 768 requirement
args=sys.argv
if len(args) > 1: #name
    name=args[1]
if len(args) > 3: #outputresolution
    outputresolution=(args[2],args[3])
if outputresolution[0]>65535:
    outputresolution=(65535,outputresolution[1])
if outputresolution[1]>65535:
    outputresolution=(outputresolution[0],65535)
if len(args) > 4: #type
    type=args[4]
if len(args) > 5: #dither
    dither=args[5]
isvideo=0
if os.path.exists("./"+name+".mp4"): #if mp4 is found, then isvideo turns true
    isvideo=1
def ccopy(thing):
    return thing
if type==1:
    originaloutres=ccopy(outputresolution) #maybe otherwise would leave a trace? idk i wont care enough to learn the proper syntax for this rn
    outputresolution=(outputresolution[0]*2,outputresolution[1]*3)
vidlen=1
if isvideo==1:
    video = cv2.VideoCapture("./"+name+".mp4")
    vidfps = video.get(cv2.CAP_PROP_FPS)
    vidlen = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
else:
    if os.path.exists("./"+name+".jpg"):
        imgpath="./"+name+".jpg"
        image = cv2.imread(imgpath)
    elif os.path.exists("./"+name+".png"):
        imgpath="./"+name+".png"
        image = cv2.imread(imgpath)
try: #delete prev tmp folder
    if os.path.exists('./tmp'):
        os.system("rmdir /s /q tmp")
except OSError:
    print('Error Deleting Previous Tmp Directory')
try: #make phase 1 directory
    if not os.path.exists('tmp/ph1'):
        os.makedirs('tmp/ph1')
except OSError:
    print('Error Creating Phase 1 Directory')
try: #make phase 2 directory
    if not os.path.exists('tmp/ph2'):
        os.makedirs('tmp/ph2')
except OSError:
    print('Error Creating Phase 2 Directory')
currentframe=0
try: #deleting previous .kv2
    if os.path.exists('./'+name+'.kv2'):
        os.system('rm ./'+name+'.kv2')
except OSError:
    print("Could not delete previous .kv2")
f = open(name+".kv2", "ab")
#i stole this off of stackoverflow i think LMAO
#actually now that i think about it, quite a bit of this program is
def float_range(A, L=None, D=None):
    #Use float number in range() function
    # if L and D argument is null set A=0.0 and D = 1.0
    if L == None:
        L = A + 0.0
        A = 0.0
    if D == None:
        D = 1.0
    while True:
        if D > 0 and A >= L:
            break
        elif D < 0 and A <= L:
            break
        yield float("%g" % A) # return float number
        A = A + D
def extractimage(num):
    global video
    ret,frame = video.read()
    if ret:
        name = './tmp/frame' + str(num) + '.jpg'
        return frame,name
    else:
        return False
def resizeimage(imagepath, inter = cv2.INTER_AREA,):
    global outputresolution
    return cv2.resize(cv2.imread(imagepath), outputresolution, interpolation = inter)
def paletteconvert(num): #make sure to save this as png
    global PALETTE
    global PALETTEtype1
    global currentframe
    global type
    global dither
    pimage = Image.new("P", (1, 1), 0)
    if type==0: #determining which palette to use
        pimage.putpalette(PALETTE)
    elif type==1:
        pimage.putpalette(PALETTEtype1)
    image = Image.open("./tmp/ph1/frame"+str(num)+".jpg")
    image = image.convert("RGB")
    #nimage=image.quantize(palette=pimage)
    image.load()
    pimage.load()
    return image._new(image.im.convert("P", dither, pimage.im))
def type1choice(tmpimage,xc,yc,thess):
    global PALETTEtype1
    tpv = tmpimage.getpixel((xc,yc))
    if tpv==(PALETTEtype1[0],PALETTEtype1[1],PALETTEtype1[2]):	#on
        thess="1"+thess
    if tpv==(PALETTEtype1[3],PALETTEtype1[4],PALETTEtype1[5]):	#off
        thess="0"+thess
    return thess
def bytestreamconvertsave(num):
    global outputresolution
    global f
    global type
    ths=''
    tempimage=Image.open("./tmp/ph2/frame"+str(num)+".png")
    tempimage=tempimage.convert("RGB")
    if type==0:
        dolater=1 #lol
    if type==1:
        for iy in range(0,outputresolution[1],3):
            for ix in range(0,outputresolution[0],2):
                ths=type1choice(tempimage,ix,iy,ths)
                ths=type1choice(tempimage,ix+1,iy,ths)
                ths=type1choice(tempimage,ix,iy+1,ths)
                ths=type1choice(tempimage,ix+1,iy+1,ths)
                ths=type1choice(tempimage,ix,iy+2,ths)
                ths=type1choice(tempimage,ix+1,iy+2,ths)
                f.write(int('10'+ths,2).to_bytes(1, byteorder="big"))
                ths=''
def roundfpstonearesttick(fps): #returns the exact delay in ticks, not fps
    newfps=math.floor(((1/fps)/.05)+.5)
    if newfps < 1:
        newfps=1
    elif newfps > 255:
        newfps=255
    return newfps
def cut(num):
    return math.floor(num*1000)/1000
def cullframes():# i know this is messy, but this is the way i came up with for selectively deleting frames to fit the desired fps
    global vidfps
    global outputfps
    global vidlen
    if outputfps != -1:
        ratio=1-((1/(roundfpstonearesttick(outputfps)*.05))/vidfps)
        countera=0.0
        target=math.ceil((1/(roundfpstonearesttick(outputfps)*.05))*(vidlen/vidfps))
        print(vidlen,target)
        if ratio <= .5:
            for i in range(vidlen):
                print("Frame "+str(i+1)+"/"+str(vidlen)+" - Phase 4/5: Cull frames to fit custom fps")
                countera=float(countera+ratio)
                if (countera-int(countera-1)) >= 1:
                    if os.path.exists("./tmp/ph2/frame"+str(i)+".png"):
                        os.system("rm ./tmp/ph2/frame"+str(i)+".png")
                    countera=float(countera-math.floor(countera))
        else:
            ratio=1-ratio
            framecount=vidlen
            for i in range(vidlen):
                print("Frame "+str(i+1)+"/"+str(vidlen)+" - Phase 4/5: Cull frames to fit custom fps")
                countera=float(countera+ratio)
                if not countera >= 1 and framecount > target:
                    if os.path.exists("./tmp/ph2/frame"+str(i)+".png"):
                        os.system("rm ./tmp/ph2/frame"+str(i)+".png")
                        framecount -= 1
                else:
                    countera=float(countera-math.floor(countera))
print("-BEGIN-")
testing=0
#writing header into to file
rxb="{0:b}".format(originaloutres[0])
while len(rxb) < 16:
    rxb="0"+rxb
ryb="{0:b}".format(originaloutres[1])
while len(ryb) < 16:
    ryb="0"+ryb
f.write(int(rxb[:8],2).to_bytes(1, byteorder="big"))
f.write(int(rxb[8:16],2).to_bytes(1, byteorder="big"))
f.write(int(ryb[:8],2).to_bytes(1, byteorder="big"))
f.write(int(ryb[8:16],2).to_bytes(1, byteorder="big"))
f.write(type.to_bytes(1, byteorder="big"))
f.write(isvideo.to_bytes(1, byteorder="big"))
newoutfps=roundfpstonearesttick(outputfps)
f.write(int(newoutfps).to_bytes(1, byteorder="big"))#written as exact delay in ticks
if isvideo==1:
    nvidlen=math.ceil((1/(roundfpstonearesttick(outputfps)*.05))*(vidlen/vidfps))
else:
    nvidlen=1
if nvidlen > ((2**24)-1):
    nvidlen=(2**24)-1
vlb="{0:b}".format(nvidlen)
while len(vlb) < 24:
    vlb="0"+vlb
f.write(int(vlb[:8],2).to_bytes(1, byteorder="big"))
f.write(int(vlb[8:16],2).to_bytes(1, byteorder="big"))
f.write(int(vlb[16:24],2).to_bytes(1, byteorder="big"))
for i in range(2):
    f.write((0).to_bytes(1, byteorder="big"))
for i in range(48):
    f.write(PALETTE[i].to_bytes(1, byteorder="big"))
if isvideo==0 and testing==0:
    print('Phase 1/3: Resize image')
    cv2.imwrite('./tmp/ph1/frame0.jpg',resizeimage(imgpath))
    print('Phase 2/3: Palette swap image')
    paletteconvert(0).save('./tmp/ph2/frame0.png')
    if deltempfiles[0]==1:
        os.remove('./tmp/ph1/frame0.jpg')
    print('Phase 3/3: Writing image to .kv2')
    bytestreamconvertsave(0)
    if deltempfiles[1]==1:
        os.remove('./tmp/ph2/frame0.png')
elif isvideo==1 and testing==0:
    for i in range(vidlen):
        print("Frame "+str(i+1)+"/"+str(vidlen)+" - Phase 1/5: Extract frame")
        tmpframe,tmpname=extractimage(i)#extract frame
        cv2.imwrite(tmpname,tmpframe)#save frame at tmp root
        print("Frame "+str(i+1)+"/"+str(vidlen)+" - Phase 2/5: Resize frame")
        cv2.imwrite('./tmp/ph1/frame'+str(i)+'.jpg',resizeimage(tmpname))#resize and save
        os.system('rm '+tmpname)#delete original frame
        print("Frame "+str(i+1)+"/"+str(vidlen)+" - Phase 3/5: Palette swap frame")
        paletteconvert(i).save('./tmp/ph2/frame'+str(i)+'.png')#palette swap and save
        if deltempfiles[0]==1:#maybe delete resized image
            os.system('rm ./tmp/ph1/frame'+str(i)+'.jpg')
    cullframes()
    displayi=1
    for i in range(vidlen):
        if os.path.exists("./tmp/ph2/frame"+str(i)+".png"):
            print("Frame "+str(displayi)+"/"+str(nvidlen)+" - Phase 5/5: Writing images to .kv2")
            displayi=displayi+1
            bytestreamconvertsave(i)
            if deltempfiles[1]==1:
                os.system("rm ./tmp/ph2/frame"+str(i)+".png")
else: #misc. and var probe area
    placeholder=1
    print(cut(10))
#deletion and tying up loose ends
f.close()
if deltempfiles[0]==1:
    try:
        if os.path.exists('.\\tmp'):
            os.system("rmdir /s /q tmp\\ph1")
    except OSError:
        print("Could not delete phase 1 folder")
if deltempfiles[1]==1:
    try:
        if os.path.exists('.\\tmp'):
            os.system("rmdir /s /q tmp\\ph2")
    except OSError:
        print("Could not delete phase 2 folder")
if deltempfiles[0]==1 and deltempfiles[1]==1:
    try:
        if os.path.exists('.\\tmp'):
            os.system("rmdir /s /q tmp")
    except OSError:
        print("Could not delete tmp folder")
try:
    if os.path.exists('.\\__pycache__'):
        os.system("rmdir /s /q __pycache__")
except OSError:
    print("Could not delete __pycache__ folder")
cv2.destroyAllWindows()
processtime=cut(time.time()-t0)
ptm=math.floor(processtime/60)
print("-FINISHED-\n\nRendered in:\n"+str(ptm)+" min \n"+str(cut(processtime-ptm*60))+' sec\nSaved as: "'+name+'.kv2"')
if shutdown==1:
    os.system('shutdown /s')
os.system('pause')
