# kv2
A program used to put images in videos into Computercraft, using a file format named ".kv2".
The converter is a python script that takes an mp4, a png, or a jpg and converts it into a kv2. 

The structure of a kv2, including header, is detailed in the config.
This kv2 can then be played with the bundled player inside Computercraft.


the 60 byte header goes as:
width and height of frame; 2 bytes
file type; 1 byte
is video?; 1 byte (0=false,1=true)
if video, what framerate?; 1 byte which represents a fixed-point number with a precision of a tenth (max is 20fps, but for demo purposes: 255=25.5fps)
amount of frames in file; 3 bytes
useless, but reserved for potential future use; 4 bytes
palette information for 16 colors; 3 bytes each (24 bit color) * 16 = 48 bytes (if type 1, then the interpreter should ignore colors 2-15)
-----------------------------------------------------------
begin imagestream, formatted as whatever type is included


types go as follows:
0=4 bits per pixel; only supports solid colors
------------------------------------------------
1=1 byte per 6 pixels; monochrome to utilize sub pixel characters to produce a very high 4:3(ish) resolution at max (164*2,81*3)
each byte represents the string.char() number needed for that special character, with amounts higher than 159 representing a char with inverted colors
Example type 1 lua code:
if byte >= 160 then
	if monitor.getBackgroundColor()==32768 then
		monitor.setBackgroundColor(1)
		monitor.setTextColor(32768)
	end
	monitor.write(string.char(160-(byte-159))) this is the relationship between the byte and the inverted char
else
	if monitor.getBackgroundColor()==1 then
		monitor.setBackgroundColor(32768)
		monitor.setTextColor(1)
	end
	monitor.write(string.char(byte))
end