import os

import pickle
import torch
import pytorch_lightning as pl

from ..LSTM.lstm import LSTMModel

class Model():
    def __init__(self, model_path, model_name) -> None:
        self.model_path = model_path
        self.model_name = model_name
        if "LSTM" not in model_name:
            self.model = pickle.load(open(os.path.join('model',self.model_path), 'rb'))
        else:
            self.model = LSTMModel.load_from_checkpoint(os.path.join('model/LSTM', self.model_name+'.ckpt'))
        ver = self.model_name.split('_')[-1]
        self.label_encoder = pickle.load(open(os.path.join('model/utils', f"l_{ver}.sav"), 'rb'))

    def predict(self, features):
        if not isinstance(self.model, pl.LightningModule):
            y_pred =  self.model.predict(features)
        else:
            values = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            y_pred = self.model(torch.permute(values, (1, 0 ,2)))
            _, y_pred = torch.max(y_pred, 1)
            y_pred = y_pred.numpy()
        y_pred = self.label_encoder.inverse_transform(y_pred)
        return y_pred
