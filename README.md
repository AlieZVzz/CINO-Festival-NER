#  A Study of Bilingual Chinese-Tibetan Named Entity Recognition for Traditional Tibetan Festivals（面向藏族传统节日的汉藏双语命名实体识别研究)
## Overview
This repository contains the official implementation of "A Study of Bilingual Chinese-Tibetan Named Entity Recognition for Traditional Tibetan Festivals" paper. Additionaly, detailed implement guides are provided.

In this study, Chinese-Tibetan bilingual text data containing information on Tibetan traditional festivals from news websites such as People's Daily Online and People's Daily Tibetan Edition were collected and manually annotated. This study compares the performance of multiple pretrained models and word vectors for Tibetan traditional festival named entity recognition task in the Chinese-Tibetan bilingual scenario and analyzes the impact of two feature processing layers of the model, BiLSTM layer and CRF layer, on the experimental results.
## Environment
- Python 3.8
- Pytorch 1.10
- beautifulsoup4 4.11.1
- Flask 2.0.2
- html2text 2020.1.16
- joeynmt 1.5.1
- transformers 4.18.0

To install the environment using Conda:
```bash
$ conda env create -f requirements.txt
```
## Running
### Train
To train the models in this study, run the command below. Detailed configs are in the config folder.
```bash
$ python main.py 
```
### Deployment
To deploy trained model to server, run the command below.
```bash
$ python app.py
```

## Metrics
<table>
<tbody>
  <tr>
    <td>
      <p>语言</p>
    </td>
    <td>
      <p>模型</p>
    </td>
    <td>
      <p>准确率</p>
    </td>
    <td>
      <p>召回率</p>
    </td>
    <td>
      <p></p>
    </td>
  </tr>
  <tr>
    <td rowspan="2">
      <p>汉语</p>
    </td>
    <td>
      <p>汉语fastText词向量-BiLSTM-CRF模型</p>
    </td>
    <td>
      <p>94.65%</p>
    </td>
    <td>
      <p>89.64%</p>
    </td>
    <td>
      <p>91.97%</p>
    </td>
  </tr>
  <tr>
    <td>
      <p>汉语RoBERTa预训练模型-BiLSTM-CRF模型</p>
    </td>
    <td>
      <p>93.97%</p>
    </td>
    <td>
      <p>92.32%</p>
    </td>
    <td>
      <p>93.05%*</p>
    </td>
  </tr>
  <tr>
    <td rowspan="2">
      <p>藏语</p>
    </td>
    <td>
      <p>藏语fastText词向量-BiLSTM-CRF模型</p>
    </td>
    <td>
      <p>84.97%</p>
    </td>
    <td>
      <p>76.68%</p>
    </td>
    <td>
      <p>80.37%</p>
    </td>
  </tr>
  <tr>
    <td>
      <p>藏语RoBERTa预训练模型-BiLSTM-CRF模型</p>
    </td>
    <td>
      <p>83.40%</p>
    </td>
    <td>
      <p>89.60%</p>
    </td>
    <td>
      <p>86.27%*</p>
    </td>
  </tr>
</tbody></table>


## Citation
If you make use of this code, please cite the following paper:
```bibtex

@article{__nodate,
	title = {面向藏族传统节日的汉藏双语命名实体识别研究},
	issn = {2096-3467},
	url = {https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CAPJ&dbname=CAPJLAST&filename=XDTQ20220919000&uniplatform=NZKPT&v=E0vy1-y12agMc69tk-2GtR8p4fYnElMzKx2NKvq_UAb22I3wPYyc87DvVxQNCyxI},
	language = {中文},
	urldate = {2022-09-29},
	journal = {数据分析与知识发现},
	author = {邓, 宇扬 and 吴, 丹},
	keywords = {Named Entity Recognition, Pretrained Language Model, Tibetan Traditional Culture, 命名实体识别, 藏族传统文化, 预训练语言模型},
	pages = {1--15},
}

```
