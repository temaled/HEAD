from sox.transform import Transformer
import numpy as np

Voiced_Regions = Transformer()
Voiced_Regions.vad(-1,True,initial_pad=0.3)
filenameIn = "/home/dere/Desktop/HarvardSentences/Test1.wav"
filenameout = "/home/dere/Desktop/HarvardSentences/Testvad.wav"
Voiced_Regions.build(filenameIn,filenameout)
