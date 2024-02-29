import sys

def edit_jpeg_dimensions(filedata):
	idx = filedata.find(b'\xff\xc0')
	
	if idx < 0:
		print('0xFF 0xC0 not found. Quitting...', file=sys.stderr)
		sys.exit(-1)

	height_b = filedata[idx+5:idx+7]
	height_i = int(height_b[0])*256 + int(height_b[1])
	print(f'OHB: {height_b}')
	print(f'OHI: {height_i}')

	width_b = filedata[idx+7:idx+9]
	width_i = int(width_b[0])*256 + int(width_b[1])

	new_height_i = height_i * 2
	new_width_i = width_i * 2
	print(f'NHI: {new_height_i}')

	print(hex(new_height_i))
	new_height_b = bytes.fromhex(f'{str(hex(new_height_i))[2:]}')
	new_width_b = bytes.fromhex(f'{str(hex(new_width_i))[2:]}')
	print(f'NHB: {new_height_b}')

	nn_height_i = int(new_height_b[0])*256 + int(new_height_b[1])
	print(nn_height_i)


	new_file = filedata[:idx+5] + new_height_b + new_width_b + filedata[idx+9:]

	print(filedata[idx+5:idx+9])
	print(new_height_b + new_width_b)
	print(len(new_file))
	print(len(filedata))
	return new_file

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('Enter file name as argument. Quitting...', file=sys.stderr)
		sys.exit(-1)

	filename = sys.argv[1]

	with open(filename, 'rb') as f:
		filedata = f.read()

	new_file = edit_jpeg_dimensions(filedata)

	with open('edited.jpg', 'wb') as f:
		f.write(new_file)
