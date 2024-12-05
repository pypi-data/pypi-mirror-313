# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Preprocessing tools for Urbansound8k data handling on ViT.
"""

__all__ = ["process_dataset"]

import numpy as np
import tensorflow as tf
import librosa


MELSPECS_PARAMS = {
    'n_mels': 128,
    'duration': 4 * 22050,
    'hop_length': 512,
    'n_fft': 2048,
    'fmin': 20
}


def process_dataset(dataset, input_size, mel_params=MELSPECS_PARAMS):
    """ Preprocessing method that loops over the samples, preprocesses each one by computing
        the mel_spectrogram and mfcc features and concatenates theses features in a 2D image that
        is fed to the model. The samples are gathered in a dictionary where the keys are the fold
        ids. Each fold contains two arrays one for the samples and the other for the corresponding
        labels.

    Args:
        dataset (soundata.Dataset): the fully initialized dataset
        input_size (tuple): model input size (X*Y)
        mel_params (dict): audio preprocessing hyperparameters.

    Return:
        dict: the preprocessed samples, split by fold, in a dictionary.
    """
    def process_audio(fp, mel_params, input_size):
        def load_audio(params, file_path):
            y, sr = librosa.load(file_path)
            # clip silence
            yt, _ = librosa.effects.trim(y, top_db=60)
            # pad to length of duration.
            if len(yt) > params['duration']:
                yt = yt[:params['duration']]
            else:
                padding = params['duration'] - len(yt)
                offset = padding // 2
                yt = np.pad(yt, (offset, params['duration'] - len(yt) - offset), 'constant')
            return yt, sr

        def create_melspec(params, audio_data, sampling_rate):
            S = librosa.feature.melspectrogram(y=audio_data,
                                               sr=sampling_rate,
                                               n_mels=params['n_mels'],
                                               hop_length=params['hop_length'],
                                               n_fft=params['n_fft'],
                                               fmin=params['fmin'],
                                               fmax=(sampling_rate // 2))
            Sb = librosa.power_to_db(S, ref=np.max)
            Sb = Sb.astype(np.float32)
            return Sb

        def prepare_feature(feature, in_size):
            feature_normalized = (feature - np.min(feature)) / (np.max(feature) - np.min(feature))
            # expand the shape to move from 2D to 3D
            feature_normalized_3d = np.expand_dims(feature_normalized, -1)
            # resize it to fit the vit default input_shape
            feature_resized = tf.image.resize(feature_normalized_3d, in_size)
            # should not be normalized since the model has its own normalization
            # layers at its beginning.
            feature_ready = tf.cast(255 * feature_resized, tf.uint8)
            return feature_ready

        # Load the wav file
        y, sr = load_audio(mel_params, fp)

        # Compute mel spectrogram
        mel_spectrogram_db = create_melspec(mel_params, y, sr)
        mel_feature = prepare_feature(mel_spectrogram_db, input_size)

        return mel_feature

    dict = {}
    for _, clip in dataset.load_clips().items():
        processed_file = process_audio(clip.audio_path, mel_params, input_size)
        label_id = clip.class_id
        fold_id = clip.fold
        if str(fold_id) not in dict.keys():
            dict[str(fold_id)] = {'samples': [], 'labels': []}
        dict[str(fold_id)]['samples'].append(processed_file)
        dict[str(fold_id)]['labels'].append(label_id)
    return dict
