from laserembeddings import Laser
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text as text  # Needed for loading universal-sentence-encoder-cmlm/multilingual-preprocess
import numpy as np
from sentence_transformers import SentenceTransformer
# importing os module  
import os 
import time

# Setup laser
laser = Laser()

# Setup LABSE
# labse_preprocessor = hub.KerasLayer(
#     "https://tfhub.dev/google/universal-sentence-encoder-cmlm/multilingual-preprocess/2")
# labse_encoder = hub.KerasLayer("https://tfhub.dev/google/LaBSE/2")

# # Setup XLM-R
# xlmr_embedder = SentenceTransformer('paraphrase-xlm-r-multilingual-v1') #XLMR 

startTime=time.time()

def normalization(embeds):
  norms = np.linalg.norm(embeds, 2, axis=1, keepdims=True)
  return embeds/norms

# Method for creating embeddings from each encoder
def create_embeddings(encoder,sentences,lang):
  #if encoder == "laser":
  #  return laser.embed_sentences(sentences,lang=lang);
  if encoder == "labse":
     processed_sentences = tf.constant(sentences)
  #   return labse_encoder(labse_preprocessor(processed_sentences))['default']
  # if encoder == "xlmr":
  #   return xlmr_embedder.encode(sentences)

# Read files and return as an array
def read_file(filepath):
  contents = []
  with open(filepath, encoding="utf-8") as f:
    contents = f.read().splitlines()
  return [line.strip().split('\t')[-1].strip() for line in contents]

# Write data to file
def write_file(data,file_path):
  np.array(data).tofile(file_path)


#create laser embeddings
root = "/home/aloka/Files/p2_document_similarity_measurement/comparable-corpus/Comparable_Sentences_with_Golden_Alignment/si-en/army/" 
encoders = ['labse'] # use : 'laser','labse','xlmr'
langs=['english', 'sinhala', 'tamil']

summary_statistics=[]

#build embeddings
for encoder in encoders:    

  txt_path=root+'sentences'
  emb_path=root+'embeddings_'+encoder



  for lang in langs:

      #statistics for summary
      sents_counts=0

      files=os.listdir(txt_path+'/'+lang)

      for file in files:
          sentences = read_file(txt_path+'/'+lang+'/'+file)
          #print(sentences)
          lang_encoder=''
          if lang=='english':
              lang_encoder='en'
          elif lang=='sinhala':
              lang_encoder='si'
          elif lang=='tamil':
              lang_encoder='ta'

          embeddings = create_embeddings(encoder,sentences,lang_encoder)
          embedding_path = emb_path+'/'+lang
          #print(len(embeddings[0]))
          sents_counts+=len(sentences)

          try:
            os.makedirs(embedding_path)
          except FileExistsError:
            print("Directory %s already exists." % embedding_path)

          write_file(embeddings,embedding_path+'/'+file+'.emb')

endTime=time.time()
print('Time taken to generate {} embeddings : {}min {}sec'.format(encoder, int((endTime-startTime)//60), int((endTime-startTime)%60)))