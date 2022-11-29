## Document Alignment
This is the code for document alignmnet.

Download the data from huggingface datasets [NLPC-UOM/document_alignment_dataset-Sinhala-Tamil-English](https://huggingface.co/datasets/NLPC-UOM/document_alignment_dataset-Sinhala-Tamil-English)

Use [da_generate_embeddings_v2.py](https://github.com/aloka-fernando/da_and_sa_parallel_corpus_mining/blob/master/document_alignment/da_generate_embeddings_v2.py) to create embeddings for each documnet.Then the embedding files should be created under the folder structure /news_source/lang/year/month/day/ 
eg: 
```python
/news/en/2021/Apr/02/ 
686073.raw  706508.raw
```

Afterwards you can run the document alignment task.

```python
#embedding filepaths
newsSource="hiru"
embeddingPathA="./p2_parallel_corpus_mining/embeddings_laser/hiru/en/"
embeddingPathB="./p2_parallel_corpus_mining/embeddings_laser/hiru/si/"

#textfiles in respective languages
readbleDataPathA="/userdirs/aloka/p2_parallel_corpus_mining/textfiles/hiru/en/" 
readbleDataPathB="/userdirs/aloka/p2_parallel_corpus_mining/textfiles/hiru/si/"

#en-si
#goldenAlignmentPath="comparable-corpus/comparable_documnets_with_golden_alignment_v2/hiru/hiru_english_sinhala.txt"


mlModelPath="//model2_itm2.sav"
option="laser" #laser, xlmr
dimension=1024 #laser-1024 | xmlr,labse-768
metric="euclidean" #metric, cosine, euclidean

echo "Document Alignment for $newsSource"

python3 cerebrex_code_A/main.py \
	$embeddingPathA \
	$embeddingPathB \
	$readbleDataPathA \
	$readbleDataPathB \
	$goldenAlignmentPath \
	$mlModelPath \
	$option \
	$dimension \
	$metric
```

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
