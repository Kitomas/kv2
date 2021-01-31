# kv2
A program used to put images in videos into Computercraft, using a file format named ".kv2".<br />
The converter is a python script that takes an mp4, a png, or a jpg and converts it into a kv2. 

The structure of a kv2, including header, is detailed in the config.<br />
This kv2 can then be played with the bundled player inside Computercraft.


the 60 byte header goes as:
-----------------------------
width and height of frame; 2 bytes<br />
file type; 1 byte<br />
is video?; 1 byte (0=false,1=true)<br />
if video, what framerate?; 1 byte which represents a fixed-point number with a precision of a tenth (max is 20fps, but for demo purposes: 255=25.5fps)<br />
amount of frames in file; 3 bytes<br />
useless, but reserved for potential future use; 4 bytes<br />
palette information for 16 colors; 3 bytes each (24 bit color) * 16 = 48 bytes (if type 1, then the interpreter should ignore colors 2-15)<br />
begin imagestream, formatted as whatever type is included<br />


types go as follows:
-----------------------
0=4 bits per pixel; only supports solid colors<br />
1=1 byte per 6 pixels; monochrome to utilize sub pixel characters to produce a very high 4:3(ish) resolution at max (164*2,81*3)<br />
each byte represents the string.char() number needed for that special character, with amounts higher than 159 representing a char with inverted colors<br />
Example type 1 lua code:<br />
if byte >= 160 then<br />
­  ­if monitor.getBackgroundColor()==32768 then<br />
­    ­monitor.setBackgroundColor(1)<br />
­    ­monitor.setTextColor(32768)<br />
­  ­end<br />
­  ­monitor.write(string.char(160-(byte-159))) this is the relationship between the byte and the inverted char<br />
else<br />
­  ­if monitor.getBackgroundColor()==1 then<br />
­    ­monitor.setBackgroundColor(32768)<br />
­    ­monitor.setTextColor(1)<br />
­  end<br />
­    ­monitor.write(string.char(byte))<br />
end<br />