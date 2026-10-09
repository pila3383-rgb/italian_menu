import tkinter as tk
from tkinter import ttk, messagebox

# Данные меню: категории, блюда, описание и цены (в рублях)
ITALIAN_MENU = {
    "Пицца 🍕": [
        {"name": "Маргарита", "description": "Томатный соус, моцарелла, базилик", "price": 390},
        {"name": "Пепперони", "description": "Острая колбаса пепперони, моцарелла, томатный соус", "price": 490},
        {"name": "Четыре сыра", "description": "Моцарелла, горгонзола, пармезан, скаморца", "price": 540},
        {"name": "Дьявола", "description": "Пикантная колбаса, перец халапеньо, моцарелла", "price": 520}
    ],
    "Паста 🍝": [
        {"name": "Карбонара", "description": "Спагетти, бекон, яичный желток, пармезан, сливки", "price": 450},
        {"name": "Болоньезе", "description": "Классический мясной соус, томаты, чеснок, базилик", "price": 480},
        {"name": "Феттуччини с грибами", "description": "Феттуччини, белые грибы, нежный сливочный соус", "price": 420}
    ],
    "Закуски 🥗": [
        {"name": "Цезарь с курицей", "description": "Листья салата, куриное филе, гренки, соус цезарь", "price": 380},
        {"name": "Капрезе", "description": "Томаты, моцарелла, соус песто, базилик", "price": 350},
        {"name": "Брускетта с томатами", "description": "Хрустящий багет, томаты, чеснок, оливковое масло", "price": 240}
    ],
    "Десерты 🍰": [
        {"name": "Тирамису", "description": "Маскарпоне, печенье савоярди, кофе, какао", "price": 320},
        {"name": "Панна-котта", "description": "Сливочное желе с ароматным ягодным топпингом", "price": 280}
    ],
    "Напитки ☕": [
        {"name": "Эспрессо", "description": "Классический крепкий кофе", "price": 120},
        {"name": "Капучино", "description": "Кофе с воздушной молочной пенкой", "price": 180},
        {"name": "Домашний лимонад", "description": "Цитрусовый освежающий напиток собственного приготовления", "price": 200}
    ]
}

class ItalianMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trattoria Bella — Электронное Меню")
        self.root.geometry("950x650")
        self.root.configure(bg="#f8f9fa")

        # Корзина покупок: {название_блюда: {"price": цена, "quantity": кол-во}}
        self.cart = {}

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Настройка шрифтов и цветов в итальянском стиле
        self.style.configure("TLabel", background="#f8f9fa", font=("Helvetica", 11))
        self.style.configure("Category.TButton", font=("Helvetica", 11, "bold"), padding=8)
        self.style.configure("Menu.TButton", font=("Helvetica", 10), background="#27ae60", foreground="white")
        self.style.map("Menu.TButton", background=[("active", "#219653")])

    def create_widgets(self):
        # Шапка приложения
        header_frame = tk.Frame(self.root, bg="#2c3e50")
        header_frame.pack(fill="x")
        
        title_label = tk.Label(header_frame, text="🇮🇹 Trattoria Bella 🇮🇹", font=("Georgia", 24, "bold"), fg="#ffffff", bg="#2c3e50")
        title_label.pack(pady=(10, 2))
        
        subtitle_label = tk.Label(header_frame, text="Традиционная итальянская кухня", font=("Georgia", 11, "italic"), fg="#bdc3c7", bg="#2c3e50")
        subtitle_label.pack(pady=(0, 10))

        # Главный контейнер
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Левая панель: Категории
        self.cat_frame = tk.Frame(main_frame, width=180, bg="#f8f9fa")
        self.cat_frame.pack(side="left", fill="y", padx=(0, 15))
        
        tk.Label(self.cat_frame, text="Категории", font=("Helvetica", 13, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        for category in ITALIAN_MENU.keys():
            btn = ttk.Button(self.cat_frame, text=category, style="Category.TButton", 
                             command=lambda c=category: self.show_category(c))
            btn.pack(fill="x", pady=4)

        # Центральная панель: Список блюд (с прокруткой)
        self.menu_canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.menu_canvas.yview)
        self.menu_scrollable_frame = tk.Frame(self.menu_canvas, bg="white")

        self.menu_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))
        )
        self.menu_canvas.create_window((0, 0), window=self.menu_scrollable_frame, anchor="nw")
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)

        self.menu_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # Правая панель: Корзина
        cart_frame = tk.Frame(main_frame, width=280, bg="#f8f9fa", bd=1, relief="solid", padx=10, pady=10)
        cart_frame.pack(side="right", fill="y", padx=(15, 0))

        tk.Label(cart_frame, text="Ваш заказ 🛒", font=("Helvetica", 13, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        self.cart_text = tk.Text(cart_frame, width=28, height=18, font=("Helvetica", 10), state="disabled", bg="#ffffff", relief="flat")
        self.cart_text.pack(fill="both", expand=True, pady=(0, 10))

        self.total_label = tk.Label(cart_frame, text="Итого: 0 ₽", font=("Helvetica", 13, "bold"), bg="#f8f9fa", fg="#c0392b")
        self.total_label.pack(anchor="w", pady=(0, 10))

        # Панель кнопок управления заказом
        btn_frame = tk.Frame(cart_frame, bg="#f8f9fa")
        btn_frame.pack(fill="x")

        # ИСПРАВЛЕНО: Вместо padding=8 используем padx=8, pady=4 в tk.Button
        clear_btn = tk.Button(btn_frame, text="Очистить", font=("Helvetica", 10), bg="#e63946", fg="white", bd=0, padx=8, pady=4, command=self.clear_cart)
        clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        order_btn = tk.Button(btn_frame, text="Заказать", font=("Helvetica", 10, "bold"), bg="#27ae60", fg="white", bd=0, padx=8, pady=4, command=self.checkout)
        order_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Показываем первую категорию при запуске
        self.show_category(list(ITALIAN_MENU.keys())[0])

    def show_category(self, category_name):
        # Очищаем окно блюд
        for widget in self.menu_scrollable_frame.winfo_children():
            widget.destroy()

        # Заголовок категории
        tk.Label(self.menu_scrollable_frame, text=category_name, font=("Georgia", 16, "bold"), bg="white", fg="#27ae60").pack(anchor="w", padx=10, pady=10)

        # Вывод блюд
        for item in ITALIAN_MENU[category_name]:
            item_frame = tk.Frame(self.menu_scrollable_frame, bg="white")
            item_frame.pack(fill="x", padx=10, pady=8)

            # Текстовое описание блюда
            info_frame = tk.Frame(item_frame, bg="white")
            info_frame.pack(side="left", fill="x", expand=True)

            tk.Label(info_frame, text=item["name"], font=("Helvetica", 11, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
            tk.Label(info_frame, text=item["description"], font=("Helvetica", 9), fg="#7f8c8d", bg="white", wraplength=400, justify="left").pack(anchor="w")
            tk.Label(info_frame, text=f"{item['price']} ₽", font=("Helvetica", 11, "bold"), fg="#d35400", bg="white").pack(anchor="w", pady=(2, 0))

            # Кнопка добавления
            add_btn = ttk.Button(item_frame, text="Добавить +", style="Menu.TButton",
                                 command=lambda i=item: self.add_to_cart(i))
            add_btn.pack(side="right", padx=10, pady=5)
            
            # Разделительная линия
            divider = tk.Frame(self.menu_scrollable_frame, height=1, bg="#ecf0f1")
            divider.pack(fill="x", padx=10, pady=5)

    def add_to_cart(self, item):
        name = item["name"]
        price = item["price"]
        
        if name in self.cart:
            self.cart[name]["quantity"] += 1
        else:
            self.cart[name] = {"price": price, "quantity": 1}
            
        self.update_cart_display()

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_text.config(state="normal")
        self.cart_text.delete("1.0", tk.END)
        
        total_price = 0
        for name, info in self.cart.items():
            item_total = info["price"] * info["quantity"]
            total_price += item_total
            self.cart_text.insert(tk.END, f"{name}\n{info['quantity']} шт. x {info['price']} ₽ = {item_total} ₽\n")
            self.cart_text.insert(tk.END, "-"*22 + "\n")
            
        self.cart_text.config(state="disabled")
        self.total_label.config(text=f"Итого: {total_price} ₽")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Корзина пуста", "Пожалуйста, добавьте хотя бы одно блюдо в заказ.")
            return
            
        order_details = ""
        total_price = 0
        for name, info in self.cart.items():
            item_total = info["price"] * info["quantity"]
            total_price += item_total
            order_details += f"• {name} ({info['quantity']} шт.) — {item_total} ₽\n"
            
        messagebox.showinfo("Заказ отправлен!", f"Ваш заказ отправлен на кухню:\n\n{order_details}\nИтого к оплате: {total_price} ₽\n\nПриятного аппетита! 🍽️")
        self.clear_cart()

if __name__ == "__main__":
    root = tk.Tk()
    app = ItalianMenuApp(root)
    root.mainloop()
