#!/usr/bin/env python
#Author : Kristopher Landon
#Release : Vertica Load Tester Beta
#Release # : 0.0.1
#Date : 12/10/2013
#License : Not for public release 


import sys
import codecs

class FileProcessor(object):

	def __init__(self):
		self.qTotal = 0
		self.qRejected = 0
		self.qAccepted = 0
		#self._TestVar = 'This is a Test'

	# @property
	# def qTotal(self):
	# 	return self._qTotal

	# @qTotal.setter
	# def qTotal(self,value):
	# 	self._qTotal = value

	# @property
	# def qRejected(self):
	# 	return self._qRejected

	# @qRejected.setter
	# def qRejected(self,value):
	# 	self._qRejected = value

	# @property
	# def qAccepted(self):
	# 	return self._qAccepted

	# @qAccepted.setter
	# def qAccepted(self,value):
	# 	self._qAccepted = value

	# #Queries Accepted
	# self.qAccepted = 0
	# #Queries Rejected
	# self.qRejected = 0
	# #Create Script Objects

	def ParseFile(self,fileIn):
		#Holder for script items
		sqlScripts = []
		try:
			#Holder for lines to build SQL Statement
			scriptBuilder = ''
			#Open the file for parsing
			f = codecs.open(fileIn,'r','utf8')
			#enumerate the file so we can inspect line by line
			for idx,line in enumerate(f):
				if ';' not in line:
					#scriptBuilder = scriptBuilder + ' ' + str(line).replace('\n',' ')
					scriptBuilder = scriptBuilder + ' ' + str(self.CleanString(line))
				elif ';' in line:
					scriptBuilder = scriptBuilder + str(self.CleanString(line))
					sqlScripts.append(self.RemoveWhiteSpace(scriptBuilder))
					scriptBuilder = ''
				elif idx == max(f):
					sqlScripts.append(self.RemoveWhiteSpace(scriptBuilder))
		except:
			ex = sys.exc_info()
			print ("Unexpected error occured " + str(ex))
		return sqlScripts

	#Check UTFS Encoding
	def CheckFileFormat(self,fileIn):
		#return value of accepted
		isAccepted = 0
		#Set only accepted encoding
		acceptedEncoding = 'utf-8'
		#Test file properties
		try:
			#open File
			testFile = codecs.open(fileIn,'r',acceptedEncoding)
			#quicktest of encoding
			testFile.readlines()
			testFile.seek(0)
		except:
			isAccepted = 0
		else:
			isAccepted = 1
		return isAccepted
	#Clean CR LF 
	def CleanString(self,toBeCleaned):
		toBeCleaned = toBeCleaned.replace('\r\n',' ')
		toBeCleaned = toBeCleaned.replace('\r',' ')
		toBeCleaned = toBeCleaned.replace('\n',' ')
		return toBeCleaned
	#Remove Leading and Trailing Whitespace
	def RemoveWhiteSpace(self,noWhite):
		noWhite = str(str(noWhite).lstrip()).strip()
		return noWhite
	#Check for safe queries
	def CheckSafeQueries(self,checkList):
		#Set Total
		self.qTotal = len(checkList)
		#Scrub Queries
		for idx,item in enumerate(checkList):
			if 'delete' in item:
				checkList.pop(idx)
			elif 'create' in item:
				checkList.pop(idx)
			elif 'drop' in item:
				checkList.pop(idx)
				checkList.pop(idx)
			elif 'alter' in item:
				checkList.pop(idx)
		self.qAccepted = len(checkList)
		self.qRejected = self.qTotal - self.qAccepted
		return checkList


		











