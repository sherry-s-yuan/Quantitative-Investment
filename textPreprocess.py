# clean noisy string
import re

# clear URLs https:\\example.com
def clear_URL(string):
	new_string = ''
	for word in string.split():
		if not "https" in word:
			new_string += word + ' '
	return new_string.rstrip()

# clear Emails example@example.com
def clear_email(string):
	new_string = ''
	for word in string.split():
		if not (".com" in word and "@" in word):
			new_string += word + ' '
	return new_string.rstrip()

# clear \n
def clear_return(string):
	no_return_string = ''
	text = re.findall('(.*)\n(.*)', string)
	# if no \n found, then return string, else get rid of \n
	if len(text) == 0:
		return string
	for i in range(len(text)):
		left = ''
		right = ''
		# if the strip string have length 0
		if not len(text[i][0]) == 0:
			left = text[i][0].lstrip().rstrip() + ' '
		if not len(text[i][1]) == 0:
			right = text[i][1].lstrip().rstrip() + ' '
		no_return_string += left + right
	return no_return_string.strip()

# clear up unecessary characters
def clear(string):
	clear_string = ''
	for i in string:
		if (ord(i) >= ord('a') and ord(i) <= ord('z')) or (ord(i) >= ord('0') and ord(i) <= ord('9')) or (ord(i) == ord(' ')) or ord(i) == ord('%') or (ord(i) == ord('.')) or (ord(i) == ord('$')) or (ord(i) == ord('#')) or (ord(i) == ord(':')):
			clear_string += i
	return clear_string

# main method 
def preprocess(string):
	return clear(clear_email(clear_URL(clear_return(string.lower()))))

## tests
#string = '$ALYI Announces $1 Million Order For ReVolt Electric Motorcycles https:\/\/t.co\/Sswta1o7Yh #ElectricVehicles $HPIL $NSAV $MSPC $BIOAQ #VAPE $CELZ $NNRX $AAGC $TGGI $AAPL $TSLA $WH $UOIP $PNAT $DIRV $SODE $MSFT $AIMH $RSHN $NNSR $AMZN $ANDI $FUSZ $FRFS $RBIZ $SRMX $PSNX $RBIZ $SBFM https:\/\/t.co\/LdvydX517Z'
##print('Length of String', len(string))

#print('result', preprocess(string))


