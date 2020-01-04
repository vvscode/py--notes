import nltk
# import grammar_check
from googletrans import Translator
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer


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

Vostok 1 was Gagarin's only spaceflight but he served as the backup 
crew to the Soyuz 1 mission, which ended in a fatal crash, killing 
his friend and fellow cosmonaut Vladimir Komarov. Fearing for his 
life, Soviet officials permanently banned Gagarin from further 
spaceflights, but he advocated to be allowed to fly regular aircraft 
which he was permitted to do after completing his education at the 
Zhukovsky Air Force Engineering Academy on 17 February 1968. Gagarin 
died five weeks later when the MiG-15 training jet he was piloting 
with his flight instructor Vladimir Seryogin crashed near the town 
of Kirzhach.
'''


sentences = nltk.sent_tokenize(text)

# # sent_0 = sentences[0]
# #
# # words = nltk.word_tokenize(sent_0)
# #
# word = 'completed'
# #
# # rword = 'окончил'
#
# lemmatizer = WordNetLemmatizer()
#
# lword = lemmatizer.lemmatize(word)
#
#
# # print(lword)
# #
# # breakpoint()
#
#
# ps = PorterStemmer()
# base = ps.stem(word)
#
# # ss = SnowballStemmer("russian")
# # rbase = ss.stem(rword)
#
# # print(rbase)
#
# result_dict = {}
#
# swords = stopwords.words('english')
#
# ngrams = nltk.ngrams(nltk.word_tokenize(text), 5)
#
# parts = []
#
# for words_tuple in ngrams:
#     # flag = False
#     # for w in words_tuple:
#     #     if (w in swords) or (w in punctuation):
#     #         flag = True
#     # if flag:
#     #     continue
#     phrase = ' '.join(words_tuple)
#     parts.append(phrase)
#
# print(parts)

# for words_tuple in bigrams:
#
#     flag = False
#
#     for w in words_tuple:
#         if (w in swords) or (w in punctuation):
#             flag = True
#
#     if flag:
#         continue
#
#     word = ' '.join(words_tuple)
#
#     # word = ps.stem(word)
#     if word in result_dict:
#         result_dict[word] += 1
#     else:
#         result_dict[word] = 1
#
#
# for word in result_dict:
#     result_dict[word] = result_dict[word] / len(result_dict) * 100
#     result_dict[word] = round(result_dict[word], 3)
#
#
# sorted_words = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)[:10]
#
#
# print(sorted_words)

#
# tool = grammar_check.LanguageTool('en-GB')
# matches = tool.check(sentences[0])
#
# print(matches)
#
# breakpoint()


translator = Translator()

result = translator.translate(text, dest='ru')


# from gtrans import translate_text
#
#
# result = translate_text(text, lt='ru', lf='en')

print(result)

