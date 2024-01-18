import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Load pre-trained model and tokenizer
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Load audio file
waveform, sample_rate = torchaudio.load("C:\\Users\\itayy\\Desktop\\wrods\\thing.wav")

# Tokenize audio
input_values = tokenizer(waveform.squeeze().numpy(), return_tensors="pt", padding="longest").input_values

# Forward pass
logits = model(input_values).logits

# Decode logits to get predicted phonemes
predicted_ids = logits.argmax(dim=-1)
predicted_phonemes = tokenizer.batch_decode(predicted_ids)

print(predicted_phonemes)
