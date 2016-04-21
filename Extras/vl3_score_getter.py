#!/usr/bin/env python

#import modules
import os
import csv
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from collections import OrderedDict
import glob

#input is a fasta file with all of your files
arg1 = sys.argv[1]

#file to deal with ambiguous characters
tempFasta = 'tempFasta.txt'
tempScore = 'tempScore.txt'

#fasta parser, returns name and seq
def read_fasta(arg):
    name, seq = None, []
    for line in arg:
        line = line.rstrip()
        if line.startswith('>'):
            line = line.split('>')
            line = line[1]
            if name: yield(name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield(name,''.join(seq))

#reads fasta, sets it up for input into Disprot, filters out those file less than 125 amino acids
def fasta_format(fasta):
	#reads in fasta file
	with open(fasta, 'r') as fasta:
		with open(tempFasta, 'w') as tempOut:
			for name, seq in read_fasta(fasta):
				if len(seq) < 125:
					print("Sequence less than 125 residues, deleting: " + name)
				else:
					if 'X' in seq:
						tempOut.write('>' + name + '\n')
						seq = seq.split('X')
						seq = ''.join(seq)
						tempOut.write(seq + '\n')
					else:
						tempOut.write('>' + name + '\n')
						tempOut.write(seq + '\n')

#takes vl3 scores and returns a dictionary
def score_pull(tempScores):
	scoreDict = OrderedDict()
	with open(tempScores, 'r') as scores:
		for line in scores:
			line = line.rstrip('\n')
			if line[0].isdigit():
				line = line.split(' ')
				aaPosition = int(line[0])
				score = float(line[2])
				if aaPosition >= 126:
					pass
				else:
					scoreDict.update({aaPosition:score})
			else:
				name = line
	#os.remove(tempScores)
	return scoreDict, name

def get_vl3(fasta):
	#sets up proper fasta file
	fasta_format(fasta)

	#defining a number for the counter that fixes 'Rate Limit Exceeded' error on Disprot webpage
	num = 1

	#portion of code that generates VL3 data. The time.sleep() commands are crucial to avoid 'Rate Limit Exceeded' errors
	
	with open(tempFasta, 'r') as fastafile:
		try:
			dictAll = OrderedDict()
			for name, seq in read_fasta(fastafile):
				#dummy title for disprot
				place_holder = "Place_Holder_Title"
				#this is a gate to not overwhelm the VL3 server to quickly with sequences.
				#after 4 sequences are run the script pauses for 2.3s and the counter resets.
				if num == 5:
					num = num - 4
					time.sleep(5)
				
				#builds sequence to be put into Disprot with a dummy title for Disprot
				sequence = ">" + place_holder + "\n" + seq
				#opens web browser for Chrome (see requirements above)
				driver = webdriver.Chrome('/Users/ryan/Desktop/IDP_Paper/Scripts_stdout/Scripts/chromedriver')
				#navigates to the disprot website
				driver.get('http://www.disprot.org/metapredictor.php')
				time.sleep(3)
				#unchecks the VSL2 and VLXT predictor checkboxes, leaving only VL3 predictor selected
				checkbox = driver.find_element_by_xpath("//input[@name='VSL2']")
				checkbox.click()
				time.sleep(1)
				checkbox = driver.find_element_by_xpath("//input[@name='VLXT']")
				checkbox.click()
				time.sleep(1.5)
				#puts fasta file into text box on disprot website
				elem = driver.find_element_by_name('native_sequence')
				elem.send_keys(sequence)
				time.sleep(2)
				#submits to Disprot
				submit = driver.find_element_by_xpath("//input[@type='submit']")
				submit.click()
				time.sleep(3)
				#click link to get only the VL3 data
				VL3_Data = driver.find_element_by_link_text('VSL3 DATA')
				VL3_Data.click()
				time.sleep(4)
				#gets the data from website
				data = driver.find_element_by_xpath("html").text

				driver.quit()

				#sets up the name for the file
				a, b, c, d, e = name.split('|')

				#sets up the file path and name of the file with proper extension
				filename = str(d) + '.txt'

				#writes the VL3 data to a file
				with open (tempScore, 'w') as out:
					out.write(str(d) + '\n' + data)
				intermediary = 'temp_scores/%s.txt' % (str(d))
				with open (intermediary, 'w') as intermediate:
					intermediate.write(str(d) + '\n' + data)
				num = num + 1

				#extracts the scores and then puts them into a dictionary
				allSamples, n = score_pull(tempScore)
				allSamples = dict(allSamples)
				dictAll.update({str(d):allSamples})

		except Exception as fail:
			try:
				driver.quit()
			except:
				pass
			print("Unable to complete.")
			sys.exit(fail)

		try:
			os.remove(tempFasta)
		except:
			pass
	return dictAll

#run if you have to get scores
def main():
	finalDict = get_vl3(arg1)
	
	with open('training_vl3_scores.txt', 'w') as finalout:
		for item in finalDict:
			scores = ','.join(['%s' % (value) for (key, value) in finalDict[item].iteritems()])
			finalout.write("%s,%s\n" % (item, scores))
	
#run if you already have each score in individual file from get_vl3
#######in score_pull() you must comment out the os.remove(tempScores line)
def main2():
	dirs = glob.glob("/Users/ryan/Desktop/Machine Learning/Classifier/temp_scores/*.txt")
	
	dictAll = OrderedDict()
	for filename in dirs:
		allSamples, name = score_pull(filename)
		allSamples = dict(allSamples)
		dictAll.update({name:allSamples})
	print(dictAll)
	with open('training_vl3_scores_final.txt', 'w') as finalout:
		for item in dictAll:
			scores = ','.join(['%s' % (value) for (key, value) in dictAll[item].iteritems()])
			finalout.write("%s,%s\n" % (item, scores))

main2()

print("Done")
