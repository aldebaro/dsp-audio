'''
Digital Signal Processing - Audio Effects
Graphic mode implemented to simplify multiple tests
Author (Graphic mode): Wilson Cosmo
Date: 26/03/2022

Original script: https://github.com/aldebaro/dsp-audio/blob/main/python_code/audio_effects.py
Original Author: Aldebaro Klautau

Demonstrates some audio effects.
Assume the WAV file is mono, not stereo.
'''

import numpy as np
from scipy.io import wavfile
from audio_util import write_wav_16_bits
#imports of the audio effects:
from effect_chorus import chorus #import of the "chorus" effect
from effect_distortion import distortion #import of the "distortion" effect
from effect_echo import echo #import of the "echo" effect
from effect_flanger import flanger #import of the "flanger" effect
from effect_overdrive import overdrive #import of the "overdrive" effect
from effect_reverb import reverb #import of the "reverb" effect
from effect_wahwah import wahwah #import of the "wah wah" effect
#imports needed for graphic mode:
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
import tkinter as tk
 #import for graph plot:
import matplotlib.pyplot as plt

def show_opt_input(): #function to add optional input for some effects, in this case only "overdrive" and "reverb" have implemented optional inputs for multiple testing
    chosen_effect = e_lst.get()
    if chosen_effect == 'Overdrive': #run the 'chorus' function
        ovis1.set( "2")
        ovis2.set( "1.5")
        ovis3.set( "1")
        ov_op_f.grid(row=0, column=1, padx=10, pady=20)
        mainw.geometry('800x470')
    elif chosen_effect == 'Reverb': #run the 'distortion' function
        rv_op_f.grid(row=0, column=1, padx=10, pady=20)
        mainw.geometry('800x470')
    else: #to add optional inputs for other audio effects a new frame attached to the main window must be created to contain the inputs
        messagebox.showinfo("No optional input", "No optional input for " + chosen_effect) #notify the user

def hide_opt_input(chosen_effect): #hides the optional input frame, called when a new effect is selected from the drop menu
    chosen_effect = e_lst.get()
    ov_op_f.grid_forget()
    rv_op_f.grid_forget()
    mainw.geometry('400x470')

def select_file_df(): #function to load the default test files
    ifs.set("./test_wav_files/sample-16bits.wav")
    ofs.set( "default.wav" )
    rifs.set("./impulse_responses/kingtubby-fl2a-16bits.wav")
    mainw.update_idletasks()

def select_file_if(): #function to load a specific input_file_name
    filetypes = (
        ('Audio files', '*.wav'),
        ('All files', '*.*')
    )
    input_file_name = fd.askopenfilename(
        title='Open a file',
        initialdir='./',
        filetypes=filetypes)
    ifs.set(input_file_name)
    mainw.update_idletasks()

def select_file_ir(): #function to load a specific impulse_response_file_name (optional input of "reverb")
    filetypes = (
        ('Audio files', '*.wav'),
        ('All files', '*.*')
    )
    impulse_response_file_name = fd.askopenfilename(
        title='Open a file',
        initialdir='./',
        filetypes=filetypes)
    rifs.set(impulse_response_file_name)
    mainw.update_idletasks()

def Apply_e(input_file_name, impulse_response_file_name): #main function, apply the selected audio effect
    output_file_name = ofs.get() #get the output_file_name from the Entry
    if output_file_name == '': #if the name is null, use a default name
        output_file_name = 'default.wav'
        messagebox.showwarning("Null output file name", "Null output file name, output file name: default.wav") #notify the user
    elif output_file_name.endswith('.wav'): #if the output_file_name is valid, the function will proceed
        pass
    else: #if the name is a invalid .wav file the the correct file extension is added
        output_file_name = output_file_name + '.wav'
        messagebox.showwarning("Invalid name", "Invalid output file name, output file renamed: " + output_file_name) #notify the user

    if input_file_name == '': #if the input file is null use a default testing file
        input_file_name = './test_wav_files/sample-16bits.wav'
        messagebox.showwarning("Null input file", "Null input file, using default input file: " + input_file_name) #notify the user

    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
    sample_rate, original_signal = wavfile.read(input_file_name) # open the WAV file, confirm it is mono and read the signal
    #signal has a shape (100,2) in case of a stereo signal with 100 samples
    #or (100,) if that original_signal has a single channel (mono)
    num_channels = len(original_signal.shape)
    if num_channels != 1:
        messagebox.showerror("Invalid Signal", "Exception - Signal must be mono") #notify the user
        raise Exception("Signal must be mono!")

    signal = original_signal.astype(np.float) #if original_signal is represented in 16 bits, convert to real numbers to facilitate manipulation
    signal /= np.max(np.abs(signal)) #normalize it to have amplitudes in the range [-1, 1]
    chosen_effect = e_lst.get() #run the selected effect from the drop menu list
    if chosen_effect == 'Chorus': #run the 'chorus' function
        new_signal = chorus(signal, 1.0/sample_rate)
    elif chosen_effect == 'Distortion': #run the 'distortion' function
        new_signal = distortion(signal)
    elif chosen_effect == 'Echo': #run the 'echo' function
        new_signal = echo(signal, 1.0/sample_rate)
    elif chosen_effect == 'Flanger': #run the 'flanger' function
        new_signal = flanger(signal, 1.0/sample_rate)
    elif chosen_effect == 'Overdrive': #run the 'overdrive' function
        new_signal = overdrive(signal, float(ovis1.get()), float(ovis2.get()), float(ovis3.get()))
    elif chosen_effect == 'Reverb': #run the 'reverb' function
        if impulse_response_file_name == '': #if the optional input_response_file_name is null the use a default testing file
            impulse_response_file_name = './impulse_responses/kingtubby-fl2a-16bits.wav'
            messagebox.showwarning("Null file", "Null impulse response file, using default: " + impulse_response_file_name) #notify the user

        ir_sample_rate, impulse_response = wavfile.read(impulse_response_file_name)
        assert(sample_rate == ir_sample_rate) #sample rates must be the same
        new_signal = reverb(signal, impulse_response)
    elif chosen_effect == 'Wah_wah': #run the 'wahwah' function
        new_signal = wahwah(signal, 1.0/sample_rate)
    # write the new signal as a 16-bits WAV file. Handle normalization properly
    write_wav_16_bits(output_file_name, sample_rate, new_signal) # apply the chosen audio effect and generate a new signal
    messagebox.showinfo("Info", "Effect " + chosen_effect + " applied. Output file = " + output_file_name) #notify the user
    if graph_ckbt_var.get() == 1: #if graph is selected, plot the original signal then the new signal
        plt.plot(signal)
        plt.title('Original signal - ' + input_file_name)
        plt.show()
        plt.plot(new_signal)
        plt.title('Signal with ' + chosen_effect + " - " + output_file_name)
        plt.show()

mainw = Tk() #main window of the application
mainw.title('DSP - Audio Effects (Graphic mode)') #window title
mainw.geometry('400x470+10+10') #window dimensions
mainw.resizable(0, 0) #non re-sizable window

mainf = Frame(mainw) #frame containing the main entries
mainf.grid(row=0, column=0, padx=10, pady=20) #positioning the frame in the main window

#objects of the frame "mainf":
ifLb = Label(mainf, text="Insert the input file:", pady=15, padx=10) #static label
ifs = StringVar() #StringVar - input_file_name
ifEt = Entry(mainf, textvariable=ifs) #input field - input_file_name
aeLb = Label(mainf, text="Select the Audio Effect:", pady=15, padx=10) #static label
ofLb = Label(mainf, text="Output file name (example.wav):", pady=15, padx=10) #static label
ofs = StringVar() #StringVar - output_file_name
ofIpF = Entry(mainf, textvariable=ofs) #input field - output_file_name
d_bt = Button(mainf, text="Default Test Files", command=lambda: select_file_df()) #Button to load the default test files
app_bt = Button(mainf, text="Apply Effect", command=lambda: Apply_e(ifs.get(), rifs.get())) #Button to run the selected effect
sf_bt = Button(mainf, text="Select File", command=lambda: select_file_if()) #Button to load a specific input_file_name
op_bt = Button(mainf, text="Show Optional Input", command=lambda: show_opt_input()) #Button to show a frame containing optional inputs
graph_ckbt_var = IntVar() #graphic generator check button var
graph_ckbt = Checkbutton(mainf, text = "Plot Graphic", variable = graph_ckbt_var, onvalue = 1, offvalue = 0, height = 2, width = 10) #graphic generator check button
e_lst = StringVar() #Option Menu - selected string
e_lst.set("Chorus") #Option Menu - default selected string
meffects = OptionMenu(mainf, e_lst, "Chorus", "Distortion", "Echo", "Flanger", "Overdrive", "Reverb", "Wah_wah", command=hide_opt_input) #Option Menu with the list of effects
#Positioning the elements
ifLb.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
sf_bt.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
ifEt.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)
ofLb.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
ofIpF.grid(row=3, column=0, sticky=tk.EW, padx=5, pady=5)
aeLb.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
meffects.grid(row=5, column=0, sticky=tk.EW, padx=5, pady=5)
app_bt.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
graph_ckbt.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
d_bt.grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
op_bt.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)

#overdrive optional input frame
ov_op_f = Frame(mainw) #declaration of the frame attached in the main window "mainw"
ovLB = Label(ov_op_f, text="Overdrive effect - Optional input", pady=15, padx=10) #static label
ovLB1 = Label(ov_op_f, text="Threshold:", pady=15, padx=10) #static label
ovLB2 = Label(ov_op_f, text="Pre Gain:", pady=15, padx=10) #static label
ovLB3 = Label(ov_op_f, text="Output Gain:", pady=15, padx=10) #static label
ovis1 = StringVar() #input field string for "threshold" for the "overdrive" function
ovis1.set("2") #default value of this entry
ovTIf = Entry(ov_op_f, textvariable=ovis1) #input field for "threshold" for the "overdrive" function
ovis2 = StringVar() #input field string for the "overdrive" function
ovis2.set("1.5") #default value of this entry
ovPIf = Entry(ov_op_f, textvariable=ovis2) #input field for "preGain" for the "overdrive" function
ovis3 = StringVar() #input field string for "outputGain" for the "overdrive" function
ovis3.set("1") #default value of this entry
ovOIf = Entry(ov_op_f, textvariable=ovis3) #input field for "outputGain" for the "overdrive" function
#Positioning the elements
ovLB.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
ovLB1.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
ovTIf.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
ovLB2.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
ovPIf.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
ovLB3.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
ovOIf.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

#reverb optional input frame
rv_op_f = Frame(mainw) #declaration of the frame attached in the main window "mainw"
rvLB = Label(rv_op_f, text="Reverb effect - Optional input", pady=15, padx=10) #static label
rvLB2 = Label(rv_op_f, text="Insert the input response file name:", pady=15, padx=10) #static label
rifs = StringVar() #input field string
rIpF = Entry(rv_op_f, textvariable=rifs) #input field for input_response_file_name
ir_bt = Button(rv_op_f, text="Select File", command=lambda: select_file_ir()) #Button to load a specific impulse_response_file_name
#Positioning the elements
rvLB.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
rvLB2.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
rIpF.grid(row=2, column=0, sticky=tk.EW, padx=5, pady=5)
ir_bt.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

mainw.mainloop() #main window loop