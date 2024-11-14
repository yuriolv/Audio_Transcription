from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("prithivida/grammar_error_correcter_v1")
tokenizer = AutoTokenizer.from_pretrained("prithivida/grammar_error_correcter_v1")


def corrigir_texto(texto):
    # Prepara o texto para o modelo
    inputs = tokenizer.encode('gec: ' + texto, return_tensors="pt", max_length=512, truncation=True)

    # Gera a correção
    outputs = model.generate(inputs, max_length=512, num_beams=5, early_stopping=True)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected_text
