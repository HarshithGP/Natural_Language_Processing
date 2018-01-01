#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
import re
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
#nltk.download('wordnet')
kTOKENIZER = TreebankWordTokenizer()
#nltk.download('stopwords')
#nltk.download('cmudict')
from nltk.corpus import stopwords
	
def morphy_stem(word):
	 #Simple stemmer
	stem = wn.morphy(word)
	if stem:
		return stem.lower()
	else:
		return word.lower()

from nltk.stem.porter import PorterStemmer
def porter_stem(word):
	# Porter stemmer#
	ps = PorterStemmer()
	return ps.stem(word).lower()

from nltk.stem.snowball import SnowballStemmer
def snowball_stem(word):
	"""Snowball Stemmer"""
	ss = SnowballStemmer("english", ignore_stopwords=True)
	return ss.stem(word).lower()

import pandas as pd
dataset = pd.read_csv('train.tsv', delimiter = '\t', quoting = 3)


#shakespeare : 0-1854
#Bronte 1855 - 3665
def get_words(start,end):
	S = []
	for i in range(start,end):
		line = dataset['text'][i].lower()
		line = re.sub('[^a-zA-Z\']',' ',line)
		line = line.split()
		for word in line:
			if word not in set(stopwords.words('english')):
				S.append(word)
	return S

def build_D(S):
	D = defaultdict(int)
	for word in S:
		word = snowball_stem(word)
		D[word] += 1
	return D

def word_list(D):
	W = []
	poet_words = []
	for w in sorted(D, key=D.get, reverse=True):
		if D.get(w)>=3:
			W.append([w,D.get(w)])
			poet_words.append(w)
	return poet_words, W

#S_words, S = word_list(build_D(get_words(0,1854)))
#B_words, B = word_list(build_D(get_words(1855,3665)))
#common = list(set(S_words).intersection(B_words)) 	 


from nltk.util import ngrams
from collections import Counter
class FeatureExtractor:
	def __init__(self):
		"""
		You may want to add code here
		"""
		

		None
	
	def features(self, text):
		
		d = defaultdict(int)
		text = re.sub('[^a-zA-Z]',' ',text)
		#d['Upper_Case']=sum(1 for c in text if c.isupper())
		text=text.lower()
		d['No_Of_Words']=len(text.split())
		#d['Upper_Case']=sum(1 for c in text if c.isupper())
		#d['Punctuation_Marks']=sum(1 for c in text if c in ['.' , ',' , ';' ,'\'', '!', '?', ':'])
		#unigram = ngrams(text.split(), n=1)

		bigrams = ngrams(text.split(), n=2)
		#trigrams = ngrams(text.split(), n=3)
		#d['unigrams'] = len(Counter(unigram))
		d['bigrams'] = len(Counter(bigrams))
		#d['trigrams'] = len(Counter(trigrams))

		#<3
		Low_Freq = ['abhor', 'contract', 'herald', 'glutton', 'tatter', 'lusti', 'success', 'beguil', 'womb', 'husbandri', 'cupid', 'usur', 'accept', 'hideous', 'sap', 'frost', 'defac', 'depart', 'poster', 'lift', 'homag', 'serv', 'ador', 'attend', 'pilgrimag', 'pitch', 'feebl', 'fore', 'convert', 'unlook', 'receivest', 'servic', 'speechless', 'unthrift', 'shift', 'kept', 'chief', 'lodg', 'growest', 'folli', 'harsh', 'seal', 'sunk', 'canopi', 'defenc', 'breed', 'prepar', 'dearth', 'stage', 'secret', 'height', 'decreas', 'sulli', 'wherefor', 'fortifi', 'top', 'counterfeit', 'pencil', 'paper', 'aliv', 'whate', 'forbid', 'allow', 'pattern', 'master', 'fashion', 'addit', 'sell', 'elder', 'nurs', 'babe', 'anew', 'replet', 'rite', 'presag', 'twenti', 'bestow', 'aspect', 'expir', 'abid', 'sightless', 'quiet', 'benefit', 'swart', 'sparkl', 'lark', 'aris', 'hid', 'dateless', 'cancel', 'expens', 'heavili', 'obsequi', 'interest', 'hidden', 'urg', 'amiss', 'surviv', 'bone', 'survey', 'exceed', 'vouchsaf', 'dearer', 'deserv', 'alchemi', 'anon', 'forlorn', 'endear', 'alack', 'rotten', 'votari', 'repent', 'relief', 'silver', 'author', 'trespass', 'got', 'advers', 'except', 'separ', 'effect', 'guilt', 'fiend', 'lame', 'vulgar', 'aught', 'leisur', 'twain', 'worship', 'robberi', 'thief', 'poverti', 'lascivi', 'petti', 'temptat', 'seat', 'forbear', 'stray', 'wink', 'direct', 'clearer', 'distanc', 'stop', 'space', 'farthest', 'nimbl', 'length', 'purg', 'wherev', 'messeng', 'pierc', 'smother', 'trifl', 'thrust', 'falsehood', 'sure', 'ward', 'lock', 'chest', 'valley', 'thievish', 'maladi', 'settl', 'eas', 'weight', 'sharp', 'onward', 'fieri', 'seldom', 'captain', 'special', 'imprison', 'whereof', 'preserv', 'imit', 'extern', 'dye', 'mar', 'pace', 'renew', 'forc', 'edg', 'hungri', 'perpetu', 'affair', 'suppos', 'languish', 'patienc', 'tame', 'bide', 'charter', 'privileg', 'backward', 'hundr', 'hasten', 'goe', 'forward', 'crook', 'flourish', 'idl', 'remedi', 'beat', 'cool', 'ink', 'beggar', 'forsworn', 'maiden', 'infect', 'blush', 'sign', 'yore', 'shown', 'vice', 'owe', 'warn', 'fled', 'vilest', 'devis', 'virtuous', 'sang', 'sunset', 'bail', 'consecr', 'twixt', 'asid', 'proceed', 'shadi', 'matur', 'offic', 'ignor', 'feather', 'stole', 'broad', 'worthless', 'build', 'attaint', 'stamp', 'gross', 'slept', 'guilti', 'exampl', 'lean', 'dignifi', 'compil', 'hymn', 'struck', 'compeer', 'conceal', 'vantag', 'physician', 'join', 'humour', 'adjunct', 'measur', 'woeful', 'owner', 'perceiv', 'mansion', 'habit', 'throne', 'queen', 'lamb', 'unfath', 'differ', 'purpl', 'growth', 'redeem', 'prevent', 'wont', 'shook', 'alik', 'forfeit', 'incertainti', 'proclaim', 'crest', 'charact', 'regist', 'bred', 'frailti', 'next', 'goddess', 'provid', 'penanc', 'correct', 'profound', 'buy', 'monarch', 'conscienc', 'palat', 'accid', 'sickl', 'purchas', 'proof', 'level', 'shun', 'cloy', 'polici', 'sphere', 'fit', 'distract', 'nobler', 'rebuk', 'nerv', 'reproach', 'resent', 'borrow', 'bold', 'defi', 'discont', 'drown', 'rent', 'drop', 'creation', 'concord', 'envi', 'jack', 'corrupt', 'danc', 'lust', 'savag', 'pursuit', 'beli', 'pretti', 'confess', 'fulfil', 'anchor', 'forg', 'sever', 'tune', 'prone', 'foolish', 'reprov', 'chase', 'busi', 'infant', 'brighter', 'languid', 'surg', 'southern', 'paradis', 'wept', 'moonlight', 'port', 'implor', 'senseless', 'rule', 'calmer', 'melt', 'flush', 'beheld', 'bled', 'frenzi', 'careless', 'escap', 'roam', 'ice', 'vault', 'pensiv', 'voiceless', 'readi', 'pillow', 'instead', 'faithless', 'arrow', 'tide', 'hearth', 'cherish', 'later', 'lighten', 'woke', 'deadliest', 'sore', 'shock', 'ancient', 'river', 'wreath', 'garden', 'western', 'distress', 'brae', 'exhaust', 'repin', 'aveng', 'sourc', 'bough', 'blown', 'elrington', 'road', 'glitter', 'remors', 'sweeter', 'elmor', 'akin', 'sympathi', 'maze', 'lethargi', 'ladybird', 'vigil', 'soar', 'entreat', 'erflow', 'deiti', 'chosen', 'altho', 'bee', 'riven', 'comrad', 'cell', 'tini', 'blossom', 'moonbeam', 'waveless', 'shout', 'tearless', 'foreign', 'snowi', 'rous', 'blew', 'undim', 'heedless', 'cavern', 'dire', 'sod', 'accurs', 'shrink', 'leaf', 'doubli', 'scent', 'danger', 'chime', 'e', 'arous', 'seraph', 'woodi', 'dell', 'cannon', 'repli', 'blith', 'flutter', 'path', 'fling', 'across', 'resound', 'torrent', 'ici', 'signal', 'yawn', 'kneel', 'stair', 'quiver', 'immort', 'sprang', 'street', 'spurn', 'combin', 'smooth', 'aw', 'eden', 'glare', 'trampl', 'tower', 'spell', 'mirror', 'deck', 'pile', 'mirth', 'agoni', 'soften', 'justic', 'nobl', 'compani', 'dome', 'perci', 'guitar', 'begun', 'reckless', 'uncloud', 'lesley', 'choke', 'deeper', 'embrac', 'guardian', 'depth', 'lamp', 'caught', 'cling', 'narrow', 'stir', 'lifetim', 'sister', 'splendour', 'unutter', 'mild', 'sustain', 'wavi', 'standard', 'final', 'deepen', 'tangl', 'elb', 'undefin', 'darker', 'haze', 'moorland', 'shepherd', 'stilli', 'wend', 'circl', 'began', 'twill', 'approach', 'sabl', 'velvet', 'infinit', 'heathi', 'blast', 'lid', 'shatter', 'rein', 'ought', 'fought', 'rippl', 'norman', 'substanti', 'fuel', 'gaudi', 'buriest', 'makest', 'forti', 'beseig', 'liveri', 'sunken', 'thriftless', 'couldst', 'renewest', 'unbless', 'unear', 'tillag', 'unthrifti', 'bequest', 'frank', 'bounteous', 'largess', 'profitless', 'traffic', 'executor', 'unfair', 'ersnow', 'lees', 'rag', 'vial', 'forbidden', 'usuri', 'loan', 'refigur', 'orient', 'climb', 'highmost', 'car', 'reeleth', 'duteous', 'tract', 'diest', 'get', 'viewest', 'union', 'marri', 'order', 'sire', 'wet', 'consumest', 'issueless', 'hap', 'makeless', 'wife', 'privat', 'user', 'destroy', 'evid', 'stick', 'conspir', 'ruinat', 'threw', 'departest', 'convertest', 'threescor', 'featureless', 'meant', 'therebi', 'clock', 'lofti', 'erst', 'herd', 'gird', 'sheav', 'bier', 'brist', 'beard', 'semblanc', 'hous', 'uphold', 'astronomi', 'luck', 'qualiti', 'famin', 'predict', 'deriv', 'prognost', 'trial', 'presenteth', 'vaunt', 'inconst', 'debateth', 'mightier', 'liker', 'pupil', 'marvel', 'mistak', 'command', 'temper', 'dimm', 'chanc', 'untrimm', 'aggrav', 'brag', 'lion', 'paw', 'teeth', 'tiger', 'jaw', 'phoenix', 'sorri', 'heinous', 'untaint', 'succeed', 'object', 'whereupon', 'gazeth', 'amazeth', 'prick', 'stirr', 'couplement', 'gem', 'candl', 'hearsay', 'persuad', 'furrow', 'expiat', 'raiment', 'wari', 'chari', 'fare', 'presum', 'gavest', 'unperfect', 'actor', 'weaken', 'ceremoni', 'ercharg', 'eloqu', 'stell', 'perspect', 'shop', 'peep', 'favourit', 'marigold', 'warrior', 'famous', 'raze', 'vassalag', 'knit', 'nake', 'whatsoev', 'apparel', 'imaginari', 'thither', 'hie', 'distemp', 'debarr', 'consent', 'complain', 'twire', 'beweep', 'outcast', 'session', 'summon', 'afresh', 'grievanc', 'foregon', 'bemoan', 'religi', 'cheater', 'outstripp', 'reserv', 'march', 'equipag', 'meadow', 'permit', 'visag', 'whit', 'disdaineth', 'reveng', 'promis', 'cloak', 'ertak', 'braveri', 'smoke', 'beaten', 'salv', 'pearl', 'mud', 'parti', 'advoc', 'commenc', 'civil', 'accessari', 'physic', 'sole', 'bewail', 'decrepit', 'entitl', 'engraft', 'suffic', 'partak', 'perus', 'tenth', 'nine', 'rhymer', 'invoc', 'curious', 'deservest', 'teachest', 'hadst', 'usest', 'deceivest', 'refusest', 'befit', 'assail', 'prevail', 'mightest', 'riot', 'tempt', 'guess', 'imperfect', 'jump', 'mile', 'maid', 'dian', 'element', 'badg', 'slide', 'embassi', 'four', 'composit', 'recur', 'recount', 'freedom', 'closet', 'crystal', 'defend', 'cide', 'impannel', 'moieti', 'betwixt', 'unto', 'famish', 'banquet', 'share', 'inheritor', 'excess', 'truest', 'greatest', 'utmost', 'advis', 'prescript', 'graviti', 'ensconc', 'uprear', 'alleg', 'plod', 'dulli', 'instinct', 'rider', 'provok', 'anger', 'bearer', 'post', 'mount', 'neigh', 'race', 'jade', 'fine', 'thin', 'carcanet', 'wardrob', 'instant', 'unfold', 'describ', 'adoni', 'helen', 'grecian', 'foison', 'bounti', 'denot', 'disclos', 'discours', 'madmen', 'unswept', 'besmear', 'sluttish', 'statu', 'overturn', 'broil', 'masonri', 'oblivi', 'enmiti', 'puriti', 'blunter', 'allay', 'sharpen', 'interim', 'requir', 'servant', 'adieu', 'jealous', 'beck', 'list', 'pardon', 'compos', 'pebbl', 'sequent', 'contend', 'elips', 'transfix', 'delv', 'parallel', 'rariti', 'mow', 'pri', 'entertain', 'possesseth', 'defin', 'surmount', 'inde', 'chopp', 'tann', 'contrari', 'iniqu', 'drain', 'steepi', 'outworn', 'hateth', 'interchang', 'rumin', 'warrant', 'stronger', 'honey', 'impregn', 'stout', 'gate', 'insuffici', 'fawn', 'needi', 'trimm', 'jolliti', 'purest', 'unhappili', 'guild', 'misplac', 'strumpet', 'limp', 'disabl', 'doctor', 'miscal', 'simplic', 'impieti', 'achiev', 'lace', 'societi', 'indirect', 'bankrupt', 'vein', 'durst', 'inhabit', 'tress', 'sepulchr', 'shorn', 'fleec', 'map', 'commend', 'accent', 'matcheth', 'solv', 'honest', 'crow', 'unstain', 'ambush', 'sur', 'perhap', 'withal', 'recit', 'twice', 'impart', 'choir', 'late', 'fadeth', 'ash', 'consum', 'arrest', 'carri', 'reviewest', 'review', 'dreg', 'contain', 'miser', 'filch', 'clean', 'starv', 'pursu', 'surfeit', 'variat', 'nymph', 'chast', 'alreadi', 'mouth', 'stealth', 'progress', 'crawl', 'wherewith', 'blank', 'invok', 'assist', 'poesi', 'dispers', 'aloft', 'verdict', 'advanc', 'drudg', 'behavior', 'thereof', 'rondur', 'hem', 'shallowest', 'afloat', 'soundless', 'boat', 'tall', 'thrive', 'epitaph', 'forgotten', 'entomb', 'breather', 'erlook', 'dedic', 'writer', 'intend', 'zealous', 'enforc', 'fresher', 'rhetor', 'sympath', 'debt', 'extant', 'imput', 'impair', 'immur', 'equal', 'penuri', 'counterpart', 'abl', 'polish', 'refin', 'hindmost', 'ripe', 'inhears', 'neither', 'astonish', 'censur', 'aright', 'correspond', 'counten', 'enfeebl', 'estim', 'releas', 'patent', 'swerv', 'mispris', 'dispos', 'gainer', 'legion', 'strangl', 'debat', 'perceivest', 'rearward', 'windi', 'raini', 'overthrow', 'onset', 'fangl', 'hound', 'particular', 'richer', 'prouder', 'revolt', 'hatr', 'virgin', 'disarm', 'appl', 'unmov', 'inherit', 'steward', 'outbrav', 'digniti', 'sourest', 'fester', 'fragrant', 'enclos', 'sport', 'disprais', 'plant', 'chose', 'seeth', 'heed', 'hardest', 'suggest', 'wolf', 'translat', 'gazer', 'mightst', 'freez', 'teem', 'big', 'issu', 'orphan', 'fruit', 'saturn', 'lap', 'vermilion', 'marjoram', 'annex', 'theft', 'veng', 'furi', 'unworthi', 'satir', 'spoil', 'faster', 'truant', 'amend', 'dy', 'intermix', 'strengthen', 'merchand', 'publish', 'philomel', 'front', 'inflam', 'trip', 'process', 'unbr', 'idolatri', 'femal', 'theme', 'nurseth', 'chronicl', 'descript', 'wight', 'knight', 'blazon', 'propheci', 'prefigur', 'prophet', 'augur', 'oliv', 'sort', 'subscrib', 'insult', 'tribe', 'hallow', 'necessari', 'page', 'qualifi', 'easi', 'rang', 'exchang', 'besieg', 'univers', 'motley', 'askanc', 'blench', 'essay', 'grind', 'dyer', 'patient', 'scandal', 'abysm', 'throw', 'adder', 'critic', 'dispens', 'govern', 'function', 'dross', 'latch', 'rudest', 'gentlest', 'deform', 'splendor', 'incap', 'monster', 'indigest', 'cherubin', 'gree', 'lesser', 'afterward', 'creep', 'decre', 'tan', 'intent', 'desper', 'tyranni', 'marriag', 'admit', 'impedi', 'rosi', 'compass', 'scant', 'repay', 'tempteth', 'hoist', 'transport', 'surmis', 'accumul', 'appeal', 'eager', 'sicken', 'sauc', 'welfar', 'anticip', 'medicin', 'drug', 'limbeck', 'appli', 'treason', 'befriend', 'transgress', 'hammer', 'taken', 'deepest', 'hit', 'fee', 'adulter', 'salut', 'sportiv', 'frailer', 'spi', 'bevel', 'maintain', 'faculti', 'subsist', 'miss', 'retent', 'talli', 'score', 'import', 'pyramid', 'built', 'newer', 'novel', 'continu', 'pomp', 'heret', 'polit', 'dweller', 'forgo', 'savour', 'thriver', 'oblat', 'mix', 'suborn', 'inform', 'impeach', 'balmi', 'fickl', 'wrack', 'goest', 'detain', 'quietus', 'raven', 'wiri', 'devil', 'breach', 'tickl', 'situat', 'chip', 'gait', 'sauci', 'random', 'hunt', 'swallow', 'bait', 'taker', 'quest', 'propos', 'uncertain', 'coral', 'dun', 'damask', 'reek', 'act', 'torn', 'err', 'neck', 'ruth', 'east', 'usher', 'sober', 'beseem', 'beshrew', 'slaveri', 'harder', 'engross', 'forsaken', 'threefold', 'whoe', 'rigor', 'gaol', 'pent', 'mortgag', 'covet', 'sureti', 'statut', 'whoever', 'written', 'embassag', 'spacious', 'addeth', 'beseech', 'receipt', 'heal', 'partial', 'bay', 'hook', 'plot', 'transferr', 'untutor', 'unlearn', 'subtleti', 'simpli', 'credit', 'suppress', 'justifi', 'slay', 'elsewher', 'defens', 'outright', 'rid', 'testi', 'news', 'wrest', 'sensual', 'dissuad', 'unsway', 'vassal', 'award', 'scarlet', 'frantic', 'unrest', 'robb', 'revenu', 'importun', 'housewif', 'runn', 'outlaw', 'stoop', 'quenchless', 'tempestu', 'arden', 'motionless', 'laughter', 'sunlit', 'derid', 'whirlwind', 'chorus', 'flit', 'unregret', 'spici', 'indulg', 'raptur', 'gori', 'rave', 'eyesight', 'unaw', 'muster', 'hark', 'gun', 'victim', 'northern', 'brown', 'reclin', 'hoari', 'roseat', 'almador', 'yell', 'unheed', 'floor', 'arctic', 'dismay', 'damp', 'dewdrop', 'rattl', 'rail', 'grim', 'concav', 'agonis', 'everywher', 'aim', 'resign', 'drift', 'falter', 'voyag', 'descri', 'eldr', 'treacher', 'relic', 'scatter', 'giant', 'anakim', 'blent', 'steed', 'charg', 'unknown', 'empti', 'conclud', 'roder', 'consol', 'daybreak', 'soulless', 'gallant', 'wean', 'attir', 'latest', 'hapless', 'rung', 'restless', 'tuft', 'louder', 'unreal', 'unfathom', 'daughter', 'grand', 'display', 'suspicion', 'atlant', 'sacrific', 'newli', 'starri', 'grove', 'lowest', 'sung', 'afric', 'conqueror', 'julius', 'impious', 'english', 'dreamt', 'sent', 'wider', 'stormless', 'imbu', 'debar', 'begon', 'crouch', 'infami', 'struggl', 'downi', 'silk', 'arm', 'trembl', 'bland', 'charm', 'mimic', 'offer', 'gabriel', 'swore', 'altar', 'vultur', 'sear', 'sunlight', 'lyre', 'bought', 'happiest', 'heather', 'untim', 'palac', 'templ', 'patriot', 'branch', 'sleet', 'vacanc', 'delug', 'mossi', 'seren', 'churn', 'deadlier', 'aloud', 'friendship', 'tenfold', 'adorn', 'vessel', 'castl', 'peevish', 'cumber', 'tumult', 'assuag', 'sympathis', 'link', 'powerless', 'tranquil', 'deer', 'glisten', 'repeat', 'edward', 'amongst', 'aimless', 'drench', 'dagger', 'sabbath', 'underneath', 'belt', 'weapon', 'jubile', 'shyli', 'spare', 'disturb', 'visit', 'brush', 'departur', 'unrel', 'dastard', 'treacheri', 'comet', 'seed', 'invis', 'brotherhood', 'en', 'vital', 'spark', 'madden', 'demon', 'redden', 'sculptur', 'un', 'lavish', 'befel', 'frequent', 'countri', 'moss', 'labyrinth', 'goal', 'chainless', 'holiday', 'harass', 'apart', 'arch', 'firelight', 'moonlit', 'stroke', 'motto', 'drew', 'crimson', 'revel', 'sheep', 'becloud', 'game', 'restraint', 'recoil', 'faintest', 'begilt', 'tassel', 'cord', 'hiss', 'unopen', 'obscur', 'billowi', 'volley', 'sting', 'geraldin', 'sunbeam', 'aspin', 'unforgiven', 'skylark', 'plaintiv', 'unavail', 'quell', 'deal', 'hoar', 'arthur', 'brother', 'rosina', 'nowher', 'corn', 'paus', 'unshadow', 'linnet', 'trill', 'entiti', 'reel', 'column', 'hurri', 'oak', 'six', 'array', 'needst', 'dissembl', 'nameless', 'darkest', 'caress', 'convers', 'cloudless', 'forehead', 'boon', 'evinc', 'gratitud', 'zalona', 'celebr', 'realiti', 'aisl', 'lut', 'tumbl', 'inki', 'lull', 'monoton', 'withdrawn', 'familiar', 'glorifi', 'grassi', 'unearth', 'unbroken', 'holli', 'brier', 'zenith', 'brazen', 'nearer', 'bubbl', 'float', 'flicker', 'radianc', 'higher', 'sapl', 'ponder', 'banish', 'camp', 'retir', 'den', 'gulf', 'lightsom', 'met', 'gentler', 'teacher', 'brenzaida', 'funer', 'pall', 'lour', 'sinless', 'resistlesslyt', 'carol', 'daisi', 'lawn', 'inclin', 'reck', 'woodland', 'dash', 'remot', 'undergo', 'galleri', 'tiresom', 'wan', 'hoof', 'print', 'crush', 'elm', 'pant', 'fraught', 'real', 'fete', 'unquench', 'wold', 'minster', 'yard', 'melancholi', 'mytholog', 'stranger', 'taint', 'mankind', 'scentless', 'petal', 'lustr', 'unceas', 'crash', 'stanza', 'manuscript', 'banner', 'waft', 'repel', 'petrel', 'truer', 'flung', 'streak', 'moonshin', 'giver', 'slowli', 'guiltless', 'myriad', 'campaign', 'sombr', 'portal', 'wrapt', 'drowsi', 'wretched', 'unsustain', 'wax', 'curb', 'unmark', 'bade', 'fervent', 'zeal', 'choos', 'lair', 'emili', 'wrote', 'wholli', 'almighti', 'tarnish', 'intens', 'steadfast', 'pervad', 'dissolv', 'rear', 'ember', 'wick', 'midst', 'cheerless', 'brink', 'ghastlier', 'shoulder', 'gasp', 'expel', 'thicken', 'airi', 'patrician', 'goat', 'sheen', 'ungovern', 'fragranc', 'tore', 'unspeak', 'york', 'nursl', 'wore', 'gale', 'hail', 'south', 'unexhaust', 'desol', 'regiv', 'heron', 'fern', 'mockeri', 'mellow', 'marr', 'ancestr', 'infin', 'inspir', 'laden', 'flew', 'thro', 'scar', 'misti', 'dryad', 'gush', 'furnac', 'lain', 'discord', 'lute', 'unstrung', 'meal', 'awok', 'shrank', 'regina', 'retrac', 'respons', 'granit', 'vagu', 'ring', 'awar', 'weaker', 'yeoman', 'cloister', 'conductor', 'sand', 'effac', 'uncov', 'whistl', 'companion', 'vacant', 'sinner', 'eversham', 'disappear', 'feudal', 'scowl', 'vengeanc', 'sheath', 'immens', 'celesti', 'beset', 'chord', 'earliest', 'reveri', 'unlock', 'nook', 'imageri', 'harvest', 'lorn', 'invinc', 'ambit', 'dreamlik', 'tuneless', 'vigor', 'clung', 'bridl', 'falcon', 'pretend', 'roofless', 'crumbl', 'noontid', 'saddest', 'entir', 'unbiass', 'sensat', 'forerunn', 'sterner', 'daredst', 'unfinish', 'forgiven', 'driven', 'unhappi', 'earthward', 'whiter', 'lightn', 'pathway', 'changeless', 'event', 'bygon', 'claim', 'heavier', 'fejian', 'devote', 'fireless', 'lifeless', 'puni', 'festal', 'affrighten', 'pane', 'unansw', 'neath', 'confus', 'innoc', 'juli', 'remark', 'degrad', 'whiten', 'fernando', 'despond', 'lit', 'daylong', 'afternoon', 'ashi', 'ship', 'bereft', 'curtain', 'azur', 'deliver', 'cope', 'plunder', 'ula', 'woodros', 'cultur', 'perjuri', 'soldier', 'turret', 'blackbird', 'throstl', 'gong', 'toll', 'unlik', 'deepli', 'iron', 'joyless', 'imparti', 'swollen', 'anxious', 'amid', 'eldenna', 'relent', 'sieg', 'purifi', 'unimagin', 'drizzli', 'bandit', 'laps', 'seiz', 'steadi', 'flute', 'royal', 'eastern', 'incens', 'burnt', 'launch', 'stolen', 'moulder', 'shallow', 'intim', 'hinder', 'hing', 'yonder', 'prudenc', 'zamorna', 'nobli', 'softer', 'wintri', 'yesternight', 'humbl', 'froze', 'angora', 'merri', 'clench', 'trod', 'fright', 'shapeless', 'piec', 'essenc', 'crag', 'songless', 'nest', 'studi', 'prospect']
		#<2
		Lower_Freq = ['substanti', 'fuel', 'gaudi', 'buriest', 'makest', 'forti', 'beseig', 'liveri', 'sunken', 'thriftless', 'couldst', 'renewest', 'unbless', 'unear', 'tillag', 'unthrifti', 'bequest', 'frank', 'bounteous', 'largess', 'profitless', 'traffic', 'executor', 'unfair', 'ersnow', 'lees', 'rag', 'vial', 'forbidden', 'usuri', 'loan', 'refigur', 'orient', 'climb', 'highmost', 'car', 'reeleth', 'duteous', 'tract', 'diest', 'get', 'viewest', 'union', 'marri', 'order', 'sire', 'wet', 'consumest', 'issueless', 'hap', 'makeless', 'wife', 'privat', 'user', 'destroy', 'evid', 'stick', 'conspir', 'ruinat', 'threw', 'departest', 'convertest', 'threescor', 'featureless', 'meant', 'therebi', 'clock', 'lofti', 'erst', 'herd', 'gird', 'sheav', 'bier', 'brist', 'beard', 'semblanc', 'hous', 'uphold', 'astronomi', 'luck', 'qualiti', 'famin', 'predict', 'deriv', 'prognost', 'trial', 'presenteth', 'vaunt', 'inconst', 'debateth', 'mightier', 'liker', 'pupil', 'marvel', 'mistak', 'command', 'temper', 'dimm', 'chanc', 'untrimm', 'aggrav', 'brag', 'lion', 'paw', 'teeth', 'tiger', 'jaw', 'phoenix', 'sorri', 'heinous', 'untaint', 'succeed', 'object', 'whereupon', 'gazeth', 'amazeth', 'prick', 'stirr', 'couplement', 'gem', 'candl', 'hearsay', 'persuad', 'furrow', 'expiat', 'raiment', 'wari', 'chari', 'fare', 'presum', 'gavest', 'unperfect', 'actor', 'weaken', 'ceremoni', 'ercharg', 'eloqu', 'stell', 'perspect', 'shop', 'peep', 'favourit', 'marigold', 'warrior', 'famous', 'raze', 'vassalag', 'knit', 'nake', 'whatsoev', 'apparel', 'imaginari', 'thither', 'hie', 'distemp', 'debarr', 'consent', 'complain', 'twire', 'beweep', 'outcast', 'session', 'summon', 'afresh', 'grievanc', 'foregon', 'bemoan', 'religi', 'cheater', 'outstripp', 'reserv', 'march', 'equipag', 'meadow', 'permit', 'visag', 'whit', 'disdaineth', 'reveng', 'promis', 'cloak', 'ertak', 'braveri', 'smoke', 'beaten', 'salv', 'pearl', 'mud', 'parti', 'advoc', 'commenc', 'civil', 'accessari', 'physic', 'sole', 'bewail', 'decrepit', 'entitl', 'engraft', 'suffic', 'partak', 'perus', 'tenth', 'nine', 'rhymer', 'invoc', 'curious', 'deservest', 'teachest', 'hadst', 'usest', 'deceivest', 'refusest', 'befit', 'assail', 'prevail', 'mightest', 'riot', 'tempt', 'guess', 'imperfect', 'jump', 'mile', 'maid', 'dian', 'element', 'badg', 'slide', 'embassi', 'four', 'composit', 'recur', 'recount', 'freedom', 'closet', 'crystal', 'defend', 'cide', 'impannel', 'moieti', 'betwixt', 'unto', 'famish', 'banquet', 'share', 'inheritor', 'excess', 'truest', 'greatest', 'utmost', 'advis', 'prescript', 'graviti', 'ensconc', 'uprear', 'alleg', 'plod', 'dulli', 'instinct', 'rider', 'provok', 'anger', 'bearer', 'post', 'mount', 'neigh', 'race', 'jade', 'fine', 'thin', 'carcanet', 'wardrob', 'instant', 'unfold', 'describ', 'adoni', 'helen', 'grecian', 'foison', 'bounti', 'denot', 'disclos', 'discours', 'madmen', 'unswept', 'besmear', 'sluttish', 'statu', 'overturn', 'broil', 'masonri', 'oblivi', 'enmiti', 'puriti', 'blunter', 'allay', 'sharpen', 'interim', 'requir', 'servant', 'adieu', 'jealous', 'beck', 'list', 'pardon', 'compos', 'pebbl', 'sequent', 'contend', 'elips', 'transfix', 'delv', 'parallel', 'rariti', 'mow', 'pri', 'entertain', 'possesseth', 'defin', 'surmount', 'inde', 'chopp', 'tann', 'contrari', 'iniqu', 'drain', 'steepi', 'outworn', 'hateth', 'interchang', 'rumin', 'warrant', 'stronger', 'honey', 'impregn', 'stout', 'gate', 'insuffici', 'fawn', 'needi', 'trimm', 'jolliti', 'purest', 'unhappili', 'guild', 'misplac', 'strumpet', 'limp', 'disabl', 'doctor', 'miscal', 'simplic', 'impieti', 'achiev', 'lace', 'societi', 'indirect', 'bankrupt', 'vein', 'durst', 'inhabit', 'tress', 'sepulchr', 'shorn', 'fleec', 'map', 'commend', 'accent', 'matcheth', 'solv', 'honest', 'crow', 'unstain', 'ambush', 'sur', 'perhap', 'withal', 'recit', 'twice', 'impart', 'choir', 'late', 'fadeth', 'ash', 'consum', 'arrest', 'carri', 'reviewest', 'review', 'dreg', 'contain', 'miser', 'filch', 'clean', 'starv', 'pursu', 'surfeit', 'variat', 'nymph', 'chast', 'alreadi', 'mouth', 'stealth', 'progress', 'crawl', 'wherewith', 'blank', 'invok', 'assist', 'poesi', 'dispers', 'aloft', 'verdict', 'advanc', 'drudg', 'behavior', 'thereof', 'rondur', 'hem', 'shallowest', 'afloat', 'soundless', 'boat', 'tall', 'thrive', 'epitaph', 'forgotten', 'entomb', 'breather', 'erlook', 'dedic', 'writer', 'intend', 'zealous', 'enforc', 'fresher', 'rhetor', 'sympath', 'debt', 'extant', 'imput', 'impair', 'immur', 'equal', 'penuri', 'counterpart', 'abl', 'polish', 'refin', 'hindmost', 'ripe', 'inhears', 'neither', 'astonish', 'censur', 'aright', 'correspond', 'counten', 'enfeebl', 'estim', 'releas', 'patent', 'swerv', 'mispris', 'dispos', 'gainer', 'legion', 'strangl', 'debat', 'perceivest', 'rearward', 'windi', 'raini', 'overthrow', 'onset', 'fangl', 'hound', 'particular', 'richer', 'prouder', 'revolt', 'hatr', 'virgin', 'disarm', 'appl', 'unmov', 'inherit', 'steward', 'outbrav', 'digniti', 'sourest', 'fester', 'fragrant', 'enclos', 'sport', 'disprais', 'plant', 'chose', 'seeth', 'heed', 'hardest', 'suggest', 'wolf', 'translat', 'gazer', 'mightst', 'freez', 'teem', 'big', 'issu', 'orphan', 'fruit', 'saturn', 'lap', 'vermilion', 'marjoram', 'annex', 'theft', 'veng', 'furi', 'unworthi', 'satir', 'spoil', 'faster', 'truant', 'amend', 'dy', 'intermix', 'strengthen', 'merchand', 'publish', 'philomel', 'front', 'inflam', 'trip', 'process', 'unbr', 'idolatri', 'femal', 'theme', 'nurseth', 'chronicl', 'descript', 'wight', 'knight', 'blazon', 'propheci', 'prefigur', 'prophet', 'augur', 'oliv', 'sort', 'subscrib', 'insult', 'tribe', 'hallow', 'necessari', 'page', 'qualifi', 'easi', 'rang', 'exchang', 'besieg', 'univers', 'motley', 'askanc', 'blench', 'essay', 'grind', 'dyer', 'patient', 'scandal', 'abysm', 'throw', 'adder', 'critic', 'dispens', 'govern', 'function', 'dross', 'latch', 'rudest', 'gentlest', 'deform', 'splendor', 'incap', 'monster', 'indigest', 'cherubin', 'gree', 'lesser', 'afterward', 'creep', 'decre', 'tan', 'intent', 'desper', 'tyranni', 'marriag', 'admit', 'impedi', 'rosi', 'compass', 'scant', 'repay', 'tempteth', 'hoist', 'transport', 'surmis', 'accumul', 'appeal', 'eager', 'sicken', 'sauc', 'welfar', 'anticip', 'medicin', 'drug', 'limbeck', 'appli', 'treason', 'befriend', 'transgress', 'hammer', 'taken', 'deepest', 'hit', 'fee', 'adulter', 'salut', 'sportiv', 'frailer', 'spi', 'bevel', 'maintain', 'faculti', 'subsist', 'miss', 'retent', 'talli', 'score', 'import', 'pyramid', 'built', 'newer', 'novel', 'continu', 'pomp', 'heret', 'polit', 'dweller', 'forgo', 'savour', 'thriver', 'oblat', 'mix', 'suborn', 'inform', 'impeach', 'balmi', 'fickl', 'wrack', 'goest', 'detain', 'quietus', 'raven', 'wiri', 'devil', 'breach', 'tickl', 'situat', 'chip', 'gait', 'sauci', 'random', 'hunt', 'swallow', 'bait', 'taker', 'quest', 'propos', 'uncertain', 'coral', 'dun', 'damask', 'reek', 'act', 'torn', 'err', 'neck', 'ruth', 'east', 'usher', 'sober', 'beseem', 'beshrew', 'slaveri', 'harder', 'engross', 'forsaken', 'threefold', 'whoe', 'rigor', 'gaol', 'pent', 'mortgag', 'covet', 'sureti', 'statut', 'whoever', 'written', 'embassag', 'spacious', 'addeth', 'beseech', 'receipt', 'heal', 'partial', 'bay', 'hook', 'plot', 'transferr', 'untutor', 'unlearn', 'subtleti', 'simpli', 'credit', 'suppress', 'justifi', 'slay', 'elsewher', 'defens', 'outright', 'rid', 'testi', 'news', 'wrest', 'sensual', 'dissuad', 'unsway', 'vassal', 'award', 'scarlet', 'frantic', 'unrest', 'robb', 'revenu', 'importun', 'housewif', 'runn', 'outlaw', 'stoop', 'quenchless', 'tempestu', 'arden', 'motionless', 'laughter', 'sunlit', 'derid', 'whirlwind', 'chorus', 'flit', 'unregret', 'spici', 'indulg', 'raptur', 'gori', 'rave', 'eyesight', 'unaw', 'muster', 'hark', 'gun', 'victim', 'northern', 'brown', 'reclin', 'hoari', 'roseat', 'almador', 'yell', 'unheed', 'floor', 'arctic', 'dismay', 'damp', 'dewdrop', 'rattl', 'rail', 'grim', 'concav', 'agonis', 'everywher', 'aim', 'resign', 'drift', 'falter', 'voyag', 'descri', 'eldr', 'treacher', 'relic', 'scatter', 'giant', 'anakim', 'blent', 'steed', 'charg', 'unknown', 'empti', 'conclud', 'roder', 'consol', 'daybreak', 'soulless', 'gallant', 'wean', 'attir', 'latest', 'hapless', 'rung', 'restless', 'tuft', 'louder', 'unreal', 'unfathom', 'daughter', 'grand', 'display', 'suspicion', 'atlant', 'sacrific', 'newli', 'starri', 'grove', 'lowest', 'sung', 'afric', 'conqueror', 'julius', 'impious', 'english', 'dreamt', 'sent', 'wider', 'stormless', 'imbu', 'debar', 'begon', 'crouch', 'infami', 'struggl', 'downi', 'silk', 'arm', 'trembl', 'bland', 'charm', 'mimic', 'offer', 'gabriel', 'swore', 'altar', 'vultur', 'sear', 'sunlight', 'lyre', 'bought', 'happiest', 'heather', 'untim', 'palac', 'templ', 'patriot', 'branch', 'sleet', 'vacanc', 'delug', 'mossi', 'seren', 'churn', 'deadlier', 'aloud', 'friendship', 'tenfold', 'adorn', 'vessel', 'castl', 'peevish', 'cumber', 'tumult', 'assuag', 'sympathis', 'link', 'powerless', 'tranquil', 'deer', 'glisten', 'repeat', 'edward', 'amongst', 'aimless', 'drench', 'dagger', 'sabbath', 'underneath', 'belt', 'weapon', 'jubile', 'shyli', 'spare', 'disturb', 'visit', 'brush', 'departur', 'unrel', 'dastard', 'treacheri', 'comet', 'seed', 'invis', 'brotherhood', 'en', 'vital', 'spark', 'madden', 'demon', 'redden', 'sculptur', 'un', 'lavish', 'befel', 'frequent', 'countri', 'moss', 'labyrinth', 'goal', 'chainless', 'holiday', 'harass', 'apart', 'arch', 'firelight', 'moonlit', 'stroke', 'motto', 'drew', 'crimson', 'revel', 'sheep', 'becloud', 'game', 'restraint', 'recoil', 'faintest', 'begilt', 'tassel', 'cord', 'hiss', 'unopen', 'obscur', 'billowi', 'volley', 'sting', 'geraldin', 'sunbeam', 'aspin', 'unforgiven', 'skylark', 'plaintiv', 'unavail', 'quell', 'deal', 'hoar', 'arthur', 'brother', 'rosina', 'nowher', 'corn', 'paus', 'unshadow', 'linnet', 'trill', 'entiti', 'reel', 'column', 'hurri', 'oak', 'six', 'array', 'needst', 'dissembl', 'nameless', 'darkest', 'caress', 'convers', 'cloudless', 'forehead', 'boon', 'evinc', 'gratitud', 'zalona', 'celebr', 'realiti', 'aisl', 'lut', 'tumbl', 'inki', 'lull', 'monoton', 'withdrawn', 'familiar', 'glorifi', 'grassi', 'unearth', 'unbroken', 'holli', 'brier', 'zenith', 'brazen', 'nearer', 'bubbl', 'float', 'flicker', 'radianc', 'higher', 'sapl', 'ponder', 'banish', 'camp', 'retir', 'den', 'gulf', 'lightsom', 'met', 'gentler', 'teacher', 'brenzaida', 'funer', 'pall', 'lour', 'sinless', 'resistlesslyt', 'carol', 'daisi', 'lawn', 'inclin', 'reck', 'woodland', 'dash', 'remot', 'undergo', 'galleri', 'tiresom', 'wan', 'hoof', 'print', 'crush', 'elm', 'pant', 'fraught', 'real', 'fete', 'unquench', 'wold', 'minster', 'yard', 'melancholi', 'mytholog', 'stranger', 'taint', 'mankind', 'scentless', 'petal', 'lustr', 'unceas', 'crash', 'stanza', 'manuscript', 'banner', 'waft', 'repel', 'petrel', 'truer', 'flung', 'streak', 'moonshin', 'giver', 'slowli', 'guiltless', 'myriad', 'campaign', 'sombr', 'portal', 'wrapt', 'drowsi', 'wretched', 'unsustain', 'wax', 'curb', 'unmark', 'bade', 'fervent', 'zeal', 'choos', 'lair', 'emili', 'wrote', 'wholli', 'almighti', 'tarnish', 'intens', 'steadfast', 'pervad', 'dissolv', 'rear', 'ember', 'wick', 'midst', 'cheerless', 'brink', 'ghastlier', 'shoulder', 'gasp', 'expel', 'thicken', 'airi', 'patrician', 'goat', 'sheen', 'ungovern', 'fragranc', 'tore', 'unspeak', 'york', 'nursl', 'wore', 'gale', 'hail', 'south', 'unexhaust', 'desol', 'regiv', 'heron', 'fern', 'mockeri', 'mellow', 'marr', 'ancestr', 'infin', 'inspir', 'laden', 'flew', 'thro', 'scar', 'misti', 'dryad', 'gush', 'furnac', 'lain', 'discord', 'lute', 'unstrung', 'meal', 'awok', 'shrank', 'regina', 'retrac', 'respons', 'granit', 'vagu', 'ring', 'awar', 'weaker', 'yeoman', 'cloister', 'conductor', 'sand', 'effac', 'uncov', 'whistl', 'companion', 'vacant', 'sinner', 'eversham', 'disappear', 'feudal', 'scowl', 'vengeanc', 'sheath', 'immens', 'celesti', 'beset', 'chord', 'earliest', 'reveri', 'unlock', 'nook', 'imageri', 'harvest', 'lorn', 'invinc', 'ambit', 'dreamlik', 'tuneless', 'vigor', 'clung', 'bridl', 'falcon', 'pretend', 'roofless', 'crumbl', 'noontid', 'saddest', 'entir', 'unbiass', 'sensat', 'forerunn', 'sterner', 'daredst', 'unfinish', 'forgiven', 'driven', 'unhappi', 'earthward', 'whiter', 'lightn', 'pathway', 'changeless', 'event', 'bygon', 'claim', 'heavier', 'fejian', 'devote', 'fireless', 'lifeless', 'puni', 'festal', 'affrighten', 'pane', 'unansw', 'neath', 'confus', 'innoc', 'juli', 'remark', 'degrad', 'whiten', 'fernando', 'despond', 'lit', 'daylong', 'afternoon', 'ashi', 'ship', 'bereft', 'curtain', 'azur', 'deliver', 'cope', 'plunder', 'ula', 'woodros', 'cultur', 'perjuri', 'soldier', 'turret', 'blackbird', 'throstl', 'gong', 'toll', 'unlik', 'deepli', 'iron', 'joyless', 'imparti', 'swollen', 'anxious', 'amid', 'eldenna', 'relent', 'sieg', 'purifi', 'unimagin', 'drizzli', 'bandit', 'laps', 'seiz', 'steadi', 'flute', 'royal', 'eastern', 'incens', 'burnt', 'launch', 'stolen', 'moulder', 'shallow', 'intim', 'hinder', 'hing', 'yonder', 'prudenc', 'zamorna', 'nobli', 'softer', 'wintri', 'yesternight', 'humbl', 'froze', 'angora', 'merri', 'clench', 'trod', 'fright', 'shapeless', 'piec', 'essenc', 'crag', 'songless', 'nest', 'studi', 'prospect']
		#Shakspeare
		# 100 or more
		S_freq100 = ['thi', 'thou', 'love', 'thee']
		# 50 - 99
		S_freq50 = ['doth', 'eye', 'time', 'beauti', 'sweet', 'heart', 'make', 'mine']
		# 10 - 49
		S_freq10 = ['shall', 'art', 'live', 'yet', 'still', 'one', 'fair', 'thine', 'day', 'like', 'hath', 'give', 'see', 'look', 'though', 'know', 'show', 'world', 'prais', 'st', 'true', 'thought', 'may', 'part', 'lie', 'say', 'dost', 'everi', 'let', 'well', 'night', 'upon', 'might', 'new', 'sinc', 'dear', 'truth', 'life', 'even', 'thus', 'face', 'summer', 'death', 'tongu', 'fals', 'think', 'better', 'self', 'prove', 'must', 'tell', 'seem', 'hast', 'would', 'men', 'thing', 'thyself', 'old', 'made', 'whose', 'age', 'noth', 'alon', 'leav', 'hand', 'sight', 'heaven', 'hate', 'away', 'come', 'find', 'ill', 'best', 'youth', 'worth', 'natur', 'use', 'much', 'good', 'er', 'therefor', 'call', 'friend', 'dead', 'hold', 'bear', 'poor', 'sin', 'hour', 'fear', 'keep', 'kind', 'vers', 'other', 'state', 'proud', 'never', 'wilt', 'chang', 'grace', 'long', 'woe', 'grow', 'full', 'name', 'soul', 'shame', 'gentl', 'mani', 'mind', 'take', 'rich', 'first', 'till', 'muse', 'speak', 'desir', 'wast', 'piti', 'earth', 'die', 'none', 'mayst', 'store', 'need', 'right', 'pride', 'word', 'far', 'black', 'fire', 'rose', 'lose', 'bright', 'within', 'winter', 'anoth', 'place', 'delight', 'shalt', 'end', 'decay', 'stand', 'paint', 'line', 'write', 'ever', 'steal', 'spirit']
		#5 - 9
		S_freq5 = ['brow', 'treasur', 'glass', 'back', 'flower', 'happi', 'strong', 'beauteous', 'without', 'born', 'wrong', 'pleasur', 'tis', 'reason', 'whilst', 'fortun', 'wit', 'shadow', 'found', 'seen', 'bring', 'power', 'tender', 'memori', 'excus', 'lend', 'great', 'work', 'joy', 'sing', 'past', 'honour', 'stay', 'set', 'bless', 'pen', 'skill', 'breath', 'mistress', 'sun', 'care', 'hope', 'put', 'bad', 'disgrac', 'deed', 'fault', 'two', 'hell', 'cheek', 'mad', 'feed', 'light', 'deep', 'form', 'spend', 'dwell', 'rest', 'ten', 'could', 'appear', 'go', 'sad', 'war', 'year', 'lip', 'save', 'etern', 'star', 'judgment', 'breast', 'view', 'hide', 'number', 'less', 'strength', 'bodi', 'cure', 'want', 'remov', 'present', 'loss', 'sorrow', 'lest', 'turn', 'glori', 'invent', 'cannot', 'swear', 'dull', 'virtu', 'sick', 'ornament', 'bud', 'content', 'weed', 'child', 'count', 'tomb', 'gone', 'play', 'bare', 'ere', 'gracious', 'way', 'hear', 'lovest', 'despis', 'chide', 'pleas', 'ah', 'barren', 'behold', 'green', 'longer', 'read', 'date', 'touch', 'sometim', 'blood', 'wide', 'antiqu', 'worst', 'man', 'hue', 'purpos', 'taught', 'dumb', 'express', 'merit', 'blind', 'grief', 'lack', 'forth', 'wealth', 'alter', 'crown', 'subject', 'argument', 'although', 'near', 'sake', 'heavi', 'return', 'straight', 'outward', 'thenc', 'strang', 'wretch', 'side', 'foul', 'slave', 'tie', 'vow', 'spent', 'three', 'fairest', 'cruel', 'fresh', 'spring', 'due', 'sum', 'despit', 'wrinkl', 'rememb', 'singl', 'imag', 'brand', 'fell', 'canst', 'tyrant', 'confound', 'quit', 'distil', 'kill', 'pay', 'will', 'burn', 'head', 'mortal', 'unless', 'ear', 'shape', 'possess', 'gainst', 'seek', 'least', 'cold', 'rude', 'heat', 'white', 'henc', 'rage', 'abund', 'rhyme', 'believ', 'poet', 'motion', 'swift', 'woman', 'gild', 'compar', 'truli', 'trust', 'forget', 'book', 'learn', 'writ', 'pictur', 'buri', 'pain', 'toil', 'worthi', 'respect', 'travel', 'dark', 'jewel', 'flatter', 'abus', 'wish', 'scope', 'king', 'precious', 'tear', 'cloud', 'enough', 'took', 'absenc', 'suffer', 'blame', 'injuri', 'gain', 'lay', 'sleep', 'larg', 'water', 'receiv', 'slow', 'assur', 'ground', 'groan', 'becom', 'brain', 'second', 'wors', 'gift', 'slander', 'esteem', 'unkind']
		
		#Bronte
		B_freq100 = []
		#>50
		B_freq50 = ['thi']
		#10 - 49
		B_freq10 = ['heart', 'day', 'thou', 'eye', 'away', 'thee', 'tear', 'heaven', 'long', 'shall', 'one', 'would', 'er', 'yet', 'earth', 'night', 'spirit', 'like', 'dark', 'soul', 'love', 'come', 'still', 'light', 'sky', 'die', 'even', 'wind', 'wild', 'last', 'though', 'life', 'rest', 'round', 'bright', 'thought', 'time', 'may', 'summer', 'hour', 'far', 'wave', 'smile', 'sun', 'sleep', 'hope', 'never', 'mourn', 'woe', 'sweet', 'see', 'ever', 'dead', 'feel', 'cold', 'tis', 'dream', 'death', 'lone', 'could', 'must', 'look', 'leav', 'well', 'sigh', 'thine', 'everi', 'home', 'weep', 'mountain', 'grief', 'cannot', 'sound', 'shine', 'brow', 'glori', 'year', 'whose', 'watch', 'deep', 'mine', 'hill', 'fall', 'might', 'seem', 'lie', 'gaze', 'green', 'free', 'oh', 'mind', 'power', 'drear', 'youth', 'divin', 'sea', 'god', 'breast', 'tell', 'call', 'memori', 'close', 'face', 'voic', 'beneath', 'morn', 'burn', 'wake', 'saw', 'gloom', 'upon', 'turn', 'vain', 'fear', 'star', 'etern', 'fair', 'chang', 'word', 'true', 'tree', 'alon', 'gone', 'sad', 'rise', 'world', 'full', 'art', 'till', 'pass', 'within', 'sunshin', 'care', 'whisper', 'pain', 'young', 'mani', 'know', 'bless', 'wander', 'tomb', 'cloud', 'weari', 'thus', 'air', 'first', 'sing', 'form', 'mist']
		#5 - 9
		B_freq5 = ['blue', 'back', 'man', 'glorious', 'vision', 'spring', 'lay', 'old', 'past', 'let', 'breez', 'stream', 'pride', 'flower', 'littl', 'despair', 'murmur', 'pour', 'speak', 'bird', 'golden', 'music', 'scorn', 'left', 'dear', 'give', 'rais', 'beauti', 'winter', 'bliss', 'laid', 'break', 'hand', 'glad', 'listen', 'flow', 'need', 'side', 'glow', 'roar', 'dreari', 'anoth', 'breath', 'storm', 'soft', 'bring', 'think', 'beam', 'wall', 'silent', 'keep', 'say', 'lost', 'moor', 'near', 'go', 'done', 'gleam', 'wood', 'warm', 'given', 'water', 'blow', 'blood', 'natur', 'hear', 'grave', 'ocean', 'tone', 'us', 'faint', 'dew', 'dim', 'seek', 'sudden', 'wide', 'snow', 'rain', 'grass', 'sorrow', 'hall', 'peac', 'dungeon', 'calm', 'heavi', 'part', 'chain', 'noth', 'bound', 'strong', 'spread', 'mighti', 'hair', 'strang', 'earli', 'place', 'stand', 'head', 'felt', 'sink', 'forgot', 'happi', 'greet', 'nay', 'human', 'none', 'dazzl', 'glanc', 'rose', 'grew', 'around', 'chill', 'gather', 'bear', 'sit', 'bower', 'men', 'shadow', 'thousand', 'cheek', 'return', 'mad', 'twilight', 'mortal', 'name', 'low', 'sinc', 'miseri', 'angel', 'stone', 'ere', 'dawn', 'dearest', 'solemn', 'ardent', 'window', 'dust', 'bitter', 'stern', 'way', 'bloom', 'wast', 'child', 'live', 'father', 'subdu', 'forth', 'shed', 'open', 'door', 'dare', 'prayer', 'sooth', 'track', 'red', 'cheer', 'friend', 'guid', 'hold', 'cours', 'fight', 'heard', 'crowd', 'thrill', 'flame', 'shore', 'wilt', 'pleasur', 'held', 'trust', 'linger', 'shone', 'ray', 'fast', 'hard', 'gloomi', 'cruel', 'anguish', 'mingl', 'joy', 'hide', 'follow', 'crime', 'wish', 'griev', 'declin', 'laugh', 'tread', 'tongu', 'swell', 'feet', 'troubl', 'ask', 'knew', 'sat', 'forget']
		

		for ii in kTOKENIZER.tokenize(text):
			
			#if ii in set(Lower_Freq):
				#d['low_freq']+=1

			if not ii in set(stopwords.words('english')) :
				d[snowball_stem(ii)] += 1
				
				#T = nltk.pos_tag(ii)
				#if T[0][1] in [ 'NN', 'NNP', 'ADJ']:
					#d[T[0][1]] += 1 
				
				"""
				if ii in S_words:
					d['SH'] +=1

				if ii in B_words:
					d['EB'] +=1
				
				if ii in common:
					d['SH'] +=1
					d['EB'] +=1
				"""	
				"""	
				if (ii in S_freq100 or ii in B_freq100):
					d['High_Freq']+=1
					
					d['S_F1']+=1
				if ii in S_freq50:
					d['S_F2']+=1
				if ii in S_freq10:
					d['S_F3']+=1
				if ii in S_freq5:
					d['S_F4']+=1

				if ii in B_freq100:
					d['E_F1']+=1	
				if ii in B_freq50:
					d['E_F2']+=1
				if ii in B_freq10:
					d['E_F3']+=1
				if ii in B_freq5:
					d['E_F4']+=1
				"""	
					
		return d



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

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
	parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
	parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
	parser.add_argument('--subsample', type=float, default=1.0, help='subsample this fraction of total')
	args = parser.parse_args()


	
	trainfile = prepfile(args.trainfile, 'r')

	if args.testfile is not None:
		testfile = prepfile(args.testfile, 'r')
	else:
		testfile = None
	outfile = prepfile(args.outfile, 'w')

	# Create feature extractor (you may want to modify this)
	fe = FeatureExtractor()
	
	# Read in training data
	train = DictReader(trainfile, delimiter='\t')
	
	# Split off dev section
	dev_train = []
	dev_test = []
	full_train = []

	from random import randint
	 
	i = 1
	for ii in train:
		if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
			continue
		feat = fe.features(ii['text'])
		if i ==1:
			print feat
			i=2
		if int(ii['id']) % 5 == 0:
			dev_test.append((feat, ii['cat']))
		else:
			dev_train.append((feat, ii['cat']))
		full_train.append((feat, ii['cat']))

	# Train a classifier
	sys.stderr.write("Training classifier ...\n")
	classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

	right = 0
	total = len(dev_test)
	"""
	sys.stderr.write("No of test samples = %f\n "%total)
	sys.stderr.write("No of dev train samples = %f\n "%len(dev_train))
	sys.stderr.write("No of Total samples = %f\n "%len(full_train))
	"""
	for ii in dev_test:
		prediction = classifier.classify(ii[0])
		if prediction == ii[1]:
			right += 1
	sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))
	

	if testfile is None:
		sys.stderr.write("No test file passed; stopping.\n")
	else:
		# Retrain on all data
		classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

		# Read in test section
		test = {}
		for ii in DictReader(testfile, delimiter='\t'):
			test[ii['id']] = classifier.classify(fe.features(ii['text']))

		# Write predictions
		o = DictWriter(outfile, ['id', 'pred'])
		o.writeheader()
		for ii in sorted(test):
			o.writerow({'id': ii, 'pred': test[ii]})
