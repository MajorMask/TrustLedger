from transformers import MarianMTModel, MarianTokenizer

@tobedecided
input = [
    "Bárcsak ne láttam volna ilyen borzalmas filmet!",
    "Iskolában van."
]

model_name = "pytorch-models/opus-mt-tc-big-hu-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))

for t in translated:
    print( tokenizer.decode(t, skip_special_tokens=True) )

# expected output:
#     I wish I hadn't seen such a terrible movie.
#     She's at school.

