import wave
import struct
import subprocess
import os
import opusenc
import base64
import zlib
import sys

tmp = sys.argv[1] + ".wav"
subprocess.Popen(["ffmpeg", "-i", sys.argv[1], "-ar", "48000", "-ac", "2", "-y", tmp], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

f = open(sys.argv[2], "wb")
e = zlib.compressobj(9)
c = 0
b = ""

opusenc.initialize(256000)

wf = wave.open(tmp)
while True:
	rc = wf.readframes(480)
	if len(rc) != 1920:
		break
	
	opus = opusenc.encode(rc)
	b += base64.b64encode(opus).decode("utf-8") + "\n"
	c += 1
	if c >= 100:
		c = 0
		f.write(e.compress(b.encode()) + e.flush(zlib.Z_SYNC_FLUSH))
		b = ""

f.write(e.compress(b.encode()) + e.flush(zlib.Z_SYNC_FLUSH))
f.close()
wf.close()
os.remove(tmp)
