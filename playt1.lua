--[[
This is the built-in type 1 .kv2 player
I can't seem to think of a way to
make this more efficient, so feel
free to optimize this

(Btw you don't actually need
to include the file extension)
Usage: playt1 /folder/file.kv2

also the third argument is dedicated
to the audio portion which is separate
to kv2, i might add and incorporate
it to the repo at some point
--]]
local function cut(num) return math.floor(num*100)/100 end
--wrapping and resetting
args={...}
if string.lower(args[1]:sub(args[1]:len()-3,args[1]:len()))~='.kv2' then
	args[1]=args[1]..'.kv2' end
if fs.exists(args[1])==false then
	print("!FILE NOT FOUND!") end
local dotape=false
tape0=peripheral.wrap("tape_drive_0")
tape1=peripheral.wrap("tape_drive_1")
if #args >= 2 then
	if tape0 ~= nil and tape1 ~= nil and args[2] then
		tape0.stop()
		tape1.stop()
		tape0.setVolume(1)
		tape1.setVolume(1)
		tape1.seek(-tape1.getSize()-6000)
		tape0.seek(-tape0.getSize()-6000)
		dotape=true
	end
end
monitor=peripheral.wrap("monitor_0")
monitor.setTextColor(1)
monitor.setBackgroundColor(32768)
term.setTextColor(1)
term.setBackgroundColor(32768)
monitor1=peripheral.wrap("monitor_1")
bufcomp=peripheral.wrap("left")
monitor.setTextScale(0.5)
monitor.clear()
--defining some locals
local doavg=true --disable if minimizing lag is your priority
local function seek(t,byte) t.seek(-t.getSize()-6000) t.seek(byte) end
local floor=math.floor
local function cut(num) return floor(num*1000)/1000 end
local function revfloor(num) return (num-floor(num)) end
local mstc=monitor.setTextColor
local msbc=monitor.setBackgroundColor
local mwrite=monitor.write
local mscp=monitor.setCursorPos
local char=string.char
local aligned=0
local alignedt=0
local tsim={1,0}
local b=string.byte
local tmpreadt={}
local invert=0
local buffer=tonumber(bufcomp.getLabel())
local anchor=-4
local function checkbuffer() buffer=tonumber(bufcomp.getLabel()) end
local function alignsam(num) return floor(num/4)*4 end
local midflip=0
local whichtape=0
local yield=0
local upto=0
local avg={}
local function mean(new)
    avg[#avg+1]=new
    local num=0
    for i in pairs(avg) do
        num=num+avg[i]
    end
    return num/#avg
end
local invert={}
for i=160,191 do invert[char(i)]=char(160-(i-159)) end --creating invert check
--read header info
local file=io.open(args[1],"rb")
local rxa=b(file:read(1))
local rxb=b(file:read(1))
local rx=(rxa*256)+rxb
local rya=b(file:read(1))
local ryb=b(file:read(1))
local ry=(rya*256)+ryb
local resolution={rx,ry}
local type=b(file:read(1))
local isvideo=b(file:read(1))
local vidfps=1/(b(file:read(1))/20)
local fca=b(file:read(1))
local fcb=b(file:read(1))
local fcc=b(file:read(1))
local vidlen=(fca*256^2)+(fcb*256)+fcc

for i=1,2 do file:read(1) end
palette={}
for i=1,48 do palette[#palette+1]=b(file:read(1)) end
local function invcon(str)
    nstr=''
    for i=1,str:len() do
        nstr=nstr..invert[str:sub(i,i)]
    end
    return nstr
end
local function solveline(str)
    local length=str:len()
    local tread=''
    local tread2=''
    local tb={}
    local l=1
    local i=0
    local inverted=false
    if invert[str:sub(1,1)]~= nil then
        inverted=true else
        inverted=false end
    local invertc=inverted
    repeat
        i=i+1
        tread=str:sub(i,i)
        tread2=invert[tread]
        if tread2 ~= nil then
            if not invertc then
                tb[#tb+1]=str:sub(l,i-1)
                l=i
                invertc=true
            end
        else
            if invertc then
                tb[#tb+1]=invcon(str:sub(l,i-1))
                l=i
                invertc=false
            end
        end
    until i>=length
    tread=str:sub(l,length)
    tread2=invert[tread:sub(1,1)]
    if tread2 ~= nil then
        tb[#tb+1]=invcon(tread)
    else
        tb[#tb+1]=tread
    end
    return inverted,tb
end
local function displayframe()
    local invertd=false
    for iy=1,resolution[2] do
        mscp(1,iy)
        invertd,tmpreadt=solveline(file:read(resolution[1]))
        for ic=1,#tmpreadt do
            if invertd then
                msbc(1)
                mstc(32768)
                mwrite(tmpreadt[ic])
                invertd=false
            else
                msbc(32768)
                mstc(1)
                mwrite(tmpreadt[ic])
                invertd=true
            end
        end
    end
end
local function look(num,num2)
    local t0p=cut((tape0.getPosition()/6000)*(2/3))
    local t1p=cut((tape1.getPosition()/6000)*(2/3))
    local vs=num/vidfps
    term.clear()
    term.setCursorPos(1,1)
	   io.write('(Ctrl+T to stop)\n')
    io.write('frame: '..num..'/'..vidlen..'\n')
    io.write('raw v seconds:'..cut(vs)..'\n')
    io.write('frame processing time in ticks: '..cut(num2)..'\n')
    if doavg then
        io.write('average frame proc. time in ticks: '..cut(mean(num2))..'\n')
    end
if dotape then
		io.write('anchor:'..anchor..'\n')
		io.write('alignedt: '..alignedt..'\n')
		io.write('aligned:'..aligned..'\n')
		io.write('tape status: '..table.concat(tsim,',')..'\n')
		io.write('tape0 pos: '..t0p..'\n')
		io.write('tape1 pos: '..t1p..'\n')
		if tsim[1]==1 then
			io.write('tape0 desync: '..cut(t0p-vs)..'\n')
		else
			io.write('tape0 desync: N/A\n') end
		if tsim[2]==1 then
			io.write('tape1 desync: '..cut(t1p-vs)..'\n')
		else
			io.write('tape1 desync: N/A\n') end
	end
end
if dotape then
	--tape0.setVolume(0)
	--tape1.setVolume(0)
	tape0.play()
end
if #args >= 3 then
    upto=tonumber(args[3])
    if upto ~= nil then
        if upto < vidlen then
            vidlen=upto
        end
    end
end
look(0,0)
os.sleep(buffer)
for ig=1,vidlen do
    start=os.clock()
    displayframe()
    length=os.clock()-start
    yield=yield+1
    if length < 1/vidfps then
        os.sleep((1/vidfps)-length)
        yield=0
    end
    if yield > 20 then os.sleep(.05) yield=0 print("forced yield") end
    if dotape then
		checkbuffer()
		alignedt=alignsam(ig/vidfps+buffer)
		aligned=alignsam(ig/vidfps+.001)
		if alignedt > anchor and alignedt ~= aligned and midflip==0 then
			anchor=aligned
			midflip=1
			if whichtape==0 then
				seek(tape1,alignedt*(3/2)*6000)
				tape1.play()
				tsim[2]=1
				whichtape=1
			elseif whichtape==1 then
				seek(tape0,alignedt*(3/2)*6000)
				tape0.play()
				tsim[1]=1
				whichtape=0
			end
		end
		if aligned >= alignedt and aligned ~= anchor and midflip == 1 then
			midflip=0
			if whichtape==0 then
				tape1.stop()
				tsim[2]=0
			elseif whichtape==1 then
				tape0.stop()
				tsim[1]=0
			end
		end
	end
	look(ig,length)
end
--wrapping up
monitor.setBackgroundColor(32768)
if vidlen ~= 1 then
    monitor.clear()
end
term.setTextColor(1)
term.setBackgroundColor(32768)
tape0.stop()
tape1.stop()
file:close()
