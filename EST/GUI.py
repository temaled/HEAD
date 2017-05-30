#!/usr/bin/env python

try:
	import Tkinter as tk
	import ttk
except:
	import tkinter as tk
	from tkinter import ttk

import tkFileDialog



class EmoTrans:
    
    def __init__(self, master):
        self.master=master
        master.title("Emotion")
	
        self.file_path=tk.StringVar()
        self.selected_emotion=tk.StringVar()
        self.selected_frequency=tk.IntVar()
        self.emotion_intensity=tk.DoubleVar() 
        self.log_chunk=tk.IntVar()
        self.chunk_size=tk.IntVar()

#File browser       
#*************************************************#
        self.browse_frame=tk.Frame(master, height=20, width=300)
        self.browse_frame.pack()
        self.browse_frame.place(x=60, y=70)
        
        
        self.path_field=tk.Entry(self.browse_frame, textvariable=self.file_path, width=45)
        self.path_field.pack(side=tk.LEFT)
        
        self.browse_button=tk.Button(self.browse_frame, text='Choose File', command=self.open_file)
        self.browse_button.pack(side=tk.RIGHT)
        
        
#Emotion and intensity
#*************************************************#
        self.emotion_frame=tk.Frame(master, height=300, width=200)
        self.emotion_frame.pack()
        self.emotion_frame.place(x=60, y=110)

        self.emo_label=tk.Label(self.emotion_frame, text="\nGenerate file for")
        self.emo_label.pack()
        
        self.radio_happy=tk.Radiobutton(self.emotion_frame, text='Happy', variable=self.selected_emotion, value='happy')
        self.radio_happy.pack(anchor=tk.W)
        self.radio_sad=tk.Radiobutton(self.emotion_frame, text='Sad', variable=self.selected_emotion, value='sad')
        self.radio_sad.pack(anchor=tk.W)
        self.radio_angry=tk.Radiobutton(self.emotion_frame, text='Angry', variable=self.selected_emotion, value='angry')
        self.radio_angry.pack(anchor=tk.W)
        self.radio_happy_tensed=tk.Radiobutton(self.emotion_frame, text='Happy Tensed', variable=self.selected_emotion,
                                               value='happy_tensed')
        self.radio_happy_tensed.pack(anchor=tk.W)

        self.int_label=tk.Label(self.emotion_frame, text="\nEmotion Intensity")
        self.int_label.pack()
        
        self.emo_int=tk.Scale(self.emotion_frame, variable=self.emotion_intensity,orient=tk.HORIZONTAL, length=100, command=self.update_intensity, showvalue=0)
        self.emo_int.pack()
        self.emo_int.set(100)
        
        self.percent=tk.Label(self.emotion_frame, text=str(self.emo_int.get())+'%')
        self.percent.pack(anchor=tk.E)
        
        self.radio_happy.select()
        self.radio_sad.deselect()
        self.radio_angry.deselect()
        self.radio_happy_tensed.deselect()
        
#Sampling frequency
#*************************************************#
        self.frequency_frame=tk.Frame(master, height=50, width=50)
        self.frequency_frame.pack()
        self.frequency_frame.place(x=340, y=110)
        
        self.freq_label=tk.Label(self.frequency_frame, text="\nSampling Frequency")
        self.freq_label.pack()
        
        self.fs_list=ttk.Combobox(self.frequency_frame,state='readonly',  values=['8,000 Hz','11,025 Hz','22,050 Hz','44,100 Hz'])
        self.fs_list.current(0)
        self.fs_list.pack()
        
#Chunk size
#*************************************************#
        self.chunk_frame=tk.Frame(master, width=200, height=200)
        self.chunk_frame.pack()
        self.chunk_frame.place(x=340, y=200)
        
        self.chunk_label=tk.Label(self.chunk_frame, text="\nChunk Size")
        self.chunk_label.pack(anchor=tk.W)

        self.two_label=tk.Label(self.chunk_frame, text ="2 ^ ")
        self.two_label.pack(side=tk.LEFT)

        self.log_chunk.set(10)
        self.chunk_size.set(1024)

        self.chunk_spinner=tk.Spinbox(self.chunk_frame,state="readonly",width=15, textvariable=self.log_chunk, from_=6, to=20, wrap=True, command=self.update_chunk)
        self.chunk_spinner.pack(side=tk.RIGHT)

        self.size_label=tk.Label(self.chunk_frame, textvariable=self.chunk_size)
        self.size_label.pack()
        self.size_label.place(x=100, y=15)

        self.generate_button=tk.Button(master,text='Generate', command=self.generate_file)
        self.generate_button.pack()
        self.generate_button.place(x=440, y=280)



        
#*************************************************#
        
        #********** END OF WIDGETS **********#
        
    def print_emotion(self):
        print (self.selected_emotion.get())
        print (self.emotion_intensity.get())
        print (self.fs_list.get())
        print (self.file_path.get())
        
    def update_intensity(self,val):
        self.percent.config(text=str(val)+'%')

    def open_file(self):
    	self.file_path.set(tkFileDialog.askopenfilename(initialdir='.', title="Select File", filetypes=(("WAVE files","*.wav"), ("All files", "*.*"))))

    def update_chunk(self):
    	self.chunk_size.set(pow(2, self.log_chunk.get()))

    def generate_file(self):
    	pass


    
root=tk.Tk()
root.style=ttk.Style()
root.style.theme_use("clam")
#('clam', 'alt', 'default', 'classic')

root.geometry('{}x{}'.format(570, 350))
root.resizable(width=False, height=False)
my_gui=EmoTrans(root)
root.mainloop()
