## Sentence Alignment

The code for sentence alignment task is shared here.

Download the data from huggingface datasets [NLPC-UOM/sentence_alignment_dataset-Sinhala-Tamil-English](https://huggingface.co/datasets/NLPC-UOM/sentence_alignment_dataset-Sinhala-Tamil-English)

Use [sa_generate_embeddings.py](https://github.com/aloka-fernando/da_and_sa_parallel_corpus_mining/blob/master/sentence_alignment/sa_generate_embeddings.py) to create embeddings for each documnet.Then the embedding files should be created under the folder structure 

```python
/src_lang-tgt_lang/news_source/embedding_type/lang 
```

eg:
```python
si-en/army/embeddings_laser/english/

100624.emb  142644.emb  198722.emb  256966.emb......
```

Use the following command from the project home with appropriate arguments to run the sentence alignment task

python3 main.py -l si-en -w army -s cosine -r True -d True -e laser

Argument | Description
--------- | ----------
-l | language pair
-w | website 
-s | similarity measurement
-r | True to use ratio score.
-d | True to use dictionary weighting.
-e | embedding 

## Citation

```python
@article{fernando2022exploiting,
  title={Exploiting bilingual lexicons to improve multilingual embedding-based document and sentence alignment for low-resource languages},
  author={Fernando, Aloka and Ranathunga, Surangika and Sachintha, Dilan and Piyarathna, Lakmali and Rajitha, Charith},
  journal={Knowledge and Information Systems},
  pages={1--42},
  year={2022},
  publisher={Springer}
}
```
