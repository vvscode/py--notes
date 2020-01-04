import nltk
import language_check
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation


text = '''
Yuri Alekseyevich Gagarin [a] (9 March 1934 – 27 March 1968) was a Soviet 
Air Forces pilot and cosmonaut who became the first human to journey 
into outer space, achieving a major milestone in the Space Race; his 
capsule Vostok 1 completed one orbit of Earth on 12 April 1961. Gagarin 
became an international celebrity and was awarded many medals and titles, 
including Hero of the Soviet Union, his nation's highest honour.

Born in the village of Klushino near a town later renamed after 
him, in his youth Gagarin was a foundryman at a steel plant in Lyubertsy. 
He later joined the Soviet Air Forces as a pilot and was stationed in 
Luostari near the Norwegian border before selection for the Soviet space 
program with five other cosmonauts. Following his spaceflight, Gagarin 
became deputy training director of the Cosmonaut Training Centre, which 
was later named after him. He was also elected as a deputy of the Soviet 
of the Union in 1962 and then to the Soviet of Nationalities, respectively 
the lower and upper chambers of the Supreme Soviet.
'''


title = 'Tis the Season for Reporting (And a New Mini Guide)'


en_stemer = SnowballStemmer('english')
en_lemma = WordNetLemmatizer()

# sentences = nltk.sent_tokenize(text)
words = nltk.word_tokenize(text)
stop_words = set(stopwords.words('english'))

cleaned_words = []

result = dict()

for w in words:
    if w in punctuation:
        continue
    # if w in stop_words:
    #     continue
    # word_stemed = en_stemer.stem(w)
    cleaned_words.append(w)

    # if word_stemed not in result:
    #     result[word_stemed] = 1
    # else:
    #     result[word_stemed] += 1



# word_freq = sorted(result.items(), key=lambda x: x[1], reverse=True)[:5]
#
# print(word_freq)

# grams5 = list(ngrams(cleaned_words, 5))
#
# grams5_text = [' '.join(x) for x in grams5]
#
# print(grams5_text, len(grams5_text))

# print(cleaned_words, len(cleaned_words))


tool = language_check.LanguageTool('ru-RU')

text = 'Я хочу применяю PYTHON для SEO.'

matches = tool.check(text)

print(len(matches))
print(matches)
