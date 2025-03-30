import File_operations as fo

# Funkcje do operacji na sygnałach
def on_add():
    time1, signal1, frequency1, amplitude1, duration1, sampling_rate1, signal_type1 = fo.load_signal()
    time2, signal2, frequency2, amplitude2, duration2, sampling_rate2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.add_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal, frequency1, amplitude1, duration1, sampling_rate1, None)


def on_subtract():
    time1, signal1, frequency1, amplitude1, duration1, sampling_rate1, signal_type1 = fo.load_signal()
    time2, signal2, frequency2, amplitude2, duration2, sampling_rate2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.subtract_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal, frequency1, amplitude1, duration1, sampling_rate1, None)


def on_multiply():
    time1, signal1, frequency1, amplitude1, duration1, sampling_rate1, signal_type1 = fo.load_signal()
    time2, signal2, frequency2, amplitude2, duration2, sampling_rate2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.multiply_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal, frequency1, amplitude1, duration1, sampling_rate1, None)


def on_divide():
    time1, signal1, frequency1, amplitude1, duration1, sampling_rate1, signal_type1 = fo.load_signal()
    time2, signal2, frequency2, amplitude2, duration2, sampling_rate2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.divide_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal, frequency1, amplitude1, duration1, sampling_rate1, None)
