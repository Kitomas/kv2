#the 60 byte header goes as:
#width and height of frame; 2 bytes
#file type; 1 byte
#is video?; 1 byte (0=false,1=true)
#if video, what framerate?; 1 byte which represents a fixed-point number with a precision of a tenth (max is 20fps, but for demo purposes: 255=25.5fps)
#amount of frames in file; 3 bytes
#useless, but reserved for potential future use; 4 bytes
#palette information for 16 colors; 3 bytes each (24 bit color) * 16 = 48 bytes (if type 1, then the interpreter should ignore colors 2-15)
#-----------------------------------------------------------
#begin imagestream, formatted as whatever type is included


#This is the configuration file used for the converter; simply replace the definitions with what your heart desires.
#Any arguments given will override the contents of this config, given in the order of: name outresX outresY type outfps dither

#The image/video that you want to convert (excluding extension)
#Ex. "samples/redditor"
name="samples/Lenna"

#51x19 is the resolution of a computer, and 164x81 is the max resolution of the largest monitor cluster (both numbers must be 1-255)
outputresolution=(164,81)

#types go as follows:
#0=4 bits per pixel; only supports solid colors
#------------------------------------------------
#1= 1 byte per 6 pixels; monochrome to utilize sub pixel characters to produce a very high 4:3(ish) resolution at max (164*2,81*3)
#each byte represents the string.char() number needed for that special character, with amounts higher than 159 representing a char with inverted colors
#Example lua code:
#if byte >= 160 then
#	if monitor.getBackgroundColor()==32768 then
#		monitor.setBackgroundColor(1)
#		monitor.setTextColor(32768)
#	end
#	monitor.write(string.char(160-(byte-159))) this is the relationship between the byte and the inverted char
#else
#	if monitor.getBackgroundColor()==1 then
#		monitor.setBackgroundColor(32768)
#		monitor.setTextColor(1)
#	end
#	monitor.write(string.char(byte))
#end
type=1

#your desired fps (-1 for original fps) (will get rounded to nearest tick; 12fps=10fps;max is 20fps)
outputfps=8

#flip this to 1 to turn on dithering
dither=0

#if you have a large file and want to render overnight or something, change
#this to 1 to shutdown your computer after it's done
#make sure there're no processes running that would prevent shutdown
shutdown=0

#debug tool; tuple for each phase, with 1 determining if that phase gets deleted
#having them both be 1 saves on hard drive space
#having them both be 0 seemingly saves on processing time
#format is (resize,convertpalette)
deltempfiles=(1,0)