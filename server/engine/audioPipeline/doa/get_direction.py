import numpy as np
SOUND_SPEED = 343.2
#SOUND_SPEED = 340.0

def gcc_phat(sig, refsig, fs=1, max_tau=None, interp=16):
    '''
    This function computes the offset between the signal sig and the reference signal refsig
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT)method.
    '''
    
    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    # Generalized Cross Correlation Phase Transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)
    R = SIG * np.conj(REFSIG)

    cc = np.fft.irfft(R / np.abs(R), n=(interp * n))

    max_shift = int(interp * n / 2)
    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift+1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cc)) - max_shift

    tau = shift / float(interp * fs)
    
    return tau, cc

def get_direction(queue, channels, sample_rate):
    best_guess = None
    buf_ = b''.join(queue)
    buf = np.frombuffer(buf_, dtype='int16')
    if channels == 6:
        MIC_DISTANCE_6 = 0.09218
        MAX_TDOA_6 = MIC_DISTANCE_6 / float(SOUND_SPEED)
        pair = [[0, 3], [1, 4], [2, 5]]
        tau = [0, 0, 0]
        theta = [0, 0, 0]

        for i, v in enumerate(pair):
            tau[i], _ = gcc_phat(buf[v[0]::channels], buf[v[1]::channels], fs=sample_rate, max_tau=MAX_TDOA_6, interp=1)
            theta[i] = np.arcsin(tau[i] / MAX_TDOA_6) * 180 / np.pi

        min_index = np.argmin(np.abs(tau))
        if (min_index != 0 and theta[min_index - 1] >= 0) or (min_index == 0 and theta[len(pair) - 1] < 0):
            best_guess = (theta[min_index] + 360) % 360
        else:
            best_guess = (180 - theta[min_index])

        best_guess = (best_guess + 30 + min_index * 60) % 360

    elif channels == 4:
        MIC_DISTANCE_4 = 0.08127
        MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)
        pair = [[0, 2], [1, 3]]
        tau = [0, 0]
        theta = [0, 0]

        for i, v in enumerate(pair):
            tau[i], _ = gcc_phat(buf[v[0]::4], buf[v[1]::4], fs=sample_rate, max_tau=MAX_TDOA_4, interp=1)
            theta[i] = np.arcsin(tau[i] / MAX_TDOA_4) * 180 / np.pi

        if np.abs(theta[0]) < np.abs(theta[1]):
            if theta[1] > 0:
                best_guess = (theta[0] + 360) % 360
            else:
                best_guess = (180 - theta[0])
        else:
            if theta[0] < 0:
                best_guess = (theta[1] + 360) % 360
            else:
                best_guess = (180 - theta[1])
            best_guess = (best_guess + 90 + 180) % 360
        best_guess = (-best_guess + 120) % 360

    elif channels == 2:
        pass

    return best_guess, buf_
