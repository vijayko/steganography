#This is a Python 3 program of a variant of Steganography where we conceal text data in an image. 

'''
This is a simple demonstration of hiding text message in an image without much changing the pixel values. 
In this program, we simply use the fact that an image will not get modified if we change the decimal pixel value by 1
which is simply changing the last bit of the binary equivalent of the pixel. 
Algorithm outlined: 

1. We first convert a text's ASCII decimal value to 8 bit binary 
2. Then, we iterate over every 9 pixel values at each iteration. To note, we are using RGB encoded images. 
Therefore, we use 3 subsequent tuples each having 3 values for R, G, and B. Thus, we have 9 decimal numbers 
at hand to encode 8-bit information. We modify the first 8 numbers and use the 9th number to mark the end of the data. 
2.1 if there is no more data to be encoded: we change 9th number to odd (if the 9th number is odd). 
	else: we make it even (if the 9th number is odd)
3. 8-bit of each character is encoded in the pixel values as follow: 
	3.1 for each bit in 8-bit binary: 
			if (bit == '0') and pixel value odd: we convert pixel value to odd. 
			elif (bit == '1') and pixel value even: we convert pixel value to odd. 
4. in order to decode, we simply reverse the process to extract the encoded bits, and convert them to string 
'''

from PIL import Image 
import argparse 

#converting text data into binary 

def text_to_bin(string_data):
	bin_data = [] #this list holds the binary equivalent of the text 

	for i in string_data:
		bin_data.append(format(ord(i), '08b')) #converting a character to it 8-bit binary
	return bin_data


#This function modifies the pixels of an image 
#We use a simple rule to modify the pixels
# - Since each character is converted to an 8 bit binary, we modify each number is a pixel according to the bits 
# - a pixel is changed to odd if the bit is '1'; a pixel to even if the bit is '0'

#generator function to modify the pixels as per the binary data 
def pixel_modification(pixel, data):
	binary_data = text_to_bin(data)
	data_length = len(binary_data)
	image_data = iter(pixel) #making an array (pixel) iterable 

	for i in range(data_length):
		#iterating over 3 pixels per iteration 
		pixel = [val for val in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

		#iterating over each binary equivalent data of text 
		for j in range(0, 8):
			#converting odd to even for bit '0'
			if (binary_data[i][j] == '0') and (pixel[j] % 2 != 0):
				pixel[j] -= 1

			#converting even to odd for bit '1'
			elif (binary_data[i][j] == '1') and (pixel[j] % 2 == 0):
				pixel[j] -= 1


		#This section is to mark the end of the data 
		# if there is more data to encode, we convert the 9th bit as 

		if (i == data_length -1):
			#if even at the end of the data, we make it odd
			if (pixel[-1] % 2 == 0):
				pixel[-1] -= 1

		else: 
			#if odd and the data has not ended, we make it even to keep going on. 
			if (pixel[-1] % 2 != 0):
				pixel[-1] -= 1

		pixel = tuple(pixel)
		yield pixel[0:3] #first 3 values of the pixel
		yield pixel[3:6] #the next 3 values
		yield pixel[6:9] # the other next subsequent values of pixel 

#this function is essentially to make use of the generator and encode the data to form a new image
def encoding_data(image, data):
	l = image.size[0] #this is the width of the image 

	(i, j) = (0, 0) #starting point 

	#using the generator to get pixels and assembling them to form a new image. 
	for p in pixel_modification(image.getdata(), data):
		# using putpixel method on the object image instantiated using Image class in PIL library
		image.putpixel((i, j), p)

		#when we reach the end of the width, we simply set the horizontal iterator to 0 and vertical is increased by 1
		if (i == l - 1):
			i = 0
			j += 1
		else: 
			i += 1

#putting everything together encode the data 
def encode(img, new_image_name):
	image = Image.open(img, 'r')

	data = input("Data to encode: ")
	if (len(data) == 0):
		raise ValueError('empty data')

	new_image = image.copy()
	encoding_data(new_image, data)

	new_image.save(new_image_name, str(new_image_name).split(".")[1].upper())

#In the decode section, we essentially reverse the process we performed in encode till we find
#the point where we marked the end of the data with by changing the 9th bit to odd. 
def decode(name):
	
	image = Image.open(name, 'r')

	data = ''
	image_data = iter(image.getdata())

	while (True):
		pixel = [val for val in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

		ans = ''

		for i in pixel[:8]:
			if (i % 2 == 0):
				ans += '0'
			else: 
				ans += '1'

		data += chr(int(ans, 2))
		#This conditional is to wait for the 9th bit that has marked the end of the encoding of the data. 
		if (pixel[-1] % 2 != 0):
			return data


'''
In order to pass the arguments, users will have to use these flags: 
-e <image name with extension to be encoded with message> 
-n <image name with extension with the encoded message>
-d <image to be decoded>


encoding command
>>> python3 -e mona.png -n secret.png 

Users will be prompted to write the message to be encoded. 

decoding command 
>>> python3 -d secret.png 

'''

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-e", "--enc_image", help="use this command to pass image name to be encoded")
	parser.add_argument("-d", "--dec_image", help="use this command to pass image name to be decoded")
	parser.add_argument("-n", "--new_image", help="use this command to pass image name that will have encoded data")
	args = parser.parse_args()
	if args.enc_image != None: 
		encode(args.enc_image, args.new_image)

	elif args.dec_image != None:
		print("Decoded message: " + decode(args.dec_image))

	else: 
		raise Exception("Invalid input. Try again!")


