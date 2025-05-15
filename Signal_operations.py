import File_operations as fo

# Funkcje do operacji na sygnałach
def on_add():
    time1, signal1, params1, signal_type1 = fo.load_signal()
    time2, signal2, params2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.add_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2)
        if time is not None:
            params_result = params1.copy()
            fo.save_signal(time, result_signal, params_result, "Dodawanie")
            update_plot_after_operation(time, result_signal, params_result, "Dodawanie")

def on_subtract():
    time1, signal1, params1, signal_type1 = fo.load_signal()
    time2, signal2, params2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.subtract_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2)
        if time is not None:
            params_result = params1.copy()
            fo.save_signal(time, result_signal, params_result, "Odejmowanie")
            update_plot_after_operation(time, result_signal, params_result, "Odejmowanie")

def on_multiply():
    time1, signal1, params1, signal_type1 = fo.load_signal()
    time2, signal2, params2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.multiply_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2)
        if time is not None:
            params_result = params1.copy()
            fo.save_signal(time, result_signal, params_result, "Mnożenie")
            update_plot_after_operation(time, result_signal, params_result, "Mnożenie")

def on_divide():
    time1, signal1, params1, signal_type1 = fo.load_signal()
    time2, signal2, params2, signal_type2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.divide_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2)
        if time is not None:
            params_result = params1.copy()
            fo.save_signal(time, result_signal, params_result, "Dzielenie")
            update_plot_after_operation(time, result_signal, params_result, "Dzielenie")

def update_plot_after_operation(time, result_signal, params, operation_type):
    import main
    mean_value, mean_abs_value, rms_value, variance, mean_power = main.calculate_signal_parameters(time, result_signal, len(time), operation_type)

    params_text = (
        f"Wartość średnia: {mean_value:.4f}\n"
        f"Wartość średnia bezwzględna: {mean_abs_value:.4f}\n"
        f"Wartość skuteczna (RMS): {rms_value:.4f}\n"
        f"Wariancja: {variance:.4f}\n"
        f"Moc średnia: {mean_power:.4f}"
    )
    main.params_label.config(text=params_text)

    signal_type = "Operacja: " + operation_type
    main.plot_signal(main.ax1, time, result_signal, signal_type)
    main.plot_histogram(main.ax2, result_signal, f"Histogram {operation_type}")
    main.canvas.draw()
