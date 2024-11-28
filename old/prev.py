import torch
from transformers import BertTokenizer, BertForSequenceClassification


load_directory = "./bert_classificador"

# Carrega o modelo
model = BertForSequenceClassification.from_pretrained(load_directory)

# Carrega o tokenizer
tokenizer = BertTokenizer.from_pretrained(load_directory)

# Configuração do dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Frase para classificação
sentence = "I had two dogs and one cat."
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenizar a entrada
inputs = tokenizer.encode_plus(
    sentence,
    max_length=64,
    padding='max_length',
    truncation=True,
    return_tensors="pt"
)

# Mover para o dispositivo (GPU ou CPU)
input_ids = inputs['input_ids'].to(device)
attention_mask = inputs['attention_mask'].to(device)

# Fazer a previsão
model.eval()
with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1)  # Para classificação binária ou multiclasse

print(f"Classe prevista: {prediction.item()}")
