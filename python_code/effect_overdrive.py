'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called XXX
References:
Author: 
Date: 
'''
import numpy as np

    # Overdrive effect
def overdrive(sig, threshold: float=2, preGain: float=1.5, outputGain: float=1):
        """
        Function to replicate overdrive effect on a signal.
        This effect usually consists of 1-2 gain stages that are led by a soft-clipping
        diode circuit, soft meaning the clipping circuit won't result in a "clean"
        cut when the signal reaches the clipping region. We can replicate this
        behaviour by having a input/output behaviour that has a linear-ish region
        close to the x-axis and a smooth curve on each end of the signal limits,
        in this case [-1,1] as the signal is normalized before treatment, such that
        the clipping isn't abrupt as is with the hyperbolic tangent function and
        arc tangent function. This approach avoids the non-linear fitting models
        that would be needed to approximate the circuit behaviour.
        As the threshold is increased, the input-output behaviour of the soft-clipping
        function will be squished and the signal will clip faster.

        :threshold: intensity of clipping, the higher the value is the lower the
        level will need to be for the clipping process to start.

        :preGain: gain to signal before the application of the signal.

        :outputGain: gain to be applied to the signal after the effect
        """
        #sig = self.normalize(self.sig)
        sig *= preGain
        sig = np.tanh(threshold*sig) # Soft Clipping algorithm
        sig *= outputGain # optional output gain
        #sig = self.denormalize(sig)
        return sig
