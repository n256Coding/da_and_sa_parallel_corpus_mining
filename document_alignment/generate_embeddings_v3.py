from laserembeddings import Laser
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text as text  # Needed for loading universal-sentence-encoder-cmlm/multilingual-preprocess
import numpy as np
from sentence_transformers import SentenceTransformer
import os 
import time
import traceback

startTime=time.time()

model_path = '/content/drive/MyDrive/Research Project/saved_models/output/make-multilingual--2022-10-29_10-49-58/'

def normalization(embeds):
  norms = np.linalg.norm(embeds, 2, axis=1, keepdims=True)
  return embeds/norms


def load_model(model_path):
    return SentenceTransformer(model_path)

distilled_encoder = load_model(model_path=model_path)

# Method for creating embeddings from each encoder
def create_embeddings(sentences):
   return distilled_encoder.encode(sentences)

# Read files and return as an array
def read_file(filepath):
  contents = []
  with open(filepath, encoding="utf-8") as f:
    contents = f.read().splitlines()
  return contents

# Write data to file
def write_file(data,file_path):
  np.array(data).tofile(file_path)


site_list = ['army', 'hiru', "newsfirst", 'itn'] 

#summary stats
summary_stats=[]
dummy_count=0
root = '/content/data'
encoder = 'distiled-encoder'


for site in site_list:
    embedding_dir_path = root+'/'+'embeddings'+'_'+encoder
    sitepath = root+'/'+'textfiles'+'/'+site

    lang_list = os.listdir(sitepath)
    for lang in lang_list:

        #summary stats
        sents_count=0
        file_count=0

        print("Start embedding creation for %s %s documents" % (site,lang))
        langpath = sitepath+'/'+lang
        years = os.listdir(langpath)
        for year in years:
            yearpath = langpath+'/'+year
            months = os.listdir(yearpath)
            for month in months:
                monthpath = yearpath+'/'+month
                days = os.listdir(monthpath)
                for day in days:
                    daypath = monthpath+'/'+day
                    files = os.listdir(daypath)
                    for file in files:
                        try:
                            sentences = read_file(daypath+'/'+file)
                            embeddings = create_embeddings(sentences)
                            embedding_path = embedding_dir_path+'/'+site+'/'+lang+'/'+year+'/'+month+'/'+day
                            #print(len(embeddings[0]))

                            sents_count+=len(sentences)
                            file_count+=1

                            try:
                                os.makedirs(embedding_path)
                            except FileExistsError:
                                #print("Directory %s already exists." % embedding_path)
                                dummy_count+=0

                            write_file(embeddings,embedding_path+'/'+file.replace('.txt','.raw'))
                        except:
                            traceback.print_exc()
                            print('ERROR : {}/{}/{}/{}/{}/{}'.format(sitepath, lang, year, month, day, file))
                            break

                print('{}-{}-{}-{} completed'.format(encoder, lang, year, month))


    summary_stats.append('{}-{} [files/sents]: {}/{}'.format(site, lang, file_count, sents_count))

endTime=time.time()
print('Time taken to generate {} embeddings : {}min {}sec'.format(encoder, int((endTime-startTime)//60), int((endTime-startTime)%60)))

#print final statistics
for item in summary_stats:
  print(item)