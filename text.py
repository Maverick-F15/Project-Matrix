from transformers import MarianMTModel, MarianTokenizer

def translate_english_to_hindi(text):
    model_name = "Helsinki-NLP/opus-mt-en-hi"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer.encode(">>en<<" + text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2)

    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

english_text = "Hello, how are you?"
translated_text = translate_english_to_hindi(english_text)
print("Translated text in Hindi:", translated_text)
