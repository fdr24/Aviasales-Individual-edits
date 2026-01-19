import tkinter as tk
from tkinter import ttk, messagebox


def open_purchase_window(route_str, time, price):


    window = tk.Toplevel()
    # создаём валидатор, который позволяет вводить только цифры с клавиатуры
    # (нужен будет для ввода паспортных данных и реквизитов карты)
    def only_digits(new_value):
        return new_value.isdigit() or new_value == ""

    digit_validation = window.register(only_digits)
    window.title("Подтверждение покупки")
    window.geometry("500x670")
    window.resizable(False, False)

    # Создаём фрейм, где пользователь вводит ФИО и дату рождения
    fio_frame = ttk.LabelFrame(window, text="ФИО пассажира", padding=10)
    fio_frame.pack(fill="x", padx=15, pady=10)

    # Фамилия
    ttk.Label(fio_frame, text="Фамилия:").grid(row=0, column=0, sticky="w", pady=5)
    surname_entry = ttk.Entry(fio_frame, width=30)
    surname_entry.grid(row=0, column=1, pady=5)

    # Имя
    ttk.Label(fio_frame, text="Имя:").grid(row=1, column=0, sticky="w", pady=5)
    name_entry = ttk.Entry(fio_frame, width=30)
    name_entry.grid(row=1, column=1, pady=5)

    # Отчество
    ttk.Label(fio_frame, text="Отчество:").grid(row=2, column=0, sticky="w", pady=5)
    patronymic_entry = ttk.Entry(fio_frame, width=30)
    patronymic_entry.grid(row=2, column=1, pady=5)
    #Дата рождения
    ttk.Label(fio_frame, text="Дата рождения (ДД.ММ.ГГГГ):").grid(row=3, column=0, sticky="w", pady=5)
    birth_date_entry = ttk.Entry(fio_frame, width=30)
    birth_date_entry.grid(row=3, column=1, pady=5)

    # Тут создаём фрейм, где пользователь вводит свои паспортные данные
    passport_frame = ttk.LabelFrame(window, text="Паспортные данные", padding=10)
    passport_frame.pack(fill="x", padx=15, pady=10)

    #Используем валидатор, чтобы проверить ввод
    ttk.Label(passport_frame, text="Серия паспорта:").pack(anchor="w")
    passport_series = ttk.Entry(
        passport_frame,
        width=20,
        validate="key",
        validatecommand=(digit_validation, "%P")
    )
    passport_series.pack(pady=3)

    ttk.Label(passport_frame, text="Номер паспорта:").pack(anchor="w")
    passport_number = ttk.Entry(
        passport_frame,
        width=20,
        validate="key",
        validatecommand=(digit_validation, "%P")
    )
    passport_number.pack(pady=3)

    ttk.Label(passport_frame, text="Дата выдачи (ДД.ММ.ГГГГ):").pack(anchor="w")
    passport_date = ttk.Entry(passport_frame, width=20)
    passport_date.pack(pady=3)

    # Фрейм с реквизитами карты
    card_frame = ttk.LabelFrame(window, text="Банковская карта", padding=10)
    card_frame.pack(fill="x", padx=15, pady=10)

    #Также используем валидатор для проверки ввода
    ttk.Label(card_frame, text="Номер карты:").pack(anchor="w")
    card_number = ttk.Entry(
        card_frame,
        width=30,
        validate="key",
        validatecommand=(digit_validation, "%P")
    )
    card_number.pack(pady=3)

    ttk.Label(card_frame, text="Срок действия (ММ/ГГ):").pack(anchor="w")
    card_date = ttk.Entry(card_frame, width=10)
    card_date.pack(pady=3)

    ttk.Label(card_frame, text="CVV:").pack(anchor="w")
    card_cvv = ttk.Entry(
        card_frame,
        width=5,
        show="*",
        validate="key",
        validatecommand=(digit_validation, "%P")
    )
    card_cvv.pack(pady=3)

    # Проверяем, что все поля заполнены
    def confirm_purchase():
        fields = [
            surname_entry.get(),
            name_entry.get(),
            patronymic_entry.get(),
            birth_date_entry.get(),
            passport_series.get(),
            passport_number.get(),
            passport_date.get(),
            card_number.get(),
            card_date.get(),
            card_cvv.get()
        ]

        if not all(fields):
            messagebox.showerror(
                "Ошибка",
                "Пожалуйста, заполните все поля!"
            )
            return

        messagebox.showinfo(
            "Покупка успешна",
            f"🎉 Покупка успешно завершена!\n\n"
            f"Маршрут: {route_str}\n"
            f"Время: {time} ч.\n"
            f"Цена: {int(price)} руб."
        )

        window.destroy()

    ttk.Button(
        window,
        text="✅ Подтвердить покупку",
        command=confirm_purchase,
        width=30
    ).pack(pady=20)