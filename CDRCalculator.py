###
# Author: Jason Turnbull 
# Version: 1.0
# Date: August 27 2013
###

import sys

def addCD (baseNumStr, CDR): 
	"""Calculate and append a Check Digit for the given base Number and return the new Reference Number as a String."""
	## FirstUp, turn our baseNumStr into a Number. (We take it as a string in case it has leading zeros)
	baseNum = int(baseNumStr) 
	
	cdrRules = {'mod10v01':{'weights': [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
							'startLeft': False, 
							'divideBy': 10, 
							'subtractFrom': 10, 
							'addDigits': 'Y',  #'Y','N','T','R' 
							'keepZero': True, 
							'length': 1},
				'mod11v13A':{'weights': [21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2],
							'startLeft': False, 
							'divideBy': 11, 
							'subtractFrom': 11, 
							'addDigits': 'N',  #'Y','N','T','R' 
							'keepZero': True, 
							'length': 2},
				'mod97v02':{'weights': [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,2,1,4,3],
							'startLeft': False, 
							'divideBy': 97, 
							'subtractFrom': 97, 
							'addDigits': 'N',  #'Y','N','T','R' 
							'keepZero': False, 
							'length': 2}
				}

	baseArr = [int(digit) for digit in str(baseNum)] ## Turn my number into an array to play with. 
	checksum = 0

	if not(cdrRules.has_key(CDR)):
		## If we don't know the rules for this CDR we can't do the math
		return False;

	else: 
		## Check if we start weighting from the left-most or right-most digit?
		if not(cdrRules[CDR]['startLeft']):
			## We need to spin the arrays to start from the right... 
			baseArr.reverse()
			cdrRules[CDR]['weights'].reverse()
		
		## Now loop through both arrays to the length of the base number
		for j in range(0,len(baseArr)):
			weightVal = baseArr[j] * cdrRules[CDR]['weights'][j]
			if (len(str(weightVal)) > 1 and cdrRules[CDR]['addDigits'] != 'N'):
				if cdrRules[CDR]['addDigits'] == 'Y':
				## we need to do some math
					weightVal = int(str(weightVal)[-1]) + int(str(weightVal)[-2])
				elif cdrRules[CDR]['addDigits'] == 'T':
				## just truncating... get the right-most value
					weightVal = int(str(weightVal)[-1])
				elif cdrRules[CDR]['addDigits'] == 'R':
				## We need to sum the digits til we get a single digit answer
					while (len(str(weightVal)) > 1):
						newWeightVal = 0 
						for digit in str(weightVal):
							newWeightVal += digit
						weightVal = newWeightVal
						
			## Now add our weighted value to our checksum	
			checksum += weightVal
		## Now we get the modulo of or checksum and divisor:
		checkDigit = checksum % cdrRules[CDR]['divideBy']
		
		## Manage the rules around zeros etc.
		if ((checkDigit != 0 or not(cdrRules[CDR]['keepZero'])) and (cdrRules[CDR]['subtractFrom'] > 0)):
			checkDigit = cdrRules[CDR]['subtractFrom'] - checkDigit
			
		if (len(str(checkDigit)) > 1 and cdrRules[CDR]['length'] == 1):
			## Need to do some switching out... this aplies to mod 11 only
			#if (CRD[-1] == 'A'):  ## Do nothing for A
			if (CDR[-1] == 'B' and checkDigit == 11): 
				checkDigit = 0
			elif (CDR[-1] == 'C' and checkDigit == 11):
				checkDigit = 1
			elif (CDR[-1] == 'D' and checkDigit == 10):
				checkDigit = 0				
			
		elif (len(str(checkDigit)) ==1 and cdrRules[CDR]['length'] == 2): 
			checkDigit = '0' + str(checkDigit)
	
	## finally add our checkDigit to our base number and return the result: 				
	return baseNumStr + str(checkDigit)
