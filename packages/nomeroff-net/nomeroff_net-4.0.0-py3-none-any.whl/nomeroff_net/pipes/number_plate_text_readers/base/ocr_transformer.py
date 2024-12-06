# pip install pytorch-lightning torch torchvision timm

import torch
import torch.nn as nn
import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import string

# Список символів для OCR (номерних знаків)
CHARS = string.ascii_uppercase + string.digits  # Літери та цифри
CHAR2IDX = {ch: idx for idx, ch in enumerate(CHARS)}
IDX2CHAR = {idx: ch for ch, idx in CHAR2IDX.items()}

# Параметри моделі
IMG_SIZE = (128, 32)  # Розмір вирізаного зображення номерного знака
MAX_LEN = 8  # Максимальна кількість символів в номері
VOCAB_SIZE = len(CHARS)
BATCH_SIZE = 16
LR = 1e-4


# Підготовка датасету
class LicensePlateDataset(Dataset):
    def __init__(self, data_paths, labels, transform=None):
        self.data_paths = data_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.data_paths)

    def __getitem__(self, idx):
        image = Image.open(self.data_paths[idx]).convert("RGB")
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        label_idx = [CHAR2IDX[c] for c in label]  # Перетворення тексту в індекси
        return image, torch.tensor(label_idx, dtype=torch.long)

transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,)),
])

# Vision Transformer для екстракції ознак
class ViTEncoder(nn.Module):
    def __init__(self, img_size=IMG_SIZE, patch_size=16, embed_dim=256, num_heads=8, num_layers=6):
        super(ViTEncoder, self).__init__()
        self.model = timm.create_model('vit_base_patch16_224', pretrained=True)
        self.model.head = nn.Identity()  # Видаляємо класифікатор

    def forward(self, x):
        return self.model(x)

# Трансформер для розпізнавання символів
class TransformerOCR(pl.LightningModule):
    def __init__(self, vocab_size, max_len, lr=LR):
        super(TransformerOCR, self).__init__()
        self.save_hyperparameters()

        self.encoder = ViTEncoder()

        self.embedding = nn.Embedding(vocab_size, 256)
        self.transformer = nn.Transformer(d_model=256, nhead=8, num_encoder_layers=6, num_decoder_layers=6)
        self.fc_out = nn.Linear(256, vocab_size)
        self.loss_fn = nn.CrossEntropyLoss()

        self.lr = lr

    def forward(self, images, labels=None):
        # Екстракція ознак зображення
        enc_output = self.encoder(images)

        # Якщо є мітки для тренування
        if labels is not None:
            labels = self.embedding(labels)
            dec_output = self.transformer(enc_output.unsqueeze(0), labels.unsqueeze(0))
            logits = self.fc_out(dec_output)
            return logits.squeeze(0)

        # Якщо тільки інференс
        return enc_output

    def training_step(self, batch, batch_idx):
        images, labels = batch
        logits = self(images, labels[:, :-1])  # Виключаємо останній токен
        loss = self.loss_fn(logits.view(-1, VOCAB_SIZE), labels[:, 1:].view(-1))  # Порівнюємо з наступним токеном
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)


# Тренувальний скрипт
if __name__ == '__main__':
    # Приклад даних
    data_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]  # Шляхи до вирізаних зображень
    labels = ["ABC123", "XYZ789"]  # Мітки з текстом номерних знаків

    dataset = LicensePlateDataset(data_paths, labels, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = TransformerOCR(vocab_size=VOCAB_SIZE, max_len=MAX_LEN)

    trainer = pl.Trainer(max_epochs=10, gpus=1)
    trainer.fit(model, dataloader)
