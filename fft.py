import numpy as np
import matplotlib.pyplot as plt

HISTROGRAM_LIST = []

for i in range(5):
    data = np.load(f"breathing_data/raw_deep{i+1}.npy")
    T_frame = 9.9e-3  # Calculated from timestamps of collected data
    M, N_samples, N_rx = data.shape

    # plt.figure(figsize=(10, 6))
    # plt.plot(data[:][0])
    # plt.title("Raw UWB Signal", fontsize=15)
    # plt.ylabel("Amplitude", fontsize=15)
    # plt.xlabel("Number of Chirps", fontsize=15)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)

    range_fftAll = np.zeros_like(data, dtype=np.complex_)
    for i in range(M):
        range_fftAll[i] = np.fft.fft(data[i], N_samples, axis=0)

    rangeFFT_all_noStatic = np.diff(range_fftAll, axis=0)

    rangeFFT_avg = np.squeeze(np.mean(range_fftAll, axis=2))
    rangeFFT_avg_no_Static = np.squeeze(np.mean(rangeFFT_all_noStatic, axis=2))
    range_avg = np.squeeze(np.mean(rangeFFT_avg_no_Static, axis=1))
    range_idx = np.argmax(np.abs(range_avg))

    # plt.figure(figsize=(10, 6))
    # plt.plot(rangeFFT_avg)
    # plt.title("FFT with Static Signals", fontsize=15)
    # plt.xlabel("Number of Samples", fontsize=15)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)

    # plt.figure(figsize=(10, 6))
    # plt.plot(rangeFFT_avg_no_Static)
    # plt.title("FFT without Static Signals", fontsize=15)
    # plt.xlabel("Number of Samples", fontsize=15)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)

    br_signal = np.unwrap(np.angle(rangeFFT_avg[:, range_idx]))
    br_time = np.arange(0, M * T_frame, T_frame)
    f_frame = 1 / T_frame
    freq_br = np.arange(0, M) * (f_frame / M)
    br_filter = (freq_br >= 0.2) & (freq_br <= 0.6)
    br_filtered = np.fft.fft(br_signal) * br_filter
    freq_br = freq_br * 60

    br_frequency = np.abs(np.fft.fft(br_signal))

    br_idx = np.where((freq_br >= 8) & (freq_br <= 30))[0]

    br_freqs = freq_br[br_idx]
    br_signal = br_frequency[br_idx]

    br_pk = np.max(br_signal)
    peak_idx_br = np.argmax(br_signal)

    br = round(br_freqs[peak_idx_br])

    print(f"Estimated Breathing Rate: {br}")

    HISTROGRAM_LIST.append(br)

    # plt.figure(figsize=(10, 6))
    # plt.plot(br_hr_signal)
    # plt.title("Breathing Rate Signal", fontsize=15)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)

    # plt.figure(figsize=(10, 6))
    # plt.plot(br_hr_frequency)
    # plt.xlabel("BR/HR (bpm)", fontsize=15)
    # plt.title("Full Spectrum", fontsize=15)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)

    plt.figure(figsize=(10, 6))
    plt.plot(freq_br, br_frequency)
    plt.xlabel("BR (bpm)", fontsize=15)
    plt.xlim(8, 30)
    plt.ylim(0, 25000)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title("Breathing Rate (Movement)", fontsize=15)
    plt.stem([br], [br_pk], "ro")

    plt.show()

bins = np.arange(0, 30, 1)

plt.hist(HISTROGRAM_LIST, bins=bins, edgecolor="black")
plt.xlabel("Breathing Rate (Deep)", fontsize=15)
plt.ylabel("Frequency", fontsize=15)
plt.text(
    0.95,
    0.95,
    f"Avg BPM: {sum(HISTROGRAM_LIST)/len(HISTROGRAM_LIST)}",
    transform=plt.gca().transAxes,
    horizontalalignment="right",
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.5, edgecolor="black"),
)
plt.xlim(7, 25)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.title("Deep BPM Histogram", fontsize=15)
plt.show()
