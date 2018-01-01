#!/usr/bin/env python
# makes a probabilistic context free grammar 
# from the preprocessed trees in train.trees.pre.unk
#

import argparse
import sys
import codecs
if sys.version_info[0] == 2:
	from itertools import izip
else:
	izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
	if type(fh) is str:
		fh = open(fh, code)
	ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
	if sys.version_info[0] == 2:
		if code.startswith('r'):
			ret = reader(fh)
		elif code.startswith('w'):
			ret = writer(fh)
		else:
			sys.stderr.write("I didn't understand code "+code+"\n")
			sys.exit(1)
	return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
	''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
	group = parser.add_mutually_exclusive_group()
	dest = arg if dest is None else dest
	group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
	group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)

def main():
	parser = argparse.ArgumentParser(description="ignore input; make a demo grammar that is compliant in form",
																	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	addonoffarg(parser, 'debug', help="debug mode", default=False)
	parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file (ignored)")
	parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file (grammar)")

	try:
		args = parser.parse_args()
	except IOError as msg:
		parser.error(str(msg))

	"""
	#workdir = tempfile.mkdtemp(prefix=os.path.basename(__file__), dir=os.getenv('TMPDIR', '/tmp'))

	def cleanwork():
		shutil.rmtree(workdir, ignore_errors=True)
	if args.debug:
		print(workdir)
	else:
		atexit.register(cleanwork)
	"""
	
	infile = prepfile(args.infile, 'r')
	outfile = prepfile(args.outfile, 'w')

	# S is a list of all trees read from train.trees.pre.unk
	S = []
	for line in infile:
		S.append(line);
	
	from nltk import Tree
	from collections import defaultdict
	D = defaultdict(int)
	d = defaultdict(int)

	# for all trees in S
	for tree in range(0,len(S)):
			
			t = Tree.fromstring(S[tree])
			# length stores no of productions in each tree
			length = len(t.productions())
			
			# for each production in t
			for i in range(0,length):
					rule = str(t.productions()[i])
					#D stores count of each distinct rule
					D[rule]+=1
					#d stores count of unique heads of rules
					d[rule.split()[0]]+=1

	#used to find the rule with max frequency 
	W = []
	for w in sorted(D, key=D.get, reverse=True):
			W.append([w,D.get(w)])
	#Rule with max frequency 
	#print(W[0]) 

	# stores a list of all distinct rules with their frequencies
	W_new = []
	for w in D:
			W_new.append([w,D.get(w)])

	import math
	# stores a list of all rules and their probabilities     
	H = []
	# for each distinct rule
	for w in W_new:
			r=d.get(w[0].split()[0])
			H.append([w[0], round((float(D.get(w[0]))/r),7)])

	# stores the grammar rules along with their probabilities
	cfg = []
	for i in H:
			rule = str(i[0].replace('\'','')+" # "+str(i[1]))
			#print(rule)
			cfg.append(rule)

	for i in cfg:
		outfile.write(i)
		outfile.write('\n')

if __name__ == '__main__':
	main()