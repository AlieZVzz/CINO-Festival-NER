#  面向藏族传统节日的汉藏双语命名实体识别研究 
#  A Study of Bilingual Chinese-Tibetan Named Entity Recognition for Traditional Tibetan Festivals
>  In this study, Chinese-Tibetan bilingual text data containing information on Tibetan traditional festivals from news websites such as People's Daily Online and People's Daily Tibetan Edition were collected and manually annotated. This study compares the performance of multiple pretrained models and word vectors for Tibetan traditional festival named entity recognition task in the Chinese-Tibetan bilingual scenario and analyzes the impact of two feature processing layers of the model, BiLSTM layer and CRF layer, on the experimental results.
## File Index
```
D:.
├───.idea
│   ├───dataSources
│   └───inspectionProfiles
├───checkpoints
│   └───01
├───CINO text classification
│   ├───data
│   ├───log
│   └───Tibetan News Classification Corpus
├───config
├───data_collect
│   ├───Chinese data
│   └───Tibetan data
│       └───crawler_data
├───log
│   ├───bo_fasttext_bilstm_crf
│   ├───bo_PLM_bilstm
│   ├───bo_PLM_crf
│   ├───cn_fasttext_bilstm_crf
│   ├───cn_PLM_bilstm
│   ├───cn_PLM_bilstm_crf
│   └───cn_PLM_crf
├───model
│   ├───CINO_base
│   ├───ernie
│   ├───fasttext_bo
│   ├───fasttext_cn
│   ├───roberta-base-bo
│   ├───roberta-chinese
│   └───__pycache__
├───output
├───static
│   ├───css
│   ├───font
│   ├───image
│   ├───js
│   └───picture
├───templates
├───utils
├───visualization
└───__pycache__

```
## Metrics
<table class="21" border="1" cellspacing="0" cellpadding="0" align="left" style="border-collapse:collapse;border:none;margin-left:6.75pt;margin-right:
 6.75pt">
 <tbody><tr style="height:2.85pt">
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><a name="_Hlk107927379"></a><a name="OLE_LINK82"><span style="font-size:7.5pt;
  font-family:宋体">语言</span></a></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><a name="_Hlk105266154"></a><a name="OLE_LINK42"><span style="font-size:7.5pt;
  font-family:宋体">模型</span></a></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">准确率</span></span><span style="font-size:7.5pt;
  font-family:宋体"></span></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">召回率</span><span style="font-size:7.5pt;
  font-family:宋体"></span></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;font-family:&quot;Times New Roman&quot;,serif">F1</span></p>
  </td>
 </tr>
 <tr style="height:2.85pt">
  <td rowspan="2" style="border:none;padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">汉语</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><a name="OLE_LINK41"><span style="font-size:7.5pt;font-family:宋体">汉语</span></a><span lang="EN-US" style="font-size:7.5pt">fastText</span><span style="font-size:7.5pt;
  font-family:宋体">词向量</span><span lang="EN-US" style="font-size:7.5pt">-BiLSTM-CRF</span><span style="font-size:7.5pt;font-family:宋体">模型</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">94.65%</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">89.64%</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">91.97%</span></p>
  </td>
 </tr>
 <tr style="height:2.85pt">
  <td valign="top" style="border:none;padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">汉语</span><span lang="EN-US" style="font-size:7.5pt">RoBERTa</span><span style="font-size:7.5pt;
  font-family:宋体">预训练模型</span><span lang="EN-US" style="font-size:7.5pt">-BiLSTM-CRF</span><span style="font-size:7.5pt;font-family:宋体">模型</span></p>
  </td>
  <td valign="top" style="border:none;padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">93.97%</span></p>
  </td>
  <td valign="top" style="border:none;padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">92.32%</span></p>
  </td>
  <td valign="top" style="border:none;padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">93.05%*</span></p>
  </td>
 </tr>
 <tr style="height:2.85pt">
  <td rowspan="2" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">藏语</span></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">藏语</span><span lang="EN-US" style="font-size:7.5pt">fastText</span><span style="font-size:7.5pt;
  font-family:宋体">词向量</span><span lang="EN-US" style="font-size:7.5pt">-BiLSTM-CRF</span><span style="font-size:7.5pt;font-family:宋体">模型</span></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">84.97%</span></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">76.68%</span></p>
  </td>
  <td valign="top" style="border-top:solid #7F7F7F 1.0pt;border-left:none;
  border-bottom:solid #7F7F7F 1.0pt;border-right:none;padding:0cm 5.4pt 0cm 5.4pt;
  height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">80.37%</span></p>
  </td>
 </tr>
 <tr style="height:2.85pt">
  
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span style="font-size:7.5pt;font-family:宋体">藏语</span><span lang="EN-US" style="font-size:7.5pt">RoBERTa</span><span style="font-size:7.5pt;
  font-family:宋体">预训练模型</span><span lang="EN-US" style="font-size:7.5pt">-BiLSTM-CRF</span><span style="font-size:7.5pt;font-family:宋体">模型</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">83.40%</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">89.60%</span></p>
  </td>
  <td valign="top" style="border:none;border-bottom:solid #7F7F7F 1.0pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:2.85pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;color:black">86.27%*</span></p>
  </td>
 </tr>
</tbody></table>

<br />

## Usage
在model文件夹中对应的预训练模型文件夹中放入pytorch模型，并在data_collect文件夹中放入对应语言的txt文件，修改main.py、utils.py、crf.py文件中的train_method。
运行main.py文件即可