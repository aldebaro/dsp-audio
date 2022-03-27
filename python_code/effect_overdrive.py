'''
Demonstrates specific audio effect using digital signal processing (DSP).
This effect is called "Overdrive"
References:
    https://ccrma.stanford.edu/~orchi/Documents/DAFx.pdf
    https://kidpatel.wixsite.com/dspaudioeffects/distortion
Author (modified version): Wilson Cosmo
Date: 25/03/2022

The modification is a verification of the optional input parameters of the Overdrive function (threshold, preGain and outputGain).
The Overdrive function will not work if one of the parameters is a null value, but in graphic mode (audio_effects_graphic_mode.py) the user may input a null value.
These optional input parameters are enabled in "audio_effects_graphic_mode.py" for testing different outputs according with the different input values.  
In case of a null value the user is notified (with a graphic message box) and the original signal is returned.

Original script: https://github.com/aldebaro/dsp-audio/blob/main/python_code/effect_overdrive.py
Original Author: Aldebaro Klautau
'''
import numpy as np
from tkinter import messagebox #library for message box feedback, for use with Graphic mode

#Overdrive effect
def overdrive(sig, threshold: float=2, preGain: float=1.5, outputGain: float=1):
        """
        Function to replicate overdrive effect on a signal.
        This effect usually consists of 1-2 gain stages that are led by a soft-clipping
        diode circuit, soft meaning the clipping circuit won't result in a "clean"
        cut when the signal reaches the clipping region. We can replicate this
        behavior by having a input/output behavior that has a linear-ish region
        close to the x-axis and a smooth curve on each end of the signal limits,
        in this case [-1,1] as the signal is normalized before treatment, such that
        the clipping isn't abrupt as is with the hyperbolic tangent function and
        arc tangent function. This approach avoids the non-linear fitting models
        that would be needed to approximate the circuit behavior.
        As the threshold is increased, the input-output behavior of the soft-clipping
        function will be squished and the signal will clip faster.

        :threshold: intensity of clipping, the higher the value is the lower the
        level will need to be for the clipping process to start.

        :preGain: gain to signal before the application of the signal.

        :outputGain: gain to be applied to the signal after the effect
        """

        if threshold == 0: #if "threshold" is a null value then the function is aborted and the original signal is returned
            messagebox.showerror("Invalid Input", "Threshold value is null, returning original signal") #notify the user
            return sig
        elif preGain == 0: #if "preGain" is a null value then the function is aborted and the original signal is returned
            messagebox.showerror("Invalid Input", "Pre Gain value is null, returning original signal") #notify the user
            return sig
        elif outputGain == 0: #if "outputGain" is a null value then the function is aborted and the original signal is returned
            messagebox.showerror("Invalid Input", "Output Gain value is null, returning original signal") #notify the user
            return sig
        else: #if all values are not null then proceed
            sig *= preGain
            sig = np.tanh(threshold*sig) # Soft Clipping algorithm
            sig *= outputGain # optional output gain
            return sig
