from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import requests



Window.size = (350,600)

kv='''
MDFloatLayout:
    md_bg_color:1,1,1,1
    Image:
        source:"assets/location.png"
        size_hint:.09,.09
        pos_hint:{"center_x":.5,"center_y":.95}
    MDLabel:
        id:location
        text:""
        pos_hint:{"center_x":.5,"center_y":.89}
        halign:"center"
        font_size:"20sp"
        
    Image:
        id:weather_image
        source:""
        size_hint:.4,.4
        pos_hint:{"center_x":.5,"center_y":.77}

    MDLabel:
        id:temperature
        text:""
        markup:True
        pos_hint:{"center_x":.5,"center_y":.62}
        halign:"center"
        font_size:"50sp"
    MDLabel:
        id:weather
        text:""
        pos_hint:{"center_x":.5,"center_y":.54}
        halign:"center"
        font_size:"20sp"

    MDFloatLayout:
        pos_hint:{"center_x":.25,"center_y":.4}
        size_hint:.22,.1
        Image:
            source:"assets/Humidity.png"
            pos_hint:{"center_x":.1,"center_y":.5}
        MDLabel:
            id: humidity
            text:""
            pos_hint:{"center_x":1,"center_y":.7}
            font_size:"14sp"
        MDLabel:
            text:"Humidity"
            pos_hint:{"center_x":1,"center_y":.3}
            font_size:"14sp"
    MDFloatLayout:
        pos_hint:{"center_x":.7,"center_y":.4}
        size_hint:.22,.1
        Image:
            source:"assets/Wind.png"
            pos_hint:{"center_x":.1,"center_y":.5}
        MDLabel:
            id: wind_speed
            text:""
            pos_hint:{"center_x":1.1,"center_y":.7}
            font_size:"16sp"
        MDLabel:
            text:"Wind"
            pos_hint:{"center_x":1.1,"center_y":.3}
            font_size:"14sp"

    MDFloatLayout:
        size_hint_y:.3
        canvas:
            Color:
                rgb: rgba(148,117,255,255)
            RoundedRectangle:
                size:self.size
                pos:self.pos
                radius:[10,10,0,0]

        MDFloatLayout:
            pos_hint:{"center_x":.5,"center_y":.71}
            size_hint:.9,.32
            canvas:
                Color:
                    rgb: rgba(131,69,255,255)
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[7]
            
            TextInput:
                id:city_name
                hint_text:"Enter City Name"
                size_hint:1,None
                pos_hint:{"center_x":.5,"center_y":.5}
                height:self.minimum_height
                multiline:False
                font_size:"20sp"
                hint_text_color:1,1,1,1
                foreground_color:1,1,1,1
                background_color:1,1,1,0
                padding:15
                cursor_color:1,1,1,1
                cursor_width:"2sp"
        Button:
            text:"Enter"
            font_size:"20sp"
            size_hint:.9,.32
            pos_hint:{"center_x":.5,"center_y":.29}
            background_color:1,1,1,0
            color:rgba(148,117,255,255)
            on_release:app.search_weather()
            canvas.before:
                Color:
                    rgb: 1,1,1,1
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[7]
            
'''


class WeatherApp(MDApp):
    api_key ="67599bdbbb1a02f44f084a61c3d57807"

    def on_start(self):
        try:
            BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+at+my+current+location").text,"html.parser")
            temp = soup.find("span",class_="BNeawe tAd8D AP7Wnd")
            location = "".join(filter(lambda item: not item.isdigit(),temp.text)).split(",",1)
            self.get_weather(location[0])

        except requests.ConnectionError:
            print("No Internet Connection!")
            exit()




    def build(self):
        Images = Builder.load_string(kv)
        return Images
    
    def get_weather(self,city_name):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"
            response = requests.get(url)
            x = response.json()
            print(x)
            if x["cod"]!="404":
                temperature = round(x["main"]["temp"]-273.15)
                humidity = x["main"]["humidity"]
                weather = x["weather"][0]["main"]
                id = str(x["weather"][0]["id"])
                wind_speed = round(x["wind"]["speed"]*18/5)
                location = x["name"] + ", " + x["sys"]["country"]
                self.root.ids.temperature.text = f"[b]{temperature}[/b]°"
                self.root.ids.weather.text = str(weather)
                self.root.ids.humidity.text = f"{humidity}%"
                self.root.ids.wind_speed.text = f"{wind_speed} km/h"
                self.root.ids.location.text = location
                self.root.ids.temperature.text = str(temperature)

                if id =="800":
                    self.root.ids.weather_image.source = "assets\sun.png"
                elif "801"<= id <="800":
                    self.root.ids.weather_image.source = "assets\clouds.png"
                elif "701"<= id <="781":
                    self.root.ids.weather_image.source = "assets\haze.png"
                elif "600"<= id =="622":
                    self.root.ids.weather_image.source = "assets\snow.png"
                elif "500"<= id <="531":
                    self.root.ids.weather_image.source = "assets\rain.png"
                elif "300"<= id <="321":
                    self.root.ids.weather_image.source = "assets\drizzle.png"
                elif "200"<= id <="232":
                    self.root.ids.weather_image.source = "assets\thunderstorm.png"

            else:
                print("City Not Found!")
        except requests.ConnectionError:
            print("No Internet Connection!")
    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != "":
         self.get_weather(city_name)

if __name__== "__main__":
    WeatherApp().run()



    #https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}