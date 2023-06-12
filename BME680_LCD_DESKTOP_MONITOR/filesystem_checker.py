import os
import uos
import micropython
statinfo = os.stat("data.txt")[6]
print("filesize of text file = ",statinfo)
blocksize = uos.statvfs("/")[1]
totalblocks = uos.statvfs("/")[2]
freeblocks = uos.statvfs("/")[3]

free_space = ((freeblocks*blocksize) /1024)

used_space = ((totalblocks*blocksize)/1024)

total_space = (used_space - free_space)

print("freespace = ", (free_space),"kb")
print("used space = ", (used_space),"kb")
print("total space = ", (total_space),"kb")






