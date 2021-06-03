#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font  as tkfont

from tkinter import scrolledtext
from tkinter import messagebox
import tkinter.font
import tkinter.messagebox as msgbox
from tkinter.filedialog import *
from PIL import Image, ImageTk

import time

import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
#api
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'my first API-2020dd811d20.json'

foodlist = ["Steak", "Pasta", "Pizza", "Salad", "Crispy fried chicken",
            'Fried food',"Fried chicken",'Cake', 'Rice','Sandwich','Fried fish',
            "Rotini", 'Pancake', 'Sushi', 'Hot dog', 'Potato wedges','Burrito',
            'Taco', 'Tortilla', 'Jjigae', 'Stew', 'Bread', 'Rice and curry','Tofu','Namul',
            'Chinese noodles', 'Tonkatsu', 'Corn flakes', 'Yellow curry', 'Mandu', 'Frosted flakes']

totalCal = 0
calories = 0
filename = ''

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("400x700")
        self.title("ForOne")
        self.resizable(False, False)
        self.configure(background='#FFFACD')
        # self['bg'] = '#FFFACD'
        self.title_font = tkfont.Font(size=20, weight='bold')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["UserInfo"] = UserInfo(parent=container, controller=self)
        self.frames["Home"] = Home(parent=container, controller=self)
        self.frames["FoodAl"] = FoodAl(parent=container, controller=self)

        self.frames["UserInfo"].grid(row=0, column=0, sticky="nsew")
        self.frames["Home"].grid(row=0, column=0, sticky="nsew")
        self.frames["FoodAl"].grid(row=0, column=0, sticky="nsew")



        self.show_frame("UserInfo")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class UserInfo(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg'] = '#FFFACD'
        # ------------만듬------------
        font = tkfont.Font(size=20, weight='bold')
        l1 = tk.Label(self, height=4, relief="flat", background='#FFFACD', text='User   Info', font=font)
        l1.pack(side=TOP)

        
        #이미지
        photo = Image.open("프로필.png")
        photo = photo.resize((120, 120))
        ph = ImageTk.PhotoImage(photo)
        imglabel1 = tk.Label(self, background='#FFFACD',image=ph)
        imglabel1.image = ph
        imglabel1.place(x=140, y=80)

        #이름
        global nameinfo
        
        font_i = tkfont.Font(size=13)
        name = tk.Label(self, text="이름", background='#FFFACD', font=font_i)
        name.place(x=100, y=210)
        nameinfo = tk.StringVar()
        input1 = tk.Entry(self, width=17, bd=5, textvariable=nameinfo)
        input1.place(x=210, y=210)
        
        # 키
        hei = tk.Label(self, text="키(cm)", background='#FFFACD', font=font_i)
        hei.place(x=100, y=280)
        userinfo1 = tk.StringVar()
        input1 = tk.Entry(self, width=17, bd=5, textvariable=userinfo1)
        input1.place(x=210, y=280)

        # 몸무게
        wei = tk.Label(self, text="몸무게(kg)", background='#FFFACD', font=font_i)
        wei.place(x=100, y=350)
        userinfo2 = tk.StringVar()
        input2 = tk.Entry(self, width=17, bd=5, textvariable=userinfo2)
        input2.place(x=210, y=350)

        # 목적
        global goalval
#         global combo_val
        goal = tk.Label(self, text="목적", background='#FFFACD', font=font_i)
        goal.place(x=100, y=420)
        goalval = tk.StringVar()
        goalCombo = ttk.Combobox(self, width=15, textvariable=goalval)
        goalCombo['values'] = ("선택해주세요", "체중감량", "체중유지", "체중증량")
        goalCombo.current(0)
        goalCombo.place(x=210, y=420)
        print(goalval.get())
#         combo_val = goalval.get()

        

        # ---------------------------------------------------------------
        #font_b = tkfont.Font(size=25)
        button = tk.Button(self, width = 6, height = 1, text="등록", background='#F0E68C', font=font_i,
                           command=lambda: controller.show_frame("Home"))
        button.pack()

        button.place(x=160, y=500)

class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg'] = '#FFFACD'
        totalCal = 0
        calorie = 0
        font = tkinter.font.Font(size=20, weight='bold')

        label = tk.Label(self, height = 5, relief="flat",
                         text="Home", background='#FFFACD', font=font)
        label.pack(side="top", fill="x", pady=10)  
        
        
#         photo2 = Image.open("칼로리1.jpg")
#         photo2 = photo2.resize((200, 250))
#         ph1 = ImageTk.PhotoImage(photo2)
#         imglabel1 = tk.Label(self, background='#FFFACD', image=ph1)
#         imglabel1.image = ph1
#         imglabel1.place(x=20, y=200)
        
        
        photo3 = Image.open("그래프1.png")
        photo3 = photo3.resize((350, 200))
        ph2 = ImageTk.PhotoImage(photo3)
        imglabel2 = tk.Label(self, background='#FFFACD', image=ph2)
        imglabel2.image = ph2
        imglabel2.place(x=20, y=250)
        
        name = tk.Label(self, textvariable=str(nameinfo), background='#FFFACD', font = tkinter.font.Font(size=12))
        name.place(x=55, y=140)
        name1 = tk.Label(self, text = "님  안녕하세요,", background='#FFFACD', font = tkinter.font.Font(size=12))
        name1.place(x=105, y=140)
        kcal = 2000
        global combo_val
        combo_val = goalval.get()
      
        print("val:: ",combo_val)
        print(goalval.get())
        
        
        if(goalval == ''):
            kcal = 1700
        elif (goalval == ''):
            kcal = 2200
        else:
            kcal = 1700
        
        goal_label = tk.Label(self, textvariable = str(goalval), background='#FFFACD', font = tkinter.font.Font(size=10))
        goal_label.place(x=50, y=180)
        name2 = tk.Label(self, text = "을 위한 목표 칼로리는 "+str(kcal)+"kcal 입니다.", background='#FFFACD', font = tkinter.font.Font(size=10))
        name2.place(x=105, y=180)
        
        

        
        # 종료버튼
        button1 = tk.Button(self, width=12, height=2, text="음식 분석하기", background='#cdffeb',
                            command=lambda: controller.show_frame("FoodAl"))
        button1.place(x=210, y=550)

        def close():
            self.quit()

        # 밥먹을 시간입니다 추가
        def restart():
            global self

            try:
                if ('normal' == self.state()):
                    self.destroy()

            finally:
                self = tk.Tk()
                self.geometry("400x700+100+50")
                self.title("FOOD CAMERA")
                self.resizable(False, False)
                self['bg'] = '#FFFACD'

                totalCal = 0
                calorie = 0
                font = tkinter.font.Font(size=20, weight='bold')
                l1 = tk.Label(self, height=5, relief="flat", background='#FFFACD', text='FOOD CAMERA', font=font)
                # l1.place(x = 20, y = 0)
                l1.pack(side=TOP)

                #         photo2 = Image.open("칼로리1.jpg")
                #         photo2 = photo2.resize((200, 250))
                #         ph1 = ImageTk.PhotoImage(photo2)
                #         imglabel1 = tk.Label(self, background='#FFFACD', image=ph1)
                #         imglabel1.image = ph1
                #         imglabel1.place(x=20, y=200)


                photo3 = Image.open("그래프2.png")
                photo3 = photo3.resize((350, 200))
                ph2 = ImageTk.PhotoImage(photo3)
                imglabel2 = tk.Label(self, background='#FFFACD', image=ph2)
                imglabel2.image = ph2
                imglabel2.place(x=20, y=250)

                #왜 연결이 안 될까..?#
                button2 = tk.Button(self, width=12, height=2, text="음식 분석하기", background='#cdffeb',
                                    command=lambda: controller.show_frame("FoodAl"))
                button2.place(x=210, y=550)

                quitButton = tk.Button(self, width=12, height=2, background='#e6e6e6', text="종료", command=close)
                quitButton.place(x=90, y=550)
        
                alarm = tk.Tk()
                alarm.title("For one Alarm")
                alarm['bg'] = '#FFFACD'
                alarm.geometry("200x200+500+300")

                label2 = Label(alarm, text='Meal Time!', width=120, height=150, fg='red', background='#FFFACD',
                               bitmap='info', compound='top', font=45)
                label2.pack()
                # label2.place(x=50,y=50)
                time.sleep(1)
                self.mainloop()

        quitButton1 = tk.Button(self, width=12, height=2, background='#e6e6e6', text="종료", command=restart)
        quitButton1.place(x=90, y=550)

class FoodAl(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#FFFACD')
        font = tkfont.Font(size=15, weight='bold')
        label = tk.Label(self, text="분석중..", font=font, background='#FFFACD')
        label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",command=lambda: controller.show_frame("StartPage"))
        # button.pack()


        stxt = StringVar()
        st = scrolledtext.ScrolledText(self, width=40, height=1)
        st.place(x=50, y=540)
        
        
        

        def openFile():
            global filename
            filename = askopenfilename(title='카메라', filetypes=(("모든 파일", "*.*"), ("GIF파일", "*.gif")))
            photo = Image.open(filename)
            photo = photo.resize((170, 170))
            ph = ImageTk.PhotoImage(photo)
            imglabel1 = tk.Label(self, image=ph)
            imglabel1.image = ph
            imglabel1.place(x=115, y=50)
            print(filename)

            client = vision.ImageAnnotatorClient()

            # 이미지 읽기
            with io.open(filename, 'rb') as image_file:
                content = image_file.read()

            image = types.Image()
            image = vision.Image(content=content)
            response = client.label_detection(image=image)
            
            
            global flag
            flag = "F"
            
            for label in response.label_annotations:
                
                global food
                global foodscore
                print("Label: ", label.description, "/ score: ", label.score)
                if label.description in foodlist:
                    
                    food = label.description
                    foodscore = round(label.score*100, 1)
                    flag = "T"
                    print(food)
                    print(label.score)
                    print(foodscore)


            foodlabel_first = tk.Label(self, text='', background='#FFFACD', width = 50, height = 2)
            foodlabel_first.place(x=10, y=230)
            
            foodlabel = tk.Label(self, text='', background='#FFFACD')
            foodlabel.configure(text=str(foodscore)+'%의 확률로 '+food+'입니다.\n아니면 이름을 입력해주세요')
            foodlabel.place(x=120, y=230)
            
            label = tk.Label(self, text="분석 완료!", font=font, background='#FFFACD')
            label.place(x=150, y = 10)
            
            

        def searchf1():
            global food
            print(flag)
            if flag == "F":
                print("api에 없거나 사용안함")
                food = ''
            elif flag == "T":
                flag == "F"
                
            print(food)
            
            global foodName1
            foodName1 = ''
            foodName1 = food1.get()
            howDish1 = ''
            howDish1 = dish1.get()
            imgname = ''
            
            global totalCal
            if foodName1 == '피자' or food == 'Pizza':
                print("사진입력시 바로 계산되나")
                label1.configure(text='아침: ' + food1.get() + ' 360kcal (한 조각)')
                totalCal += 360 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '치킨' or food == 'Crispy fried chicken' or food == 'Fried food' or food == 'Fried chicken':
                label1.configure(text='아침: ' + food1.get() + ' 300kcal (닭다리 한 조각)')
                totalCal += 300 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '샐러드' or food == 'Salad':
                label1.configure(text='아침: ' + food1.get() + ' 175kcal (그린샐러드 기준)')
                totalCal += 175 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '스테이크' or food == 'Steak' or food == 'Beef':
                label1.configure(text='아침: ' + food1.get() + ' 266kcal (1인분)')
                totalCal += 266 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '파스타' or food == 'Pasta':
                label1.configure(text='아침: ' + food1.get() + ' 660kcal (1인분)')
                totalCal += 660 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '케이크' or food == 'Cake':
                label1.configure(text='아침: ' + food1.get() + ' 213kcal (1인분)')
                totalCal += 213 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '카레밥' or food == 'Rice' or food =='Rice and curry':
                label1.configure(text='아침: ' + food1.get() + ' 544kcal (1인분)')
                totalCal += 544 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '샌드위치' or food == 'Sandwich' or food =='Bread':
                label1.configure(text='아침: ' + food1.get() + ' 252kcal (1인분)')
                totalCal += 252 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '생선구이' or food == 'Fried fish':
                label1.configure(text='아침: ' + food1.get() + ' 123kcal (1인분)')
                totalCal += 123 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '샐러드파스타' or food == 'Rotini':
                label1.configure(text='아침: ' + food1.get() + ' 226kcal (1인분)')
                totalCal += 226 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '팬케이크' or food == 'Pancake':
                label1.configure(text='아침: ' + food1.get() + ' 253kcal (1인분)')
                totalCal += 253 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '초밥' or food == 'Sushi':
                label1.configure(text='아침: ' + food1.get() + ' 446kcal (1인분)')
                totalCal += 446 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '핫도그' or food == 'Hot dog':
                label1.configure(text='아침: ' + food1.get() + ' 242kcal (1인분)')
                totalCal += 242 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '감자튀김' or food == 'Potato wedges':
                label1.configure(text='아침: ' + food1.get() + ' 311kcal (1인분)')
                totalCal += 311 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '브리또' or food == 'Burrito' or food == 'Tortilla':
                label1.configure(text='아침: ' + food1.get() + ' 206kcal (1인분)')
                totalCal += 206 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '타코' or food == 'Taco':
                label1.configure(text='아침: ' + food1.get() + ' 226kcal (1인분)')
                totalCal += 226 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '삼계탕' or food == 'Jjigae' or food =='Stew':
                label1.configure(text='아침: ' + food1.get() + ' 454kcal (1인분)')
                totalCal += 454 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '두부김치' or food == 'Tofu':
                label1.configure(text='아침: ' + food1.get() + ' 237kcal (1인분)')
                totalCal += 237 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '시금치' or food == 'Namul':
                label1.configure(text='아침: ' + food1.get() + ' 64kcal (1인분)')
                totalCal += 64 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '볶음우동' or food == 'Chinese noodles':
                label1.configure(text='아침: ' + food1.get() + ' 400kcal (1인분)')
                totalCal += 400 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '돈까스' or food == 'Tonkatsu':
                label1.configure(text='아침: ' + food1.get() + ' 500kcal (1인분)')
                totalCal += 500 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '콘프라이트' or foodName1 == '시리얼' or food == 'Corn flakes' or food == 'Frosted Flakes':
                label1.configure(text='아침: ' + food1.get() + ' 357kcal (1인분)')
                totalCal += 357 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '카레' or food == 'Yellow curry':
                label1.configure(text='아침: ' + food1.get() + ' 325kcal (1인분)')
                totalCal += 325 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName1 == '만두' or food == 'Mandu':
                label1.configure(text='아침: ' + food1.get() + ' 595kcal (1인분)')
                totalCal += 595 * float(howDish1)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            
            

        def searchf2():
            global food
            if flag == "F":
                print("api에 없거나 사용안함")
                food = ''
            elif flag == "T":
                flag == "F"
                
            global foodName2
            foodName2 = ''
            foodName2 = food2.get()
            howDish2 = ''
            howDish2 = dish2.get()

            global totalCal
            if food1 == None:
                msgbox.showinfo('알림', 'dkffla')
            if foodName2 == '피자' or food == 'Pizza':
                label2.configure(text='점심: ' + food2.get() + ' 360kcal (한 조각)')
                totalCal += 360 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '치킨' or food == 'Crispy fried chicken' or food == 'Fried food' or food =='Fried chicken':
                label2.configure(text='점심: ' + food2.get() + ' 300kcal (닭다리 한 조각)')
                totalCal += 300 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '샐러드' or food == 'Salad':
                label2.configure(text='점심: ' + food2.get() + ' 175kcal (그린샐러드 기준)')
                totalCal += 175 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '스테이크' or food == 'Steak' or food == 'Beef':
                label2.configure(text='점심: ' + food2.get() + ' 266kcal (1인분)')
                totalCal += 266 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')

            elif foodName2 == '파스타' or food == 'Pasta':
                label2.configure(text='점심: ' + food2.get() + ' 660kcal (1인분)')
                totalCal += 660 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '케이크' or food == 'Cake':
                label2.configure(text='점심: ' + food2.get() + ' 213kcal (1인분)')
                totalCal += 213 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '카레밥' or food == 'Rice' or food == 'Rice and curry':
                label2.configure(text='점심: ' + food2.get() + ' 544kcal (1인분)')
                totalCal += 544 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '샌드위치' or food == 'Sandwich' or food == 'Bread':
                label2.configure(text='점심: ' + food2.get() + ' 252kcal (1인분)')
                totalCal += 252 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '생선구이' or food == 'Fried fish':
                label2.configure(text='점심: ' + food2.get() + ' 123kcal (1인분)')
                totalCal += 123 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '샐러드파스타' or food == 'Rotini':
                label2.configure(text='점심: ' + food2.get() + ' 226kcal (1인분)')
                totalCal += 226 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '팬케이크' or food == 'Pancake':
                label2.configure(text='점심: ' + food2.get() + ' 253kcal (1인분)')
                totalCal += 253 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '초밥' or food == 'Sushi':
                label2.configure(text='점심: ' + food2.get() + ' 446kcal (1인분)')
                totalCal += 446 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '핫도그' or food == 'Hot dog':
                label2.configure(text='점심: ' + food2.get() + ' 242kcal (1인분)')
                totalCal += 242 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '감자튀김' or food == 'Potato wedges':
                label2.configure(text='점심: ' + food2.get() + ' 311kcal (1인분)')
                totalCal += 311 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '브리또' or food == 'Burrito' or food == 'Tortilla':
                label2.configure(text='점심: ' + food2.get() + ' 206kcal (1인분)')
                totalCal += 206 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '타코' or food == 'Taco':
                label2.configure(text='점심: ' + food2.get() + ' 226kcal (1인분)')
                totalCal += 226 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '삼계탕' or food == 'Jjigae' or food == 'Stew':
                label2.configure(text='점심: ' + food2.get() + ' 454kcal (1인분)')
                totalCal += 454 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '두부김치' or food == 'Tofu':
                label2.configure(text='점심: ' + food2.get() + ' 237kcal (1인분)')
                totalCal += 237 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '시금치' or food == 'Namul':
                label2.configure(text='점심: ' + food2.get() + ' 64kcal (1인분)')
                totalCal += 64 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '볶음우동' or food == 'Chinese noodles':
                label2.configure(text='점심: ' + food2.get() + ' 400kcal (1인분)')
                totalCal += 400 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '돈까스' or food == 'Tonkatsu':
                label2.configure(text='점심: ' + food2.get() + ' 500kcal (1인분)')
                totalCal += 500 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '콘프라이트' or foodName2 == '시리얼' or food == 'Corn flakes' or food == 'Frosted Flakes':
                label2.configure(text='점심: ' + food2.get() + ' 357kcal (1인분)')
                totalCal += 357 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '카레' or food == 'Yellow curry':
                label2.configure(text='점심: ' + food2.get() + ' 325kcal (1인분)')
                totalCal += 325 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName2 == '만두' or food == 'Mandu':
                label2.configure(text='점심: ' + food2.get() + ' 595kcal (1인분)')
                totalCal += 595 * float(howDish2)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')


        def searchf3():
            global food
            if flag == "F":
                print("api에 없거나 사용안함")
                food = ''
            elif flag == "T":
                flag == "F"
            
            global foodName3
            foodName3 = ''
            foodName3 = food3.get()
            howDish3 = ''
            howDish3 = dish3.get()

            global totalCal
            if foodName3 == '피자' or food == 'Pizza':
                label3.configure(text='저녁: ' + food3.get() + ' 360kcal (한 조각)')
                totalCal += 360 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '치킨' or food == 'Crispy fried chicken' or food == 'Fried food' or food == 'Fried chicken':
                label3.configure(text='저녁: ' + food3.get() + ' 300kcal (닭다리 한 조각)')
                totalCal += 300 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '샐러드' or food == 'Salad':
                label3.configure(text='저녁: ' + food3.get() + ' 175kcal (그린샐러드 기준)')
                totalCal += 175 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '스테이크' or food == 'Steak' or food == 'Beef':
                label3.configure(text='저녁: ' + food3.get() + ' 266kcal (1인분)')
                totalCal += 266 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')

            elif foodName3 == '파스타' or food == 'Pasta':
                label3.configure(text='저녁: ' + food3.get() + ' 660kcal (1인분)')
                totalCal += 660 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '케이크' or food == 'Cake':
                label3.configure(text='저녁: ' + food3.get() + ' 213kcal (1인분)')
                totalCal += 213 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '카레밥' or food == 'Rice' or food == 'Rice and curry':
                label3.configure(text='저녁: ' + food3.get() + ' 544kcal (1인분)')
                totalCal += 544 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '샌드위치' or food == 'Sandwich' or food == 'Bread':
                label3.configure(text='저녁: ' + food3.get() + ' 252kcal (1인분)')
                totalCal += 252 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '생선구이' or food == 'Fried fish':
                label3.configure(text='저녁: ' + food3.get() + ' 123kcal (1인분)')
                totalCal += 123 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '샐러드파스타' or food == 'Rotini':
                label3.configure(text='저녁: ' + food3.get() + ' 226kcal (1인분)')
                totalCal += 226 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '팬케이크' or food == 'Pancake':
                label3.configure(text='저녁: ' + food3.get() + ' 253kcal (1인분)')
                totalCal += 253 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '초밥' or food == 'Sushi':
                label3.configure(text='저녁: ' + food3.get() + ' 446kcal (1인분)')
                totalCal += 446 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '핫도그' or food == 'Hot dog':
                label3.configure(text='저녁: ' + food3.get() + ' 242kcal (1인분)')
                totalCal += 242 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '감자튀김' or food == 'Potato wedges':
                label3.configure(text='저녁: ' + food3.get() + ' 311kcal (1인분)')
                totalCal += 311 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '브리또' or food == 'Burrito' or food == 'Tortilla':
                label3.configure(text='저녁: ' + food3.get() + ' 206kcal (1인분)')
                totalCal += 206 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '타코' or food == 'Taco':
                label3.configure(text='저녁: ' + food3.get() + ' 226kcal (1인분)')
                totalCal += 226 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '삼계탕' or food == 'Jjigae' or food == 'Stew':
                label3.configure(text='저녁: ' + food3.get() + ' 454kcal (1인분)')
                totalCal += 454 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '두부김치' or food == 'Tofu':
                label3.configure(text='저녁: ' + food3.get() + ' 237kcal (1인분)')
                totalCal += 237 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '시금치' or food == 'Namul':
                label3.configure(text='저녁: ' + food3.get() + ' 64kcal (1인분)')
                totalCal += 64 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '볶음우동' or food == 'Chinese noodles':
                label3.configure(text='저녁: ' + food3.get() + ' 400kcal (1인분)')
                totalCal += 400 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '돈까스' or food == 'Tonkatsu':
                label3.configure(text='저녁: ' + food3.get() + ' 500kcal (1인분)')
                totalCal += 500 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '콘프라이트' or foodName3 == '시리얼' or food == 'Corn flakes' or food == 'Frosted Flakes':
                label3.configure(text='저녁: ' + food3.get() + ' 357kcal (1인분)')
                totalCal += 357 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '카레' or food == 'Yellow curry':
                label3.configure(text='저녁: ' + food3.get() + ' 325kcal (1인분)')
                totalCal += 325 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')
            elif foodName3 == '만두' or food == 'Mandu':
                label3.configure(text='저녁: ' + food3.get() + ' 595kcal (1인분)')
                totalCal += 595 * float(howDish3)
                st.delete(1.0, END)
                st.insert(END, '섭취 칼로리는 ' + str(totalCal) + 'kcal 입니다')


                

        def eating():
            global totalCal
            eatval = eat.get()
            if eatval == 1:
                totalCal -= 180

        def dishbutf1():
            global totalCal
            howDish1 = ''
            howDish1 = dish1.get()

        eat = tk.IntVar()

        global flag
        flag = "F"
            
        # 아침
        bre = tk.Label(self, text="아침", background='#FFFACD')
        bre.place(x=55, y=282)
        food1 = tk.StringVar()
        input1 = tk.Entry(self, width=17, bd=3, textvariable=food1)
        input1.place(x=90, y=280)
        

        
        fopen1 = tk.Button(self, width=4, height=1, background='#cde9ff', text="+", command=openFile)
        fopen1.place(x=270, y=280)
        
        search1 = tk.Button(self, width=4, height=1, background='#cdffeb', text="입력", command=searchf1)
        search1.place(x=320, y=280)
        dish1 = tk.StringVar()
        dishInput1 = tk.Entry(self, width=5, textvariable=dish1)
        dishInput1.place(x=90, y=315)
        dishlabel1 = tk.Label(self, text = "인분", background='#FFFACD')
        dishlabel1.place(x=130, y=316)
        label1 = tk.Label(self, text="", background='#FFFACD')
        label1.place(x=90, y=342)

        # 점심
        bre = tk.Label(self, text="점심", background='#FFFACD')
        bre.place(x=55, y=362)
        food2 = tk.StringVar()
        input2 = tk.Entry(self, width=17, bd=3, textvariable=food2)
        input2.place(x=90, y=360)

        
        fopen2 = tk.Button(self, width=4, height=1, background='#cde9ff', text="+", command=openFile)
        fopen2.place(x=270, y=360)
        search2 = tk.Button(self, width=4, height=1, background='#cdffeb', text="입력", command=searchf2)
        search2.place(x=320, y=360)
        dish2 = tk.StringVar()
        dishInput2 = tk.Entry(self, width=5, bd=2, textvariable=dish2)
        dishInput2.place(x=90, y=395)
        dishlabel2 = tk.Label(self, text="인분", background='#FFFACD')
        dishlabel2.place(x=130, y=396)
        label2 = tk.Label(self, text="", background='#FFFACD')
        label2.place(x=90, y=420)
        
        # 저녁
        bre = tk.Label(self, text="저녁", background='#FFFACD')
        bre.place(x=55, y=442)
        food3 = tk.StringVar()
        input3 = tk.Entry(self, width=17, bd=3, textvariable=food3)
        input3.place(x=90, y=440)

        fopen3 = tk.Button(self, width=4, height=1, background='#cde9ff', text="+", command=openFile)
        fopen3.place(x=270, y=435)
        search3 = tk.Button(self, width=4, height=1, background='#cdffeb', text="입력", command=searchf3)
        search3.place(x=320, y=435)
        dish3 = tk.StringVar()
        dishInput3 = tk.Entry(self, width=5, textvariable=dish3)
        dishInput3.place(x=90, y=475)
        dishlabel3 = tk.Label(self, text="인분", background='#FFFACD')
        dishlabel3.place(x=130, y=476)
        label3 = tk.Label(self, text="", background='#FFFACD')
        label3.place(x=90, y=500)  # +50

        OKButton = tk.Button(self, width=8, height=2, text="OK", command=lambda: controller.show_frame("Home"))
        OKButton.place(x=150, y=650)
        


if __name__ == "__main__":
    self = SampleApp()
    self.mainloop()

