python main.py -e data/twitter_dev.ner data/twitter_dev_test.ner 
python main.py -T crf -e data/twitter_dev.ner data/twitter_dev_test.ner data/twitter_test.ner


perl data/conlleval.pl -d \t < twitter_dev.ner.pred
perl data/conlleval.pl -d \t < twitter_dev_test.ner.pred