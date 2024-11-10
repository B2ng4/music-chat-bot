import tensorflow as tf
import librosa
import numpy as np
import soundfile as sf
from keras.layers import Input, Bidirectional, LSTM, Dense, TimeDistributed, Dropout
from keras.models import Model
from keras import regularizers  # Импортируем регуляризаторы
from transformers import BertTokenizer, TFBertModel
import logging
import random
import os
from functools import lru_cache
import texts as txt

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class SingingModel:
    def __init__(self):
        self.SAMPLING_RATE = 22050
        self.N_MEL_CHANNELS = 80
        self.MAX_TEXT_LENGTH = 100
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.encoder = self._build_encoder()
        self.decoder = self._build_decoder()
        self.model = self._build_full_model()
        self.audio_cache = {}
        self.text_cache = {}
        self.model_checkpoint_path = 'checkpoints/best_model.h5'
        self.load_weights()

    def load_weights(self):
        if os.path.exists(self.model_checkpoint_path):
            self.model.load_weights(self.model_checkpoint_path)
            logging.info(f"Весы загружены из {self.model_checkpoint_path}")
        else:
            logging.warning(f"Файл весов не найден: {self.model_checkpoint_path}")

    @lru_cache(maxsize=512)
    def prepare_text(self, text):
        inputs = self.tokenizer(text, return_tensors="tf", padding="max_length", max_length=self.MAX_TEXT_LENGTH, truncation=True)
        sequence_array = tf.squeeze(inputs['input_ids'])
        return sequence_array.numpy()

    def prepare_audio(self, audio_path, augment=True):
        if audio_path in self.audio_cache:
            return self.audio_cache[audio_path]

        try:
            audio, sr = librosa.load(audio_path, sr=self.SAMPLING_RATE, mono=True)
            if augment:
                audio = self.augment_audio(audio)
            audio = librosa.util.normalize(audio)
            audio_trimmed, _ = librosa.effects.trim(audio, top_db=30)

            if random.random() < 0.1:
                pause_duration = int(self.SAMPLING_RATE * 0.5)
                insert_position = random.randint(0, len(audio_trimmed) - pause_duration)
                audio_trimmed = np.insert(audio_trimmed, insert_position, np.zeros(pause_duration))

            if len(audio_trimmed) < self.MAX_TEXT_LENGTH:
                return None

            mel_spectrogram = librosa.feature.melspectrogram(
                y=audio_trimmed,
                sr=self.SAMPLING_RATE,
                n_mels=self.N_MEL_CHANNELS,
                power=1.0
            )
            mel_spectrogram = np.log(np.clip(mel_spectrogram, a_min=1e-5, a_max=None))

            if mel_spectrogram.shape[1] > self.MAX_TEXT_LENGTH:
                mel_spectrogram = mel_spectrogram[:, :self.MAX_TEXT_LENGTH]
            elif mel_spectrogram.shape[1] < self.MAX_TEXT_LENGTH:
                pad_width = ((0, 0), (0, self.MAX_TEXT_LENGTH - mel_spectrogram.shape[1]))
                mel_spectrogram = np.pad(mel_spectrogram, pad_width, mode='constant')

            self.audio_cache[audio_path] = mel_spectrogram
            return mel_spectrogram
        except Exception as e:
            logging.error(f"Ошибка при обработке {audio_path}: {e}")
            return None

    def create_dataset(self, texts, audio_paths, batch_size, augment=True):
        def generator():
            for text, path in zip(texts, audio_paths):
                x = self.prepare_text(text)
                y = self.prepare_audio(path, augment=augment)
                if y is None or y.shape[0] != self.N_MEL_CHANNELS:
                    continue
                yield x, y

        dataset = tf.data.Dataset.from_generator(
            generator,
            output_signature=(
                tf.TensorSpec(shape=(self.MAX_TEXT_LENGTH,), dtype=tf.int32),
                tf.TensorSpec(shape=(self.N_MEL_CHANNELS, self.MAX_TEXT_LENGTH), dtype=tf.float32)
            )
        )

        return dataset.batch(batch_size).shuffle(1000).prefetch(tf.data.experimental.AUTOTUNE)

    def _build_encoder(self):
        inputs = Input(shape=(self.MAX_TEXT_LENGTH,), dtype=tf.int32)
        bert_model = TFBertModel.from_pretrained('bert-base-uncased', output_hidden_states=False)
        bert_output = bert_model(inputs)[0]
        return Model(inputs=inputs, outputs=bert_output)

    def augment_audio(self, audio):
        if random.random() > 0.5:
            pitch_shift = random.randint(-2, 2)
            audio = librosa.effects.pitch_shift(audio, sr=self.SAMPLING_RATE, n_steps=pitch_shift)
        if random.random() > 0.5:
            speed_change = random.uniform(0.9, 1.1)
            audio = librosa.effects.time_stretch(audio, rate=speed_change)
        if random.random() > 0.5:
            noise = np.random.randn(len(audio)) * 0.005
            audio = audio + noise
        if random.random() > 0.5:
            volume_change = random.uniform(0.7, 1.3)
            audio = audio * volume_change
        return audio

    def _build_decoder(self):
        inputs = Input(shape=(None, 768))
        x = TimeDistributed(Dense(256, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.001, l2=0.001)))(inputs)
        x = Dropout(0.2)(x)
        x = Bidirectional(LSTM(256, return_sequences=True, kernel_regularizer=regularizers.l1_l2(l1=0.001, l2=0.001)))(x)
        x = Dropout(0.2)(x)
        x = TimeDistributed(Dense(self.N_MEL_CHANNELS, activation='linear', kernel_regularizer=regularizers.l1_l2(l1=0.001, l2=0.001)))(x)  # Активируем линейно, так как это регрессия
        return Model(inputs=inputs, outputs=x)

    def _build_full_model(self):
        text_inputs = Input(shape=(self.MAX_TEXT_LENGTH,), dtype=tf.int32)
        encoded = self.encoder(text_inputs)

        mel_outputs = self.decoder(encoded)
        mel_outputs = tf.transpose(mel_outputs, perm=[0, 2, 1])

        model = Model(inputs=text_inputs, outputs=mel_outputs)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="mae",  # Изменение на Huber Loss
            metrics=['mae']
        )
        return model

    def train(self, texts, audio_paths, epochs=100, batch_size=1, validation_data=None):
        dataset = self.create_dataset(texts, audio_paths, batch_size, augment=True)
        for x, y in dataset.take(1):
            logging.info(f"Input shape: {x.shape}, Output shape: {y.shape}")

        num_examples = sum(1 for _ in dataset)
        logging.info(f"Подготовлено {num_examples} примеров для обучения")
        os.makedirs('checkpoints', exist_ok=True)

        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=9, restore_best_weights=True),
            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10),
            tf.keras.callbacks.ModelCheckpoint(self.model_checkpoint_path, monitor='val_loss', save_best_only=True),
            tf.keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True)
        ]

        if validation_data is not None:
            val_texts, val_audio_paths = validation_data
            val_dataset = self.create_dataset(val_texts, val_audio_paths, batch_size, augment=False)
            return self.model.fit(dataset, epochs=epochs, validation_data=val_dataset, callbacks=callbacks)
        else:
            return self.model.fit(dataset, epochs=epochs, callbacks=callbacks)

    def generate_singing(self, text, output_path):
        sequence = self.prepare_text(text)
        sequence = tf.expand_dims(sequence, axis=0)
        mel_spec = self.model.predict(sequence)
        mel_spec = mel_spec.squeeze().astype(np.float32)
        mel_spec = np.exp(mel_spec)
        mel_spec = np.clip(mel_spec, 1e-5, np.max(mel_spec))
        S = librosa.feature.inverse.mel_to_stft(
            mel_spec,
            sr=self.SAMPLING_RATE,
            n_fft=1024,
            fmin=0.0,
            fmax=8000.0,
            power=1.0
        )

        desired_length = 10 * self.SAMPLING_RATE  # 10 секунд
        audio = librosa.griffinlim(np.abs(S), n_iter=2000, hop_length=256, win_length=1024)
        if len(audio) < desired_length:
            audio = np.pad(audio, (0, desired_length - len(audio)), mode='constant')
        else:
            audio = audio[:desired_length]

        audio = librosa.util.normalize(audio) * 0.95
        sf.write(output_path, audio, self.SAMPLING_RATE, 'PCM_24')
        logging.info(f"Aудио сохранено в {output_path}")

# Пример использования
if __name__ == "__main__":
    model = SingingModel()
    texts = txt.texts
    audio_paths = txt.audio_paths
    np.random.seed(42)
    indices = np.arange(len(audio_paths))
    np.random.shuffle(indices)
    val_size = 10
    validation_indices = indices[:val_size]
    training_indices = indices[val_size:]
    training_texts = [texts[i] for i in training_indices]
    training_audio_paths = [audio_paths[i] for i in training_indices]
    validation_texts = [texts[i] for i in validation_indices]
    validation_audio_paths = [audio_paths[i] for i in validation_indices]
    for x in range(40):
        model.train(training_texts, training_audio_paths, epochs=100, validation_data=(validation_texts, validation_audio_paths))
    model.load_weights()
    text = "Привет! Покааааааа " * 3
    model.generate_singing(text, "output_singing.wav")
