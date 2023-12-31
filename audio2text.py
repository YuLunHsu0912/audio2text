import os
import shutil
import speech_recognition as sr
import concurrent.futures
import wave
import json
import numpy as np
from inlp.convert import chinese
from pydub import AudioSegment
import numpy as np


def texts_to_one(path, target_file):
    files = os.listdir(path)
    files.sort()
    files = [path+"/" + f for f in files if f.endswith(".txt")]
    with open(target_file, "w", encoding="utf-8") as f:
        for file in files:
            with open(file, "r", encoding='utf-8') as f2:
                txt= f2.read().split("\n")
                if len(txt) < 2:
                    continue
                f.write(txt[1])
    print("完成合併, 檔案位於 %s " % target_file)
def VoiceToText_thread(file):
  txt_file = "%s/%s.txt" % (txt_path, file[:-4])   
  if os.path.isfile(txt_file):
    return
  with open("%s/%s.txt" % (txt_path, file[:-4]), "w", encoding="utf-8") as f:
    f.write("%s:\n" % file)
    r = sr.Recognizer()  # 預設辨識英文
    with sr.WavFile(wav_path+"/"+file) as source:  # 讀取wav檔
      audio = r.record(source)
      # r.adjust_for_ambient_noise(source)
      # audio = r.listen(source)
    try:
      text = r.recognize_google(audio,language = voiceLanguage)
      text = chinese.s2t(text)
      # r.recognize_google(audio)
      
      if len(text) == 0:
        print("===無資料==")
        return

      print(f"{file}\t{text}")
      f.write("%s \n\n" % text)
      if file == files[-1]:
          print("結束翻譯")
    except sr.RequestError as e:
      print("無法翻譯{0}".format(e))
      # 兩個 except 是當語音辨識不出來的時候 防呆用的
      # 使用Google的服務
    except LookupError:
      print("Could not understand audio")
    except sr.UnknownValueError:
      print(f"Error: 無法識別 Audio\t {file}")
try:
    assert args.cfg is not None, "no cfg input file, try default inner parameter."
    with open(args.cfg, 'r') as ff:
        cfg = json.load(ff)

except Exception as e:
    print(e)
    
if __name__ == "__main__":
    file_list = os.listdir('file')
    overlap_time = "0000"
    for file_name in file_list:
        print(file_name)
        os.mkdir('wav')
        os.mkdir('txt')
        audio = AudioSegment.from_file("file/"+file_name, "wav")
        audio_time = len(audio)
        cut_parameters = np.arange(10,audio_time/1000,10)  
        start_time = int(0)
        for t in cut_parameters:
            stop_time = int(t * 1000)  
            audio_chunk = audio[start_time:stop_time] 
            audio_chunk.export("wav/temp-{:03d}.wav".format(int(t/10)), format="wav")  
            start_time = stop_time - int(overlap_time)  
   
        voiceLanguage="zh-TW" 
        wav_path='wav'
        txt_path='txt'
        thread_num=10
        files = os.listdir(wav_path)
        files.sort()
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
            executor.map(VoiceToText_thread, files)
        target_txtfile = "{}.txt".format(file_name[:-4])
        texts_to_one(txt_path, target_txtfile)
        shutil.rmtree(wav_path)
        shutil.rmtree(txt_path)
        
