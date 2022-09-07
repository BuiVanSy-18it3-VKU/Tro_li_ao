import os
import playsound
import speech_recognition as sr
import time
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import requests
import urllib.request as urllib2
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch

language = 'vi'
path = ChromeDriverManager().install()
wikipedia.set_lang('vi')

#speech to text
def speak(text):
    print("Zing: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("doc.mp3")
    playsound.playsound("doc.mp3", False)
    os.remove("doc.mp3")

def get_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bạn: ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except :
            print("...")
            return 0

def stop():
    speak("Tạm biệt")

def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Xin lỗi, bạn có thể nói lại không?")
            time.sleep(2)
    time.sleep(2)
    stop()
    return 0

def talk(name):
    day_time = int(strftime('%H'))
    if 5 <= day_time <= 10:
        speak("Chào buổi sáng. Chúc bạn một ngày tốt lành!")
    elif 0 <= day_time < 5:
        speak("Đang nửa đêm đó bạn ơi???")
    elif 10 < day_time <= 13:
        speak("chào bạn mình là Zing. Buổi trưa ngon miệng.")
    elif 13 < day_time <= 18:
        speak("chào bạn mình là Zing. Buổi chiều vui vẻ !")
    else:
        speak("Chúc bạn buổi tối vui vẻ!")
    time.sleep(3)
    speak("Bạn thế nào?")
    time.sleep(3)
    ans = get_voice()
    if "ổn" in ans or "khỏe" in ans:
        speak("Thật là tốt!. Bạn khỏe tôi cũng khỏe")
    else:
        speak("Tôi không hiểu! xin lỗi bạn")

def help():
    speak("""Tôi có thể làm những việc sau:
    1. Chào hỏi
    2. Hiển thị ngày giờ
    3. Mở website, ứng dụng trong máy.
    4. Tìm kiếm trên Google
    5. Dự báo thời tiết
    6. Tìm video youtube
    7. Thay đổi hình nền máy tính
    8. Tìm định nghĩa """)
    time.sleep(25)

def open_website(text):
    regex = re.search('mở (.+)', text)
    if regex:
        domain = regex.group(1)
        url = 'https://www.' + domain
        webbrowser.open(url)
        speak("Trang web của bạn đã được mở lên!")
        return True
    else:
        return False

def google_search(text):
    search_for = str(text).split("kiếm", 1)[1]
    speak("bắt đầu tìm kiếm... ")
    time.sleep(1)
    url = f'https://google.com/search?q={search_for}'
    webbrowser.get().open(url)
    speak("Đây là kết quả bạn muốn")

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak("Zing không hiểu rồi ")
    time.sleep(5)

def play_youtube():
    speak("Mở video về gì?")
    time.sleep(2)
    my_song = get_text()
    while True:
        result = YoutubeSearch(my_song, max_results=10).to_dict()
        if result:
            break
    url = f'https://www.youtube.com' + result[0]['url_suffix']
    print("Link youtube: \t," , url)
    webbrowser.get().open(url)
    speak("Mở kết quả đầu tiên")
    time.sleep(2)

def weather():
    speak("Bạn muốn xem thời tiết thành phố nào!")
    time.sleep(3)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time = data["sys"]
        sun_rise = datetime.datetime.fromtimestamp(sun_time["sunrise"])
        sun_set = datetime.datetime.fromtimestamp(sun_time["sunset"])
        wther = data["weather"]
        weather_des = wther[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}% """\
            .format(day=now.day, month=now.month, year=now.year,
                    hourrise=sun_rise.hour,
                    minrise=sun_rise.minute,
                    hourset=sun_set.hour, minset=sun_set.minute,
                    temp=current_temp, pressure=current_pressure,
                    humidity=current_humidity)
        speak(content)
        time.sleep(25)
    else:
        speak("Không tìm thấy thành phố!")
        time.sleep(2)

def open_app(text):
    if "google" in text:
        speak("Mở google chrome")
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
        time.sleep(3)
    elif "word" in text:
        speak("Mở Microsoft Word")
        os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word2016.lnk")
        time.sleep(5)
    else:
        speak("Phần mềm của bạn chưa được cài đặt!")
        time.sleep(2)

def chang_wallpaper():
    api_key = 'zQbgEMZLggEZ0C5ixGorFf0drlbU_WUdkl-sThwH3t4'
    url = 'https://api.unsplash.com/photos/random?client_id=' + api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']

    urllib2.urlretrieve(photo, r"C:\Users\Bui Van Sy\Downloads\11.png")
    image = os.path.join(r"C:\Users\thanh\Downloads\11.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
    speak("Hình nền máy tính vừa được thay đổi")
    time.sleep(2)

def tell_me():
    try:
        speak("Bạn muốn nghe về gì ạ!")
        time.sleep(2)
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(20)
    except:
        speak("Zing nghe không hiểu")
        time.sleep(3)

def call_ai():
    speak("Xin chào. Mình là Zing. Một Virtual Assistant. Bạn tên là ?")
    time.sleep(6)
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        time.sleep(1.5)
        speak("Bạn cần Zing giúp gì ạ!")
        time.sleep(2)
        while True:
            text = get_text()
            if not text:
                break
            elif "trò chuyện" in text or "nói chuyện" in text:
                talk(name)
            elif "kết thúc" in text or "tạm biệt" in text:
                speak("Goodbye! Hẹn gặp lại")
                time.sleep(3)
                stop()
                break
            elif "mở" in text:
                if "." in text:
                    open_website(text)
                else:
                    open_app(text)
            elif "ngày" in text or "giờ" in text:
                get_time(text)
            elif "tìm kiếm" in text:
                google_search(text)
            elif "video" in text:
                play_youtube()
            elif "thời tiết" in text:
                weather()
            elif "hình nền" in text:
                chang_wallpaper()
            elif "định nghĩa" in text:
                tell_me()
            elif "có thể làm gì" in text:
                help()

call_ai()