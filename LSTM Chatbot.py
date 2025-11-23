"""
LSTM Test Chatbot
=====
  This is a simple LSTM-based chatbot that generates text based on user input. It uses TensorFlow and Keras to build and train the model.
"""

import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.models import Sequential
import numpy as np
import time
import re # For word tokenization

def generate_words(model, start_words_list, num_generate, seq_len, word_to_int, int_to_word, temperature=1.0):
  # Convert start_words_list to integer representation
  input_eval = [word_to_int.get(word.lower(), word_to_int[vocab[0]]) for word in start_words_list]
  # Use word_to_int[vocab[0]] as a fallback for OOV words.
  # A more robust solution would be a dedicated <unk> token.
  
  # Pad or truncate the input sequence to `seq_len`
  if len(input_eval) < seq_len:
    padding_word_int = word_to_int[vocab[0]] # Use the first word in vocab as padding
    input_eval = [padding_word_int] * (seq_len - len(input_eval)) + input_eval
  elif len(input_eval) > seq_len:
    input_eval = input_eval[-seq_len:] # Take the last `seq_len` words

  # Add batch dimension (1 for single sequence prediction)
  input_eval = np.array(input_eval).reshape(1, seq_len)

  generated_words_list = []

  for _ in range(num_generate):
    # Predict logits for the next word
    predictions = model.predict(input_eval, verbose=0)[0] # Get predictions (logits) for the current batch item

    # Apply temperature for sampling (to logits)
    predictions = predictions / temperature
    
    # Sample the next word ID based on logits using tf.random.categorical
    predicted_id = tf.random.categorical(tf.expand_dims(predictions, 0), num_samples=1)[-1,0].numpy()
    
    # Append the predicted word to the generated list
    generated_words_list.append(int_to_word[predicted_id])

    # Update the input sequence for the next prediction
    # Take the last 'seq_len - 1' words and append the new predicted word ID
    input_eval = np.append(input_eval[:, 1:], [[predicted_id]], axis=1)
      
  return start_words_list + generated_words_list

def display(string : str) -> None: # displays a string in a fancy way
  print("", end='')
  count = 0
  for i in string.split():
    count += 1
    time.sleep(0.09) # Simulate typing delay
    
    print(i, end=' ', flush=True)
    
    if count > 15:
      count = 0
      print()
      print("", end='')
  print()

text_content = ("""

Instruction Models
A model trained for text generation can be later adapted to follow instructions. You can try some of the most powerful instruction-tuned open-access models like Mixtral 8x7B, Cohere Command R+, and Meta Llama3 70B at Hugging Chat.

Code Generation
A Text Generation model, also known as a causal language model, can be trained on code from scratch to help the programmers in their repetitive coding tasks. One of the most popular open-source models for code generation is StarCoder, which can generate code in 80+ languages. You can try it here.

Stories Generation
A story generation model can receive an input like "Once upon a time" and proceed to create a story-like text based on those first words. You can try this application which contains a model trained on story generation, by MosaicML.

If your generative model training data is different than your use case, you can train a causal language model from scratch. Learn how to do it in the free transformers course!

Task Variants
Completion Generation Models
A popular variant of Text Generation models predicts the next word given a bunch of words. Word by word a longer text is formed that results in for example:

Given an incomplete sentence, complete it.
Continue a story given the first sentences.
Provided a code description, generate the code.
The most popular models for this task are GPT-based models, Mistral or Llama series. These models are trained on data that has no labels, so you just need plain text to train your own model. You can train text generation models to generate a wide variety of documents, from code to stories.

Text-to-Text Generation Models
These models are trained to learn the mapping between a pair of texts (e.g. translation from one language to another). The most popular variants of these models are NLLB, FLAN-T5, and BART. Text-to-Text models are trained with multi-tasking capabilities, they can accomplish a wide range of tasks, including summarization, translation, and text classification.

Language Model Variants
When it comes to text generation, the underlying language model can come in several types:

Base models: refers to plain language models like Mistral 7B and Meta Llama-3-70b. These models are good for fine-tuning and few-shot prompting.

Instruction-trained models: these models are trained in a multi-task manner to follow a broad range of instructions like "Write me a recipe for chocolate cake". Models like Qwen 2 7B, Yi 1.5 34B Chat, and Meta Llama 70B Instruct are examples of instruction-trained models. In general, instruction-trained models will produce better responses to instructions than base models.

Human feedback models: these models extend base and instruction-trained models by incorporating human feedback that rates the quality of the generated text according to criteria like helpfulness, honesty, and harmlessness. The human feedback is then combined with an optimization technique like reinforcement learning to align the original model to be closer with human preferences. The overall methodology is often called Reinforcement Learning from Human Feedback, or RLHF for short. Zephyr ORPO 141B A35B is an open-source model aligned through human feedback.

Text Generation from Image and Text
There are language models that can input both text and image and output text, called vision language models. IDEFICS 2 and MiniCPM Llama3 V are good examples. They accept the same generation parameters as other language models. However, since they also take images as input, you have to use them with the image-to-text pipeline. You can find more information about this in the image-to-text task page.


""")

MAX_TEXT_LENGTH = 10000 
text_content = text_content[:MAX_TEXT_LENGTH]

text_content = text_content.lower()

# Regex to split words and keep common punctuation as separate tokens
# \b\w+\b matches words (alphanumeric + underscore)|[.,!?;]
words = re.findall(r"\b[\w']+\b", text_content)

# Create Vocabulary and Mappings

vocab = sorted(list(set(words)))
word_to_int = {word: i for i, word in enumerate(vocab)}
int_to_word = {i: word for i, word in enumerate(vocab)}
vocab_size = len(vocab)

# Convert Text to Integer Sequences

text_as_int = [word_to_int[word] for word in words]

# Create Training Data (Sequences of Word IDs for Input and Target)

seq_len = 15 # Length of input sequence (number of words)
X = [] # Input sequences of word IDs
y = [] # Target word ID

for i in range(len(text_as_int) - seq_len):
  X.append(text_as_int[i:i+seq_len])
  y.append(text_as_int[i+seq_len])

# Convert to numpy arrays for TensorFlow
X = np.array(X)
y = np.array(y)

print(f"Number of training sequences: {len(X)}")
print(f"Shape of X: {X.shape}") # (num_sequences, seq_len)
print(f"Shape of y: {y.shape}") # (num_sequences,)

# Define the LSTM Model 

embedding_dim = 64 # Dimension of the word embeddings
lstm_units = 128    # Number of units in the LSTM layers

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=seq_len))

model.add( Bidirectional(LSTM(lstm_units, return_sequences=True)) )
model.add(Dense(vocab_size)) 

model.add( Bidirectional(LSTM(lstm_units, return_sequences=True)) )
model.add(Dense(vocab_size)) 

model.add(LSTM(lstm_units))
model.add(Dense(vocab_size)) 

model.compile(
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
  optimizer='adam', 
  metrics=['accuracy']
)

# Train the Model

history = model.fit(
  X,
  y,
  epochs=75 ,
  batch_size=16
)

# test

print("\n===== Testing Mode =====")

start_seed_words = "hello there".split()

generated_text = generate_words(
  model,
  start_words_list=start_seed_words,
  num_generate=30, # Number of words to generate
  seq_len=seq_len,
  word_to_int=word_to_int,
  int_to_word=int_to_word,
  temperature=0.9 # Adjust temperature for creativity (e.g., 0.5 to 1.0)
)

display(f"[User]: {' '.join(start_seed_words)}")
print()
display(f"┃ [Model]: { ' '.join(generated_text[len(start_seed_words):]) }")