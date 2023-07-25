# audio2text
**使用步驟**

* 安裝必要的套件，請在terminal輸入指令
```
pip install -r requirement.txt
```
* 請將音檔與aduio2text.py cfg.json放入同一個位置
* 更改cfg.json檔案裡面的參數
* 在terminal 輸入指令
```
python3 audio2text.py -c cfg.json
```
* 執行完成時候，回在同樣的位置出現檔名一樣的txt，即是文字檔


**cfg.json：有兩個參數**
* audio_name：請更改成您的音檔名稱(需為wav檔案)
* overlap_time：因為本專案將每個音檔切成數個10秒的小音檔。每個小音檔會與前面小音檔重複您指定的秒數
