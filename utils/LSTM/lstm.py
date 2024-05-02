import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import pytorch_lightning as pl
from torch.autograd import Variable
import pandas as pd
from lightning.pytorch.callbacks.early_stopping import EarlyStopping
RANDOM_STATE = 42
pl.seed_everything(RANDOM_STATE, workers=True)

class CICIDSDataset(Dataset):
  def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
    self.X = X
    self.y = y
  def __len__(self):
    return len(self.X)

  def __getitem__(self, idx):
    return torch.tensor(self.X.iloc[idx], dtype=torch.float32).unsqueeze(0), torch.tensor(self.y[idx], dtype=torch.int64)


class LSTMModel(pl.LightningModule):
  def __init__(self, input_size, hidden_size, num_layers, num_classes, learning_rate):
    super().__init__()
    self.hidden_size = hidden_size
    self.num_layers = num_layers
    self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
    self.fc = nn.Linear(hidden_size, num_classes)
    self.relu = nn.ReLU()
    self.learning_rate = learning_rate

  def forward(self, x):

    h0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(self.device))
    c0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(self.device))
    out, (hn, cn) = self.lstm(x, (h0, c0))
    hn = hn.view(-1, self.hidden_size)
    out = self.relu(hn)
    out = self.fc(out)
    return out

  def training_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self(x)
    loss = F.cross_entropy(y_hat, y)
    self.log('train_loss', loss, on_step=True, on_epoch=False, prog_bar=True)
    return loss

  def validation_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self(x)
    loss = F.cross_entropy(y_hat, y)
    self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
    return loss

  def test_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self(x)
    loss = F.cross_entropy(y_hat, y)
    self.log('test_loss', loss)
    return loss

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=self.learning_rate)
