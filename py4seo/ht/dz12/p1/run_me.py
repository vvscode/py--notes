from synonimizer import Synonimizer

processor = Synonimizer(
  mix_original_words=False, # Do not add original words on randomizing
  replace_percentage=40 # Keep part of original text with no changes
)
processor.load_synonims_file('dicts/synmaster.utf8.txt')

with open('input/gagrin.txt') as input_file:
  text = input_file.read().strip()

alter_text = processor.process_text(text)

with open('output/gagrin.txt', 'w') as output_file:
  output_file.write(str(alter_text))

print("Done:")
print(alter_text)