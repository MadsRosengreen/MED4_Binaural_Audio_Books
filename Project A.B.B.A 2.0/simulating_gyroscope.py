import pyglet
import sofa
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import *

hrtf_database = sofa.Database.open('QU_KEMAR_anechoic_3m.sofa')

# recording
sampling_freq = 48000
sd.default.samplerate = sampling_freq
sd.default.channels = (1, 2)
rec_time = 1 # seconds

mic_data = sd.rec(rec_time * sampling_freq)
mic_data_transposed = mic_data.transpose()

print("Recording...")
sd.wait()
print("Recording ended.")


population = [(90, 200), (91, 20), (92, 20), (93, 20), (94, 20), (95, 20), (96, 20), (97, 20), (98, 20),
              (99, 20), (100, 20), (101, 20), (-1, 200)]

output_ear1 = np.zeros([1, rec_time * sampling_freq])
output_ear2 = np.zeros([1, rec_time * sampling_freq])





elapsed_duration = 0

for position in population:
    angle = position[0]
    duration = position[1]

    ir_ear1 = hrtf_database.Data.IR.get_values(indices={"M": position[0], "R": 0, "E": 0})
    ir_ear2 = hrtf_database.Data.IR.get_values(indices={"M": position[0], "R": 1, "E": 0})

    start_index = elapsed_duration
    end_index = elapsed_duration + duration
    elapsed_duration += duration

    if start_index == 0:
        initial_state1 = lfilter_zi(ir_ear1, 1)
        initial_state2 = lfilter_zi(ir_ear2, 1)

        output_ear1[0, start_index:end_index], filter_state1 = \
            lfilter(ir_ear1, 1, mic_data_transposed[0, start_index:end_index], zi=initial_state1)
        output_ear2[0, start_index:end_index], filter_state2 = \
            lfilter(ir_ear2, 1, mic_data_transposed[0, start_index:end_index], zi=initial_state2)

    else:
        output_ear1[0, start_index:end_index], filter_state1 = \
            lfilter(ir_ear1, 1, mic_data_transposed[0, start_index:end_index], zi=filter_state1)
        output_ear2[0, start_index:end_index], filter_state2 = \
            lfilter(ir_ear2, 1, mic_data_transposed[0, start_index:end_index], zi=filter_state2)



print("Playing...")
sd.wait()
print("Playback ended.")

