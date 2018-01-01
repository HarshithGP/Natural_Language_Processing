# CKY Syntax Parser using Probabilistic Context Free Grammar

Project description
- Developed a parser for building the syntax tree of english sentences using the CKY algorithm.
- The syntax tree helps in performing syntactic analysis which serves as the first step towards full semantic analysis and information extraction. 
- The probabilistic context free grammar was generated from the ATIS portion of the PENN Treebank and the probablities for the rules were determined using the principles of maximum likelihood estimation. Used log probabilities to prevent underflow. 
- Preprocessed the trees in the development set to ensure strict binarization and merged unary nodes. Replaced rare/infrequent words having a frequency less than 2 with <unk>. 
- Tested the parser on a hidden test set of sentences and achieved the following metrics
Accuracy : 91.35 Recall : 75.74 F1 Score : 82.81
- Implemented parent annotation, head lexicalization, stemming and (beaming) to enhance the F1 score to 84.67
