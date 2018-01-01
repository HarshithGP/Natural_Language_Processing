
import distsim

#word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
word_to_vec_dict = distsim.load_word2vec("glove.6B.50d.txt")
#word_to_ccdict = distsim.load_contexts("nytcounts.4k")
L = []
relation = []
group = 0
with open('word-test.v3.txt',"r") as f_in:
#with open('word-test.v3.txt',"r") as f_in:
	 for line in f_in:
		 if line[0]==':':
			 group+=1
			 L.append([group, line])
			 relation.append(line.strip('\n').replace(':',''))
		 else:
			 L.append([group,line])

Accuracy_Best1 = []
Accuracy_Best5 = []
Accuracy_Best10 = []

for g in range(1,9):   
	analogy = []
	for i in range(0,len(L)):       
		if L[i][0]==g and len(L[i][1].split()) == 4:
		   analogy.append(L[i][1].split())
	   
	best1=best5=best10=0  
   
	for a in range(0,len(analogy)):

		first = word_to_vec_dict[analogy[a][0]]
		second = word_to_vec_dict[analogy[a][1]]
		fourth = word_to_vec_dict[analogy[a][3]]
			
		ret = distsim.show_nearest(word_to_vec_dict,first-second+fourth,set([analogy[a][0],analogy[a][1],analogy[a][3]]),distsim.cossim_dense)
		#ret = distsim.show_nearest(word_to_ccdict,z,set([ analogy[a][0], analogy[a][1], analogy[a][3] ]),distsim.cossim_sparse)
	   
		if analogy[a][2] == ret[0][0]:
			best1+=1
		if analogy[a][2] in [w[0] for w in ret[0:5]]:
			best5+=1
		if analogy[a][2] in [w[0] for w in ret[0:10]]:
			best10+=1
		
		"""
		print("---------------------------------------------------------------------------------------")
		for i in range(0,len(ret)):
			print(analogy[a][0]+" : "+analogy[a][1]+" :: "+ret[i][0]+" : "+analogy[a][3])
		print("---------------------------------------------------------------------------------------")
		"""

	Accuracy_Best1.append(round(float(best1)/len(analogy),3))
	Accuracy_Best5.append(round(float(best5)/len(analogy),3))
	Accuracy_Best10.append(round(float(best10)/len(analogy),3))





print("Group \t\t\t"+"Best-1 Acc \t"+"Best-5 Acc \t"+"Best-10 Acc \t")
for g in range(1,group+1):
	#print(str(relation[g-1])+"\t"+Accuracy_Best1[g-1]+"\t\t"+Accuracy_Best5[g-1]+"\t\t"+Accuracy_Best10[g-1])  
	print '{:25s} {:4.3f} \t {:4.3f} \t\t {:4.3f}'.format(str(relation[g-1]), Accuracy_Best1[g-1], Accuracy_Best5[g-1], Accuracy_Best10[g-1])
