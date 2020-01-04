import random
import logging

import pymorphy2
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Download packages
nltk.download('punkt')

class Synonimizer():
  def __init__(self, mix_original_words=True, replace_percentage = 50):
    self.replace_percentage = replace_percentage
    self.mix_original_words = mix_original_words
    self.words_base = {}
    self.morph = pymorphy2.MorphAnalyzer()


  def load_synonims_file(self, file_path):
    for line in  open(file_path):
      line_words = line.strip().split('|')
      main_word = line_words[0]
      synonyms = line_words[1:]
      if main_word not in self.words_base:
        self.words_base[main_word] = []
      
      self.words_base[main_word].extend(synonyms)

      if self.mix_original_words and main_word not in self.words_base[main_word]:
        self.words_base[main_word].append(main_word)

  def get_synonym(self, word):
    parsed_word = self.morph.parse(word)[0]
    normal_form = parsed_word.normal_form
    original_form = list(parsed_word.tag._grammemes_tuple)
    
    if normal_form not in self.words_base:
      return word

    random_percent = random.randrange(0, 100)
    if random_percent > self.replace_percentage:
      return word

    new_word_in_normal_form = random.choice(self.words_base[normal_form])
    new_word = self.get_word_target_form(new_word_in_normal_form, original_form)
    logging.debug(f'{word} --> {new_word}')

    if word[0].isupper():
      new_word = new_word.capitalize()

    return new_word

  def get_word_target_form(self, word, form):
    list = []
    list.extend(form)
    intlect_to_remove = ['inan', 'masc', 'NOUN']
    for inflections_to_remove in intlect_to_remove:  
      if inflections_to_remove in list:
        list.remove(inflections_to_remove)
      formed_word = self.morph.parse(word)[0].inflect(set(form))
      if formed_word is not None:
        return formed_word.word
      logging.debug('Invalid reflect to:', word, list)
    return word

  def process_text(self, text):
    tokens = word_tokenize(text)
    new_tokens = map(lambda word: self.get_synonym(word), tokens)
    return TreebankWordDetokenizer().detokenize(new_tokens)
