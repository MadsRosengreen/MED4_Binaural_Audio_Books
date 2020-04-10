import sofa
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import *
import matplotlib.pyplot as plt

hrtf_database = sofa.Database.open('QU_KEMAR_anechoic_3m.sofa')

data, sampling_freq = sf.read('sample.wav')
input_transposed_right = np.reshape(data[:, 0], (-1, 1)).transpose()
input_transposed_left = np.reshape(data[:, 1], (-1, 1)).transpose()

total_samples = data.shape[0]
total_different_positions = 360

# creating a data structure that will store all the transforming information..
# I think the best and most efficient way to store it is

population = []
for i in range(total_different_positions):
    population.append((i, total_samples // total_different_positions if i > 0 else total_samples % total_different_positions))
    # split the total_samples (e.g. 720 000) evenly between total_different_positions (e.g. 360), but because it might not be
    # an integer, take the mod of it once. (say you have 13 samples and 5 positions - it would be split like [1, 3, 3, 3, 3]..
    # temporary implementation choice


output_ear_right = np.zeros([1, total_samples])
output_ear_left = np.zeros([1, total_samples])
# output_ear_left = np.zeros([1, total_samples])

filter_state_right = 0
filter_state_left = 0
elapsed_duration = 0

for position in population:
    angle = position[0]
    duration = position[1]

    ir_ear_right = hrtf_database.Data.IR.get_values(indices={"M": angle, "R": 0, "E": 0})
    ir_ear_left = hrtf_database.Data.IR.get_values(indices={"M": angle, "R": 1, "E": 0})

    start_index = elapsed_duration
    elapsed_duration += duration
    end_index = elapsed_duration

    if start_index == 0:
        filter_state_right = lfilter_zi(ir_ear_right, 1)
        filter_state_left = lfilter_zi(ir_ear_left, 1)

    output_ear_right[0, start_index:end_index], filter_state_right = \
        lfilter(ir_ear_right, 1, input_transposed_right[0, start_index:end_index], zi=filter_state_right)
    output_ear_left[0, start_index:end_index], filter_state_left = \
        lfilter(ir_ear_left, 1, input_transposed_left[0, start_index:end_index], zi=filter_state_left)

output = np.append(output_ear_right.transpose(), output_ear_left.transpose(), axis=1)

# sd.play(output, sampling_freq)
sd.play(output, sampling_freq)
sf.write("sample_modified.wav", output, sampling_freq)


print("Playing...")
sd.wait()
print("Playback ended.")

