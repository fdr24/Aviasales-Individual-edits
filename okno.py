import tkinter as tk
from tkinter import ttk, messagebox
from info import MAJOR_CITIES, generate_random_tickets, get_routes_dict_from_tickets
from filter import get_routes, filter_flights
from datetime import datetime
from purchase_window import open_purchase_window
import random


def run_gui_interface():
    """Запускает графический интерфейс приложения"""

    # Генерируем билеты при запуске
    tickets = generate_random_tickets(count=2000)
    routes_dict = get_routes_dict_from_tickets(tickets)

    # Получаем список всех городов
    cities = [city["name"] for city in MAJOR_CITIES]

    # Создаём главное окно
    root = tk.Tk()
    root.title("Система поиска авиабилетов с фильтрами")
    root.geometry("750x750")

    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Создаем стиль для виджетов
    style = ttk.Style()
    style.theme_use('clam')

    # Настройка стилей
    style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    style.configure('TButton', font=('Arial', 10))
    style.configure('TCombobox', font=('Arial', 10))
    style.configure('TRadiobutton', font=('Arial', 10))

    # Заголовок
    title_label = ttk.Label(root, text="✈️ СИСТЕМА ПОИСКА АВИАБИЛЕТОВ С ФИЛЬТРАМИ", style='Title.TLabel')
    title_label.pack(pady=20)

    # Создаем основной фрейм
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Фрейм для выбора городов
    city_frame = ttk.LabelFrame(main_frame, text="Выбор маршрута", padding=10)
    city_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    # Город отправления
    ttk.Label(city_frame, text="Город отправления:", style='Header.TLabel').grid(row=0, column=0, sticky="w", pady=5)
    from_city = ttk.Combobox(city_frame, values=cities, state="readonly", width=30)
    from_city.set("Выберите город")
    from_city.grid(row=1, column=0, padx=(0, 20), pady=5)

    # Город назначения
    ttk.Label(city_frame, text="Город назначения:", style='Header.TLabel').grid(row=0, column=1, sticky="w", pady=5)
    to_city = ttk.Combobox(city_frame, values=cities, state="readonly", width=30)
    to_city.set("Выберите город")
    to_city.grid(row=1, column=1, pady=5)

    # Фрейм для даты
    date_frame = ttk.LabelFrame(main_frame, text="Выбор даты", padding=10)
    date_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    # Ввод даты
    ttk.Label(date_frame, text="Дата полета (ДД.ММ.ГГ):", style='Header.TLabel').grid(row=0, column=0, sticky="w",
                                                                                      pady=5)
    date_entry = ttk.Entry(date_frame, width=20, font=('Arial', 10))
    date_entry.grid(row=1, column=0, pady=5)
    date_entry.insert(0, "01.01.26")

    # Кнопка для генерации случайной даты
    def generate_random_date():
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = 26  # 2026
        date_str = f"{day:02d}.{month:02d}.{year:02d}"
        date_entry.delete(0, tk.END)
        date_entry.insert(0, date_str)

    ttk.Button(date_frame, text="Случайная дата", command=generate_random_date, width=15).grid(row=1, column=1, padx=10)

    # Фрейм для выбора типа фильтра
    filter_frame = ttk.LabelFrame(main_frame, text="Тип фильтрации", padding=10)
    filter_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    filter_var = tk.StringVar(value="all")

    # Радиокнопки для выбора типа фильтра
    ttk.Radiobutton(
        filter_frame, text="Самые быстрые",
        variable=filter_var, value="fastest"
    ).grid(row=0, column=0, sticky="w", pady=2)

    ttk.Radiobutton(
        filter_frame, text="Самые дешевые",
        variable=filter_var, value="cheapest"
    ).grid(row=1, column=0, sticky="w", pady=2)

    ttk.Radiobutton(
        filter_frame, text="Только прямые рейсы",
        variable=filter_var, value="direct"
    ).grid(row=0, column=1, sticky="w", pady=2, padx=(20, 0))

    ttk.Radiobutton(
        filter_frame, text="Только с 1 пересадкой",
        variable=filter_var, value="one_stop"
    ).grid(row=1, column=1, sticky="w", pady=2, padx=(20, 0))

    ttk.Radiobutton(
        filter_frame, text="Все варианты",
        variable=filter_var, value="all"
    ).grid(row=2, column=0, sticky="w", pady=2, columnspan=2)

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)

    # Окно вывода результатов
    result_frame = ttk.LabelFrame(main_frame, text="Результаты поиска", padding=10)
    result_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
    main_frame.rowconfigure(4, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # Создаем Text виджет с прокруткой
    result_text = tk.Text(result_frame, height=15, width=70, wrap=tk.WORD, font=('Arial', 10))
    result_scroll = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    result_text.configure(yscrollcommand=result_scroll.set)

    result_text.grid(row=0, column=0, sticky="nsew")
    result_scroll.grid(row=0, column=1, sticky="ns")

    result_frame.rowconfigure(0, weight=1)
    result_frame.columnconfigure(0, weight=1)

    # Настройка тегов для форматирования
    result_text.tag_configure("title", font=('Arial', 12, 'bold'), foreground='#2c3e50')
    result_text.tag_configure("route", font=('Arial', 11, 'bold'), foreground='#2980b9')
    result_text.tag_configure("info", font=('Arial', 10), foreground='#34495e')
    result_text.tag_configure("warning", font=('Arial', 10, 'italic'), foreground='#e74c3c')
    result_text.tag_configure("success", font=('Arial', 10, 'bold'), foreground='#27ae60')
    result_text.tag_configure("center", justify="center")
    result_text.tag_configure("filter_info", font=('Arial', 10, 'italic'), foreground='#8e44ad')  # НОВЫЙ тег

    def buy_ticket(route):
        route_str, time, price = route
        messagebox.showinfo(
            "Покупка билета",
            f"Вы выбрали билет:\n\n"
            f"Маршрут: {route_str}\n"
            f"Время в пути: {time} ч.\n"
            f"Цена: {int(price)} руб.\n\n"
            f"Дальнейшая покупка будет реализована позже."
        )

    def search():
        """Выполняет поиск билетов с использованием фильтров"""
        fc = from_city.get()
        tc = to_city.get()
        date = date_entry.get()
        filter_type = filter_var.get()

        # Проверки ввода
        if fc == "Выберите город" and tc == "Выберите город":
            messagebox.showerror("Ошибка", "Выберите город вылета и город прибытия")
            return
        if fc == "Выберите город":
            messagebox.showerror("Ошибка", "Выберите город вылета")
            return
        if tc == "Выберите город":
            messagebox.showerror("Ошибка", "Выберите город прибытия")
            return
        if fc == tc:
            messagebox.showerror("Ошибка", "Город вылета и прибытия не могут совпадать")
            return

        # Проверка формата даты
        try:
            datetime.strptime(date, "%d.%m.%y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГ (например, 01.01.26)")
            return

        # Очищаем поле результатов
        result_text.delete(1.0, tk.END)

        # Показываем статус поиска
        result_text.insert(tk.END, "🔍 Поиск билетов...\n\n", "title")
        result_text.update()

        try:
            # Ищем маршруты с использованием  функции filter_flights
            filtered_routes = filter_flights(fc, tc, filter_type)

            # Применяем праздничные наценки (только для отображения)
            if filtered_routes:
                # Преобразуем формат для holiday_price
                routes_for_holiday = []
                for route in filtered_routes:
                    # Преобразуем кортеж в список для совместимости
                    route_list = list(route)
                    routes_for_holiday.append(route_list)


                # Преобразуем обратно в кортежи
                filtered_routes = []
                for route_list in routes_for_holiday:
                    filtered_routes.append(tuple(route_list))

            if not filtered_routes:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "❌ Рейсы не найдены\n\n", "title")
                result_text.insert(tk.END, "К сожалению, на выбранный маршрут и дату билеты не найдены.\n", "info")
                result_text.insert(tk.END, "Попробуйте:\n", "info")
                result_text.insert(tk.END, "• Изменить тип фильтра\n", "info")
                result_text.insert(tk.END, "• Выбрать другие города\n", "info")
                result_text.insert(tk.END, "• Выбрать другую дату\n", "info")
            else:
                result_text.delete(1.0, tk.END)

                # Заголовок результатов с информацией о фильтре
                filter_names = {
                    "fastest": "Самые быстрые",
                    "cheapest": "Самые дешевые",
                    "direct": "Только прямые",
                    "one_stop": "Только с 1 пересадкой",
                    "all": "Все варианты"
                }

                result_text.insert(tk.END, f"✅ Найдено рейсов: {len(filtered_routes)}\n\n", "title")
                result_text.insert(tk.END, f"Маршрут: {fc} → {tc}\n", "route")
                result_text.insert(tk.END, f"Дата: {date}\n", "route")
                result_text.insert(tk.END, f"Тип фильтра: {filter_names[filter_type]}\n", "filter_info")  # ИЗМЕНЕНО
                result_text.insert(tk.END, "─" * 60 + "\n\n", "info")


                # Выводим найденные маршруты
                for i, route in enumerate(filtered_routes, 1):
                    route_str, time, price = route
                    time_str = str(time) if time % 1 != 0 else str(int(time))

                    result_text.insert(tk.END, f"Вариант {i}:\n", "success")
                    result_text.insert(tk.END, f"  Маршрут: {route_str}\n", "info")
                    result_text.insert(tk.END, f"  Время в пути: {time_str} часов\n", "info")
                    result_text.insert(tk.END, f"  Стоимость: {int(price)} руб.\n", "info")

                    # Кнопка "Купить"
                    buy_btn = ttk.Button(
                        result_text,
                        text="🛒 Купить",
                        command=lambda r=route: open_purchase_window(
                            r[0],  # route_str
                            r[1],  # time
                            r[2]  # price
                        )
                    )

                    result_text.window_create(tk.END, window=buy_btn)
                    result_text.insert(tk.END, "\n")

                    if i < len(filtered_routes):
                        result_text.insert(tk.END, "\n" + "•" * 40 + "\n\n", "info")
                    else:
                        result_text.insert(tk.END, "\n" + "═" * 60 + "\n\n", "info")

                result_text.insert(tk.END, "🎫 Выберите подходящий вариант и обратитесь в кассу!\n", "success")

        except ValueError as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"❌ Ошибка поиска\n\n", "title")
            result_text.insert(tk.END, f"{str(e)}\n\n", "warning")
            result_text.insert(tk.END, "Проверьте правильность введенных данных.\n", "info")

    def clear_all():
        """Очищает все поля"""
        from_city.set("Выберите город")
        to_city.set("Выберите город")
        date_entry.delete(0, tk.END)
        date_entry.insert(0, "01.01.26")
        filter_var.set("all")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Готов к поиску...\n\n", "title")
        result_text.insert(tk.END, "Выберите города, дату и тип фильтра,\n", "info")
        result_text.insert(tk.END, "затем нажмите 'Найти билеты'.\n", "info")

    def exit_app():
        """Выход из приложения"""
        root.quit()
        root.destroy()

    # Создаем кнопки
    ttk.Button(button_frame, text="🔍 Найти билеты", command=search, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="🧹 Очистить всё", command=clear_all, width=15).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="🚪 Выход", command=exit_app, width=15).pack(side=tk.LEFT, padx=5)

    # Инициализируем поле результатов
    clear_all()

    # Запускаем главный цикл
    root.mainloop()


# Если файл запущен напрямую, запускаем интерфейс
if __name__ == "__main__":
    run_gui_interface()

#выполнил Рыбин Фёдор ИСУ: 504 995