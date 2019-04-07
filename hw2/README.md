### HW2 財報文字探勘練習

#### 資料來源及處理

 我們使用的是世界大型科技公司的10-K財報，分別取了Apple Inc 2013~2017的資料，以及Cisco, Facebook, Alphabet (Google), Microsoft這四家公司2017年的資料，以便進行垂直及水平的分析。原始的10-K財報之pdf檔在pdfs資料夾中，轉換過後的文字檔在txts資料夾中，轉換成按照詞頻的排序的word frequency list用pickle格式存在pickles資料夾中，本次作業中公司的對應名稱皆為其bloomberg ticker。資料處理方式是使用`preprocess.py`這個程式，只要在pdfs這個資料夾中有該公司的bloomberg ticker為名的資料夾，裡面的pdf檔按照指定的年份格式命名，就能使用`python preprocess.py BLOOMBERG_TICKER`的方式，產生txts及pickles資料夾中該公司的對應資料夾。



#### POS,NER及後續的作圖

後面的步驟都是用ipynb檔案呈現的，內有所有步驟的文字敘述。這次作業我們有兩個ipynb檔，一個是[Demo_pos_ner.ipynb](https://github.com/howard41436/FINTECH/blob/master/hw2/Demo_pos_ner.ipynb)，內容如作業二所要求做了POS和NER，最後的共現性分析也挑了兩組類別去做。另一個是[Demo_sentiment.ipynb](https://github.com/howard41436/FINTECH/blob/master/hw2/Demo_sentiment.ipynb)，由於跟教授個別討論後發現財報的文字內容不適合用一般的NER分析，因為其中出現的人地物，其實跟我們將來final要分析的財報品質無關，其共現性意義也不大。因此我們使用了教授提供的University of Notre Dame提供的LoughranMcDonald MasterDictionary，他是一個專門拿來分析財報的辭典，原因是他的辭典不是去分詞性或人地物，而是一個字表示出的情感類別，分成7類(Negative, Positive, Uncertainty, Litigious, Constraining, Superfluous, Interesting)，而這些正是我們重視的。因此我們用同樣的分析手法，只是從NER改成做情感詞的，最後也有做出共現圖和熱點圖，我們認為這份Demo做出來的結果是較有意義的。