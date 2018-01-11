#coding=UTF-8
import io
import os
import struct

def decryptPNG(infilename,filename):
	outfilename = "E:\\crackme\\血族\\out\\png" + os.sep + filename
	with open(infilename,'rb') as pngfile:
		data = pngfile.read()
		pngfile.close()
	with open(outfilename,"wb") as outpng:
		head1 = struct.pack('BB',0x89,0x50)
		outpng.write(head1)
		outpng.write(data[0x2:0x10])
		#outpng.write(data[0x10:])
		L10 = data[0x10] ^ 0x50
		L11 = data[0x11] ^ 0x51
		L12 = data[0x12] ^ 0x52
		L13 = data[0x13] ^ 0x53
		L14 = data[0x14] ^ 0x54
		L15 = data[0x15] ^ 0x55
		L16 = data[0x16] ^ 0x56
		L17 = data[0x17] ^ 0x57
		L18 = data[0x18]
		L19 = data[0x19] ^ 0x57
		L1a = data[0x1a] ^ 0x56
		L1b = data[0x1b] ^ 0x55
		L1c = data[0x1c] ^ 0x54
		L1d = data[0x1d] ^ 0x53
		L1e = data[0x1e] ^ 0x52
		L1f = data[0x1f] ^ 0x51
		L20 = data[0x20] ^ 0x50
		head2 = struct.pack('BBBBBBBBBBBBBBBBB',L20,L1f,L1e,L1d,L1c,L1b,L1a,L19,L18,L17,L16,L15,L14,L13,L12,L11,L10)
		outpng.write(head2)
		outpng.write(data[0x21:])
		outpng.close()

		
def decryptJPG(infilename,filename):
	outfilename = "E:\\crackme\\血族\\out\\jpg" + os.sep + filename
	size = os.path.getsize(infilename)
	with open(infilename,'rb') as jpgfile:
		data = jpgfile.read()
		jpgfile.close()
	with open(outfilename,'wb') as outjpg:
		head1 = struct.pack('BB',0xff,0xd8)
		for i in range(2,size):
			if data[i] == 0xff:
				if data[i+1] == 0xc0:
					start = i+4
					end = start + 0xf
					#print("start: ",hex(start))
					L0 = data[start] ^ 0x4a
					L1 = data[start+1] ^ 0x4b
					L2 = data[start+2] ^ 0x4c
					L3 = data[start+3] ^ 0x4d
					L4 = data[start+4] ^ 0x4e
					L5 = data[start+5] ^ 0x4f
					L6 = data[start+6] ^ 0x50
					L7 = data[start+7]
					L8 = data[start+8] ^ 0x50
					L9 = data[start+9] ^ 0x4f
					La = data[start+0xa] ^ 0x4e
					Lb = data[start+0xb] ^ 0x4d
					Lc = data[start+0xc] ^ 0x4c
					Ld = data[start+0xd] ^ 0x4b
					Le = data[start+0xe] ^ 0x4a
					head2 = struct.pack('BBBBBBBBBBBBBBB',Le,Ld,Lc,Lb,La,L9,L8,L7,L6,L5,L4,L3,L2,L1,L0)
					outjpg.write(head1)
					outjpg.write(data[2:start])
					outjpg.write(head2)
					outjpg.write(data[end:])
					break;
		outjpg.close()
					
def decryptTXT(infilename,filename,dir):
	outfilename = "E:\\crackme\\血族\\out\\" + dir + os.sep + filename
	size = os.path.getsize(infilename)
	with open(infilename,'rb') as txtfile:
		data = txtfile.read()
		txtfile.close()
	if data[size-2] != 0x47:
		return
	if data[size-3] != 0x44:
		return
	if data[size-4] != 0x53:
		return
	size = size -5
	zh = (size+1)//2
	ha = (size+1)%2
	
	if ha:
		with open(outfilename,'wb') as txtfile:
			for i in range(size):
				if i < zh:
					ch = data[size - i] ^ (0x54 + i)%0xff
				elif i == zh:
					ch = data[size-i]
				else:
					ch = data[size - i] ^ (0x54 + size -i)%0xff
				ch1 = struct.pack('B',ch)
				txtfile.write(ch1)
			txtfile.close()
	else:
		with open(outfilename,'wb') as txtfile:
			for i in range(size):
				if i < zh:
					ch = data[size - i] ^ (0x54 + i)%0xff
				else:
					ch = data[size - i] ^ (0x54 + size -i)%0xff
				ch1 = struct.pack('B',ch)
				txtfile.write(ch1)
			txtfile.close()
			
	
		
if __name__ == '__main__':

	filedir = "E:\\crackme\\血族\\xuezu\\assets"
	pngnum = 0
	jpgnum = 0
	luanum = 0
	csvnum = 0
	xmlnum = 0
	for path,subdirs,files in os.walk(filedir):
		for filename in files:
			if filename.endswith('.png'):
				pngnum += 1
				infilename = path + os.sep + filename
				decryptPNG(infilename,filename)
				print(filename + "已被修复")
			elif filename.endswith('.jpg'):
				jpgnum += 1
				infilename = path + os.sep + filename
				decryptJPG(infilename,filename)
				print(filename + "已被修复")
			elif filename.endswith('.lua'):
				luanum += 1
				infilename = path + os.sep + filename
				decryptTXT(infilename,filename,'lua')
				print(filename + "已被修复")
			elif filename.endswith('.csv'):
				csvnum += 1
				infilename = path + os.sep + filename
				decryptTXT(infilename,filename,'csv')
				print(filename + "已被修复")
			elif filename.endswith('.xml'):
				xmlnum += 1
				infilename = path + os.sep + filename
				decryptTXT(infilename,filename,'xml')
				print(filename + "已被修复")
	
	print("[**************************************]")
	print("")
	print("           png num : ",pngnum)
	print("           jpg num : ",jpgnum)
	print("           lua num : ",luanum)
	print("           csv num : ",csvnum)
	print("           xml num : ",xmlnum)
	print("")
	print("[**************************************]")
