SonusAI: Framework for simplified creation of deep NN models for sound, speech, and voice AI

SonusAI includes functions for pre-processing training and validation data and
creating performance metrics reports for key types of Keras models:
- recurrent, convolutional, or a combination (i.e. RCNNs)
- binary, multiclass single-label, multiclass multi-label, and regression
- training with data augmentations:  noise mixing, pitch and time stretch, etc.

SonusAI python functions are used by:
 - Aaware Inc. sonusai framework:   Easily create train/validation data, run prediction, evaluate model performance
 - Keras model scripts:             User python scripts for Keras model creation, training, and prediction. These can use sonusai-specific data but also some general useful utilities for training rnn-based models like CRNN's, DSCRNN's, etc. in Keras.
