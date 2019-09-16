# A small Deep Learning tutorial with Github and Keras

## Prepare data

We'll work on a simple Deep Learning Dog vs. Cat classifiser. 

Create a `data/` folder. The dogs-vs-cats dataset can be downloaded [here](https://www.kaggle.com/c/3362/download-all) (you have to log in to your Kaggle account to be able to download it)

Extract the file to `data/` folder.

Rename the new extracted folder to `dogcat/`

```bash
mv dogs-vs-cats dogcat
cd dogcat/
```

Unzip train dataset

```bash
unzip train.zip
```

Re-organize the dataset into the following structure:

```bash
dogcat/
|---train/
    |---dog/
    |---cat/
|---val/
    |---dog/
    |---cat/
```

with command:

```bash
python utils.py
```
