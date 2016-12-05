# -*- coding: UTF-8 -*-
import cProfile
pr = cProfile.Profile()
pr.enable()

import sys
import re
import unicodedata
import psycopg2
from gensim import corpora, models
from collections import Counter
import numpy as np
from sklearn.externals import joblib
import warnings
warnings.filterwarnings("ignore")

error=0
if error==0:
    try:
        # Set only one time.
        click = int(sys.argv[1])
        path = str(sys.argv[2])
        get_conn = psycopg2.connect(dbname=sys.argv[4],user=sys.argv[5], host=sys.argv[3], password=sys.argv[6])
        

        #click = 1
        #path = u"/home/terence/Downloads/data/"
        #get_conn = psycopg2.connect(dbname='Demo DB',user='postgres', host='localhost', password='postgres')
        get_conn.autocommit = True
        get_cur  = get_conn.cursor()
    except:
        print "connect DB error."
        error = 1
        raise 

if error==0:
    try:
        dictionary = corpora.Dictionary.load(path+"all_lda_dictionary.dict")
        lda = models.LdaModel.load(path + "all_lda_50.model")
    except:
        print "Load lda model error."
        error = 1
        raise 

if error==0:
    try:
    # I'm 1_regular.py
        column = ["text_0", "text_1", "text_2", "text_3", "text_4", "text_5", "text_6", "text_7", "text_8", "text_9", "text_10",
                  "text_11"]

        get_cur.execute("Select " + ",".join(column[0:1 + click]) + " From basic")
        raw_table = get_cur.fetchall()
	if  len(sys.argv)==8:
            original = sys.argv[7]
	else:
            original = " ".join(raw_table[0])

        onix1 = set([u"a", u"a's", u"able", u"about", u"above", u"according", u"accordingly", u"across", u"actually", u"after",
                     u"afterwards", u"again", u"against", u"ain't", u"all", u"allow", u"allows", u"almost", u"alone", u"along",
                     u"already", u"also", u"although", u"always", u"am", u"among", u"amongst", u"an", u"and", u"another",
                     u"any", u"anybody", u"anyhow", u"anyone", u"anything", u"anyway", u"anyways", u"anywhere", u"apart", u"appear",
                     u"appreciate", u"appropriate", u"are", u"aren't", u"around", u"as", u"aside", u"ask", u"asking",
                     u"associated",
                     u"at", u"available", u"away", u"awfully", u"b", u"be", u"became", u"because", u"become", u"becomes",
                     u"becoming",
                     u"been", u"before", u"beforehand", u"behind", u"being", u"believe", u"below", u"beside", u"besides",
                     u"best",
                     u"better", u"between", u"beyond", u"both", u"brief", u"but", u"by", u"c", u"c'mon", u"c's", u"came",
                     u"can", u"can't",
                     u"cannot", u"cant", u"cause", u"causes", u"certain", u"certainly", u"changes", u"clearly", u"co", u"com",
                     u"come",
                     u"comes", u"concerning", u"consequently", u"consider", u"considering", u"contain", u"containing",
                     u"contains",
                     u"corresponding", u"could", u"couldn't", u"course", u"currently", u"d", u"definitely", u"described",
                     u"despite",
                     u"did", u"didn't", u"different", u"do", u"does", u"doesn't", u"doing", u"don't", u"done", u"down",
                     u"downwards",
                     u"during", u"e", u"each", u"edu", u"eg", u"eight", u"either", u"else", u"elsewhere", u"enough",
                     u"entirely",
                     u"especially", u"et", u"etc", u"even", u"ever", u"every", u"everybody", u"everyone", u"everything",
                     u"everywhere",
                     u"ex", u"exactly", u"example", u"except", u"f", u"far", u"few", u"fifth", u"first", u"five", u"followed",
                     u"following", u"follows", u"for", u"former", u"formerly", u"forth", u"four", u"from", u"further",
                     u"furthermore",
                     u"g", u"get", u"gets", u"getting", u"given", u"gives", u"go", u"goes", u"going", u"gone", u"got",
                     u"gotten",
                     u"greetings", u"h", u"had", u"hadn't", u"happens", u"hardly", u"has", u"hasn't", u"have", u"haven't",
                     u"having",
                     u"he", u"he's", u"hello", u"help", u"hence", u"her", u"here", u"here's", u"hereafter", u"hereby",
                     u"herein",
                     u"hereupon", u"hers", u"herself", u"hi", u"him", u"himself", u"his", u"hither", u"hopefully", u"how",
                     u"howbeit",
                     u"however", u"i", u"i'd", u"i'll", u"i'm", u"i've", u"ie", u"if", u"ignored", u"immediate", u"in",
                     u"inasmuch",
                     u"inc", u"indeed", u"indicate", u"indicated", u"indicates", u"inner", u"insofar", u"instead", u"into",
                     u"inward",
                     u"is", u"isn't", u"it", u"it'd", u"it'll", u"it's", u"its", u"itself", u"j", u"just", u"k", u"keep",
                     u"keeps", u"kept",
                     u"know", u"knows", u"known", u"l", u"last", u"lately", u"later", u"latter", u"latterly", u"least", u"less",
                     u"lest",
                     u"let", u"let's", u"like", u"liked", u"likely", u"little", u"look", u"looking", u"looks", u"ltd", u"m",
                     u"mainly",
                     u"many", u"may", u"maybe", u"me", u"mean", u"meanwhile", u"merely", u"might", u"more", u"moreover",
                     u"most",
                     u"mostly", u"much", u"must", u"my", u"myself", u"n", u"name", u"namely", u"nd", u"near", u"nearly",
                     u"necessary",
                     u"need", u"needs", u"neither", u"never", u"nevertheless", u"new", u"next", u"nine", u"no", u"nobody",
                     u"non", u"none",
                     u"noone", u"nor", u"normally", u"not", u"nothing", u"novel", u"now", u"nowhere", u"o", u"obviously", u"of",
                     u"off",
                     u"often", u"oh", u"ok", u"okay", u"old", u"on", u"once", u"one", u"ones", u"only", u"onto", u"or",
                     u"other", u"others",
                     u"otherwise", u"ought", u"our", u"ours", u"ourselves", u"out", u"outside", u"over", u"overall", u"own",
                     u"p",
                     u"particular", u"particularly", u"per", u"perhaps", u"placed", u"please", u"plus", u"possible",
                     u"presumably",
                     u"probably", u"provides", u"q", u"que", u"quite", u"qv", u"r", u"rather", u"rd", u"re", u"really",
                     u"reasonably",
                     u"regarding", u"regardless", u"regards", u"relatively", u"respectively", u"right", u"s", u"said", u"same",
                     u"saw",
                     u"say", u"saying", u"says", u"second", u"secondly", u"see", u"seeing", u"seem", u"seemed", u"seeming",
                     u"seems",
                     u"seen", u"self", u"selves", u"sensible", u"sent", u"serious", u"seriously", u"seven", u"several",
                     u"shall", u"she",
                     u"should", u"shouldn't", u"since", u"six", u"so", u"some", u"somebody", u"somehow", u"someone",
                     u"something",
                     u"sometime", u"sometimes", u"somewhat", u"somewhere", u"soon", u"sorry", u"specified", u"specify",
                     u"specifying",
                     u"still", u"sub", u"such", u"sup", u"sure", u"t", u"t's", u"take", u"taken", u"tell", u"tends", u"th",
                     u"than",
                     u"thank", u"thanks", u"thanx", u"that", u"that's", u"thats", u"the", u"their", u"theirs", u"them",
                     u"themselves",
                     u"then", u"thence", u"there", u"there's", u"thereafter", u"thereby", u"therefore", u"therein", u"theres",
                     u"thereupon", u"these", u"they", u"they'd", u"they'll", u"they're", u"they've", u"think", u"third",
                     u"this",
                     u"thorough", u"thoroughly", u"those", u"though", u"three", u"through", u"throughout", u"thru", u"thus",
                     u"to",
                     u"together", u"too", u"took", u"toward", u"towards", u"tried", u"tries", u"truly", u"try", u"trying",
                     u"twice",
                     u"two", u"u", u"un", u"under", u"unfortunately", u"unless", u"unlikely", u"until", u"unto", u"up", u"upon",
                     u"us",
                     u"use", u"used", u"useful", u"uses", u"using", u"usually", u"uucp", u"v", u"value", u"various", u"very",
                     u"via",
                     u"viz", u"vs", u"w", u"want", u"wants", u"was", u"wasn't", u"way", u"we", u"we'd", u"we'll", u"we're",
                     u"we've",
                     u"welcome", u"well", u"went", u"were", u"weren't", u"what", u"what's", u"whatever", u"when", u"whence",
                     u"whenever",
                     u"where", u"where's", u"whereafter", u"whereas", u"whereby", u"wherein", u"whereupon", u"wherever",
                     u"whether",
                     u"which", u"while", u"whither", u"who", u"who's", u"whoever", u"whole", u"whom", u"whose", u"why", u"will",
                     u"willing", u"wish", u"with", u"within", u"without", u"won't", u"wonder", u"would", u"would", u"wouldn't",
                     u"x",
                     u"y", u"yes", u"yet", u"you", u"you'd", u"you'll", u"you're", u"you've", u"your", u"yours", u"yourself",
                     u"yourselves", u"z", u"zero"])
        contractions_rep = [(r"won\'t", 'will not'),(r"can\'t", 'cannot'),(r"i\'m", 'i am'),(r"ain\'t", 'is not'),
                            (r"(\w+)\'ll", '\g<1> will'),(r"(\w+)n\'t", '\g<1> not'),(r"(\w+)\'ve", '\g<1> have'),
                            (r"(\w+)\'s", '\g<1> is'),(r"(\w+)\'re", '\g<1> are'),(r"(\w+)\'d", '\g<1> would'),
                            (r"gonna", 'going to'),(r"wanna", 'want to'),(r"o'clock", 'of the clock'),(r"'tis", 'it is'),
                            (r"'twas", 'it was'),(r"y'all", 'you all')]
        contractions_list=[]
        for (regex, repl) in contractions_rep:
            contractions_list.append((re.compile(regex), repl))


        def regular_word(content):
            # 1. Convert diacritics words
            content = unicode(content, 'utf-8')
            content = unicodedata.normalize('NFD', content)
            content = content.encode('ascii', 'ignore')

            # 2. Convert english contractions
            for (pattern, repl) in contractions_list:
                (content, count) = re.subn(pattern, repl, content)

            # 3. Remove non-numbers and non-letters
            content = re.sub("[^a-zA-Z]", " ", content)

            # 4. Convert words to lower case
            content = content.lower()

            # 5. Split words
            content = content.split()

            # 6. Optionally remove stop words (false by default)
            content = [w for w in content if not w in onix1]

            return content

        regulated = regular_word(original)
    except:
        print "1_regular part error."
        error = 1
        raise 

if error==0:
    try:
    # I'm 2_1_wordcount.py
        length = float(len(regulated))
        counts = Counter(regulated)

        words= [[1,"icp","dilantin","head","neuro","mri","mm","stroke","hospital","sbp","reactive","hemorrhage","pupils","checks","ct","left","sah","extremities","commands","exam","sdh"],
                      [3, "left", "carotid", "cerebral", "vertebral", "cta", "angiogram", "common", "embolization", "amt",
                       "internal", "evidence", "procedural", "order", "clip", "service", "artery", "identifier", "aneurysm",
                       "arteries", "numeric"],
                      [7, "injury", "anoxic", "cooling", "blanket", "vf", "vt", "cpr", "atropine", "colostomy", "intubated",
                       "protocol", "code", "unresponsive", "eeg", "brain", "arrest", "pea", "sun", "cardiac", "bradycardia"],
                      [12, "bipap", "hospital", "respiratory", "copd", "sputum", "rr", "admitted", "transferred", "cxr",
                       "pulmonary", "resp", "ed", "distress", "pe", "micu", "ct", "nebs", "pna", "pneumonia", "chest"],
                      [13, "water", "dnr", "ns", "baseline", "hematuria", "tract", "urine", "dni", "daughter", "free",
                       "hyponatremia", "uti", "foley", "cc", "na", "dementia", "sodium", "bladder", "urinary", "urology"],
                      [21, "pain", "monitor", "ccu", "ct", "min", "pa", "ci", "insulin", "weaned", "pulses", "wean", "gtt",
                       "mcg", "pacer", "kg", "iabp", "lasix", "sbp", "neo", "started"],
                      [28, "remains", "fentanyl", "sedation", "cc", "wean", "mcg", "propofol", "gtt", "abg", "increased",
                       "intubated", "bp", "secretions", "peep", "pt", "sedated", "hr", "vent", "mg", "min"],
                      [31, "pressors", "wbc", "sepsis", "shock", "blood", "infection", "septic", "lactate", "map", "zosyn",
                       "cvp", "levophed", "cultures", "fluid", "line", "hypotension", "bacteremia", "hypotensive", "vanco",
                       "cx"],
                      [34, "po", "airway", "aspiration", "protect", "gag", "eval", "secretions", "swallowing", "inability",
                       "clearance", "cough", "thin", "liquids", "stent", "evaluation", "tracheal", "risk", "swallow", "oral",
                       "speech"],
                      [49, "scale", "units", "doses", "regular", "line", "prn", "insulin", "ml", "hr", "po", "iv", "mg", "bid",
                       "date", "daily", "sc", "sliding", "tid", "drip", "order"]]
        length = float(len(regulated))
        counts = Counter(regulated)


        wordcount_count = ""
        wordcount_perce = ""
        for i in range(0,10):
            wordcount_count += "When "+ str(words[i][0]) + " Then Case word "
            wordcount_perce += "When "+ str(words[i][0]) + " Then Case word "
            for j in range(1,21):
                wordcount_count += "When '" + words[i][j] + "' Then " + str(counts[words[i][j]]) + " "
                wordcount_perce += "When '" + words[i][j] + "' Then " + str(counts[words[i][j]]/length) + " "
            wordcount_count += "End "
            wordcount_perce += "End "

        wordcount_text  = "update WORDCOUNT set count_" + str(click) + " = Case topic_id "
        wordcount_text += wordcount_count + " End, "
        wordcount_text += "percent_" + str(click) + " = Case topic_id "
        wordcount_text += wordcount_perce + " End "
        wordcount_text += "Where topic_id in (1,3,7,12,13,21,28,31,24,49); "
        get_cur.execute(wordcount_text)

    except:
        print "2_1_wordcount part error."
        error = 1
        raise 

if error==0:
    try:
    # I'm 2_2_text2topic.py
        vec_bow = dictionary.doc2bow(regulated)
        vec_lsi = lda.__getitem__(vec_bow, eps=0)

        update_text = "update TEXT2TOPIC set proportion_" + str(click) + " = Case topic_id "
        for i in range(0,50):
            update_text += "When " + str(vec_lsi[i][0] + 1) + " Then " + str(float(vec_lsi[i][1])) +" "
        get_cur.execute(update_text+" end;")
    except:
        print "2_2_text2topic part error."
        error = 1
        raise 

if error==0:
    try:
    # I'm 3_2_svm.py
        get_cur.execute("Select basic.age, basic.gender, basic.sapsii_first from basic")
        basictable = get_cur.fetchall()
        if basictable[0][1] == 'M':
            gender = 1
        else:
            gender = 0
        newx=[float(basictable[0][0]),gender,float(basictable[0][2])]

        get_cur.execute("Select proportion_"+str(click)+" from text2topic")
        text2topictable = get_cur.fetchall()
        for row in text2topictable:
            newx.append(float(row[0]))

        use_all = False
        if use_all == True:
            svr_in = joblib.load(path + "svr_in_50.pkl")
        elif click == 0:
            svr_in = joblib.load(path + "svr_in_12.pkl")
        else:
            svr_in = joblib.load(path + "svr_in_"+str(click*12)+".pkl")

        get_cur.execute("update svm set survival_"+str(click)+" = "+str(1-float(svr_in.predict(np.array(newx).reshape(1,53))))+" where patient_id = 26429")
    except:
        print "3_2_svm part error."
        error = 1
        raise 



# End.


pr.disable()
if error==0:
    print "0_all_in_one.py " + str(click) + " end."
    #pr.print_stats(sort="tottime")
