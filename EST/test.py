from scipy.signal import butter
fs = 8000
N = 5
Wn = 1000 / (fs*0.5)
b,a = butter(N, Wn, btype='low', analog=False)
print b,a