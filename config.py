# global variables
import pvporcupine
import torch

from datasets import load_dataset
from transformers import pipeline

# for wake wuction 
porcupine = pvporcupine.create(
  access_key= 'M+yKeh0VpkCQWNticKvu87148LC2kU6L9DNFEBsY1nkmH8ZocK9iLQ==',
  keyword_paths = ['wake_word/собака_ru_mac_v3_0_0.ppn'],
  model_path = "wake_word/porcupine_params_ru.pv"
)

# for connection with AI
synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

chater = pipeline(model='facebook/blenderbot-400M-distill')