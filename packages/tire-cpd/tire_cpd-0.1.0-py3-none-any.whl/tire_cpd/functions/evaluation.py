import numpy as np
from tire_cpd.functions import postprocessing, utils
from tire_cpd.functions import metrics
from scipy.signal import find_peaks


def show_result(dissimilarities, window_size):
    detected_peaks = find_peaks(dissimilarities)[0]
    print("detected change points:")
    print(detected_peaks + window_size)


def show_result_multi_channel(window_size, dissimilarities, loss_coherent, loss_incoherent):
    ratio = loss_incoherent/(loss_coherent + loss_incoherent)
    large_ratio = ratio[ratio >= 0.65]
    small_ratio = ratio[ratio < 0.65]
    if small_ratio.size == 0:
        small_ratio = [0]

    # check ratio to assign change-types
    peaks_AS = find_peaks(dissimilarities['A&S'])[0]
    peaks_B = find_peaks(dissimilarities['B'])[0]
    if np.mean(small_ratio) < 0.25 and large_ratio.size != 0:
        peaks_both = []
        selected_peaks_AS = []
        selected_peaks_B = peaks_B

    elif np.mean(ratio) < 0.25:
        peaks_both = []
        selected_peaks_AS = peaks_AS
        selected_peaks_B = []

    # merge detections from two branches
    else:
        peaks_both = []
        new_peaks_AS = []
        peaks_B_bu = peaks_B
        stop_point = peaks_AS[-1]
        nr_AS = int(0.1 * peaks_AS.size)
        nr_B = int(0.1 * peaks_B.size)
        # find overlaps of two branches
        for peak_AS in peaks_AS:
            if peaks_B.size == 0:
                stop_point = peak_AS
                break
            nearst_peak = peaks_B[np.abs(peaks_B - peak_AS).argmin()]
            if np.abs(nearst_peak - peak_AS) <= window_size:
                peaks_B = np.delete(peaks_B, np.where(peaks_B == nearst_peak))
                alpha = dissimilarities['A&S'][peak_AS] / np.mean(np.sort(dissimilarities['A&S'][peaks_AS])[-nr_AS:])
                beta = dissimilarities['B'][nearst_peak] / np.mean(np.sort(dissimilarities['B'][peaks_B_bu])[-nr_B:])
                merged_loc = np.around((alpha * peak_AS + beta * nearst_peak) / (alpha + beta)).astype(int)
                peaks_both.append(merged_loc)
            else:
                new_peaks_AS.append(peak_AS)
        new_peaks_AS = np.asarray(np.concatenate([new_peaks_AS, peaks_AS[np.argwhere(peaks_AS == stop_point)
                                                                         [0][0]:]], axis=0), dtype=np.int64)
        new_peaks_B = np.asarray(peaks_B, dtype=np.int64)
        peaks_B = find_peaks(dissimilarities['B'])[0]

        # only take significant changes in each branch

        selected_peaks_AS = np.array(new_peaks_AS)[list(np.where(dissimilarities['A&S'][new_peaks_AS] >= 0.25 *
                                                   np.mean(np.sort(dissimilarities['A&S'][peaks_AS])[-nr_AS:])))[0]]
        selected_peaks_B = np.array(new_peaks_B)[list(np.where(dissimilarities['B'][new_peaks_B] >= 0.25 *
                                                 np.mean(np.sort(dissimilarities['B'][peaks_B])[-nr_B:])))[0]]
        selected_peaks_AS = utils.overlap_test(selected_peaks_AS, np.array(peaks_both), window_size)
        selected_peaks_B = utils.overlap_test(selected_peaks_B, np.array(peaks_both), window_size)
    detected_peaks = np.sort(np.concatenate((selected_peaks_AS, selected_peaks_B, peaks_both)))
    print("detected change points:")
    print(detected_peaks + window_size)


def smoothened_dissimilarity_measures(encoded_windows, encoded_windows_fft, domain, window_size):
    """
    Calculation of smoothened dissimilarity measures

    Args:
        encoded_windows: TD latent representation of windows
        encoded_windows_fft:  FD latent representation of windows
        domain: TD/FD/both
        window_size: window size used

    Returns:
        smoothened dissimilarity measures
    """

    if domain == "TD":
        encoded_windows_both = encoded_windows
    elif domain == "FD":
        encoded_windows_both = encoded_windows_fft
    elif domain == "both":
        beta = np.quantile(postprocessing.distance(encoded_windows, window_size), 0.95)
        alpha = np.quantile(postprocessing.distance(encoded_windows_fft, window_size), 0.95)
        encoded_windows_both = np.concatenate((encoded_windows * alpha, encoded_windows_fft * beta), axis=1)

    encoded_windows_both = postprocessing.matched_filter(encoded_windows_both, window_size)
    distances = postprocessing.distance(encoded_windows_both, window_size)
    distances = postprocessing.matched_filter(distances, window_size)

    return distances


def smoothened_dissimilarity_measures_multiview(encoded_windows, window_size):
    """
    Calculation of smoothened dissimilarity measures

    Args:
        encoded_windows: latent representation of windows
        window_size: window size used

    Returns:
        smoothened dissimilarity measures
    """
    encoded_windows_both = postprocessing.matched_filter(encoded_windows, window_size)
    distances = postprocessing.distance(encoded_windows_both, window_size)
    distances = postprocessing.matched_filter(distances, window_size)
    return distances


def smoothened_dissimilarity_measures_multichannel(encoded_AS, encoded_AS_fft, encoded_B, encoded_B_fft, window_size):
    # window_size = 40
    if encoded_AS_fft is None:
        encoded_AS_both = encoded_AS
        encoded_B_both = encoded_B
    elif encoded_AS is None:
        encoded_AS_both = encoded_AS_fft
        encoded_B_both = encoded_B_fft
    else:
        beta_AS = np.quantile(postprocessing.distance(encoded_AS, window_size), 0.95)
        alpha_AS = np.quantile(postprocessing.distance(encoded_AS_fft, window_size), 0.95)
        encoded_AS_both = np.concatenate((encoded_AS * alpha_AS, encoded_AS_fft * beta_AS), axis=1)
        beta_B = np.quantile(postprocessing.distance(encoded_B, window_size), 0.95)
        alpha_B = np.quantile(postprocessing.distance(encoded_B_fft, window_size), 0.95)
        encoded_B_both = np.concatenate((encoded_B * alpha_B, encoded_B_fft * beta_B), axis=1)
    distances = {"A&S":[], "B":[]}

    encoded_windows_both = {"A&S": postprocessing.matched_filter(encoded_AS_both, window_size),
                            "B": postprocessing.matched_filter(encoded_B_both, window_size)}
    for idx, value in encoded_windows_both.items():
        distances[idx] = postprocessing.matched_filter(postprocessing.distance(value, window_size), window_size)
    return distances

