#This is the configuration file used for the converter; simply replace the definitions with what your heart desires.
#Any arguments given will override the contents of this config, given in the order of: name outresX outresY type outfps dither

#The image/video that you want to convert (excluding extension)
#Ex. "samples/redditor"
name="samples/redditor"

#51x19 is the resolution of a computer, and 164x81 is the max resolution of the largest monitor cluster (both numbers must be 1-65535)
#(you can utilize multiple monitor clusters to make an even bigger monitor)
outputresolution=(164,81)

#types go as follows:
#0=4 bits per pixel; only supports solid colors
#1= 1 byte per 6 pixels; monochrome to utilize sub pixel characters
type=1

#your desired fps (-1 for original fps) (will get rounded to nearest tick; 12fps=10fps;max is 20fps)
outputfps=8

#flip this to 1 to turn on dithering
dither=1

#if you have a large file and want to render overnight or something, change
#this to 1 to shutdown your computer after it's done
#make sure there're no processes running that would prevent shutdown
shutdown=0

#debug tool; tuple for each phase, with 1 determining if that phase gets deleted
#having them both be 1 saves on hard drive space
#having them both be 0 seemingly saves on processing time
#format is (resize,convertpalette)
deltempfiles=(0,0)