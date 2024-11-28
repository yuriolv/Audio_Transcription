import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset

# Configuração do dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Dataset personalizado para DataLoader
class ColaDataset(Dataset):
    def __init__(self, sentences, labels, tokenizer, max_len):
        self.sentences = sentences
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        sentence = str(self.sentences[idx])
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            sentence,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'label': torch.tensor(label, dtype=torch.long)
        }

# Carregar CoLA dataset
data = pd.read_csv("train.tsv", sep="\t", header=None, names=["source", "label", "misc", "sentence"])
sentences = data['sentence'].values
labels = data['label'].values

# Dividir em treino e validação
train_sentences, val_sentences, train_labels, val_labels = train_test_split(sentences, labels, test_size=0.1, random_state=42)

# Inicializar tokenizer e dataset
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_dataset = ColaDataset(train_sentences, train_labels, tokenizer, max_len=64)
val_dataset = ColaDataset(val_sentences, val_labels, tokenizer, max_len=64)

# DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# Modelo BERT
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
model.to(device)

# Otimizador
optimizer = AdamW(model.parameters(), lr=5e-5)

# Função de perda
loss_fn = torch.nn.CrossEntropyLoss()

# Loop de treinamento
for epoch in range(6):  # Número de épocas
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()
        optimizer.step()

    print(f"Época {epoch + 1}, Loss: {total_loss / len(train_loader):.4f}")

# Avaliação no conjunto de validação
model.eval()
all_predictions = []
all_labels = []

with torch.no_grad():
    for batch in val_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        
        all_predictions.extend(predictions.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Relatório de métricas
print(classification_report(all_labels, all_predictions, target_names=["Incorreta", "Correta"]))

# Diretório onde o modelo será salvo
save_directory = "./bert_classificador"

# Salva o modelo treinado
model.save_pretrained(save_directory)

# Salva o tokenizer
tokenizer.save_pretrained(save_directory)
