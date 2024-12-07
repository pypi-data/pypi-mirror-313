# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Tue Feb 27 2024


import tensorflow as tf
from tqdm import tqdm


class EpochProgressCallback(tf.keras.callbacks.Callback):
    """
    Class to implement a tqdm progress bar over epochs, written by ChatGPT, provided by
    Arne Thomsen
    """

    def __init__(self, total_epochs):
        super().__init__()
        self.total_epochs = total_epochs
        self.pbar = None

    def on_train_begin(self, logs=None):
        self.pbar = tqdm(total=self.total_epochs, desc="epoch")

    def on_epoch_end(self, epoch, logs=None):
        self.pbar.update(1)

        if logs is not None:
            loss = logs.get("loss")
            val_loss = logs.get("val_loss")
            lr = logs.get("lr")

            self.pbar.set_postfix({"loss": loss, "val_loss": val_loss, "lr": lr})

    def on_train_end(self, logs=None):
        self.pbar.close()
