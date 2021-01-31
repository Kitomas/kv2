--[[
This is the built-in type 1 .kv2 player
I can't seem to think of a way to 
make this more efficient, so feel
free to optimize this

(Btw you don't actually need
to include the file extension)
Usage: playt1 /folder/file.kv2
--]]

args={...}
--os.sleep(4)
monitor=peripheral.find("monitor")
monitor.setTextScale(0.5)
monitor.clear()
monitor.setTextColor(1)
monitor.setBackgroundColor(32768)
local function framecountconvert(a,b,c) return ((a*65535)+(b*256)+c) end
if args[1]:sub(args[1]:len()-3,args[1]:len()) ~= ".kv2" then
    args[1]=args[1]..".kv2" end
local file=io.open(args[1],"rb")
local resolution={file:read(),file:read()}
local filetype=file:read()
local isvideo=file:read()
local vidfps=file:read()
local fca=file:read()
local fcb=file:read()
local fcc=file:read()
local vidlen=framecountconvert(fca,fcb,fcc)--converting 3 bytes to an int
for i=1,4 do file:read() end --currently unused bytes
local palette={}
for i=1,48 do table.insert(palette,file:read()) end
function displayframe(mon)
    local tempnum=1
    local tempbgcolor=1
    for iy=1,resolution[2] do
        mon.setCursorPos(1,iy)
        for ix=1,resolution[1] do
            tempnum=file:read()
            tempbgcolor=mon.getBackgroundColor()
            if tempnum >= 160 then
                if tempbgcolor==32768 then
                    mon.setBackgroundColor(1)
                    mon.setTextColor(32768)
                end
                mon.write(string.char(160-(tempnum-159)))
            else
                if tempbgcolor==1 then
                    mon.setBackgroundColor(32768)
                    mon.setTextColor(1)
                end
                mon.write(string.char(tempnum))
            end
        end
    end
    return true
end
local plzbro=0 --please dont too long without yield me program ty
for i=1,vidlen do
    displayframe(monitor)
    plzbro=plzbro+1 --yeah uhh mess with this till your heart is content; it just tries to render a frame as quickly as it can
    if plzbro > 20 then plzbro=0 os.sleep() end
    print(i..'/'..vidlen,"Frames")
end
monitor.setBackgroundColor(32768)
monitor.setTextColor(1)
file:close()
