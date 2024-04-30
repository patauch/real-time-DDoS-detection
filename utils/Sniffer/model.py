import pickle
import torch
import pytorch_lightning as pl

class Model():
    def __init__(self, model_path, model_name) -> None:
        self.model_path = model_path
        self.model_name = model_name
        self.model = pickle.load(open(self.model_path, 'rb'))

    def predict(self, features):
        if not isinstance(self.model, pl.LightningModule):
            return self.model.predict(features)
        else:
            values = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            y_pred = self.model(torch.permute(values, 1, 0 ,2))
            _, y_pred = torch.max(y_pred, 1)
            y_pred = y_pred.numpy()
            return y_pred
