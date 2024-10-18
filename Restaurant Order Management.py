import tkinter as tk
from tkinter import ttk, messagebox

class RestaurantManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management App")
        self.menuItems = {
            "French Fries":2,
            "Lunch Set":6,
            "Hamburger":3,
            "Pizza":4,
            "Cheese Burger":3.5,
            "Soda":1,
            "Drinks":2
        }
        self.exchangerate = 134
        self.setupbackground(root)
        frame = ttk.Frame(root)
        frame.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
        ttk.Label(frame, text = "Restaurant Order Management", font = ("Arial", 20, "bold")).grid(row = 0, columnspan = 3, padx = 10, pady = 10)
        self.menuLabels = {}
        self.menuQuantities = {}

        for i, (item, price) in enumerate(self.menuItems.items(), start = 1):
            label = ttk.Label(frame,text = f"{item}(${price}):", font = ("Arial", 12))
            label.grid(row = i, column = 0, padx = 10, pady = 5)
            self.menuLabels[item] = label
            QuantityEntry = ttk.Entry(frame, width = 5)
            QuantityEntry.grid(row = i, column = 1, padx = 10, pady = 5)
            self.menuQuantities[item] = QuantityEntry
        self.currencyVar = tk.StringVar()
        ttk.Label(frame, text = "Currency: ", font = ("Arial", 12)).grid(row = len(self.menuItems)+1, column = 0, padx = 10, pady = 5)

        currency_dropdown = ttk.Combobox(frame, textvariable=self.currencyVar, state="readonly", width=18, values=('USD', 'NPR'))
        currency_dropdown.grid(row=len(self.menuItems) + 1, column=1, padx=10, pady=5)
        
        currency_dropdown.current(0)
        self.currencyVar.trace('w', self.updateMenuPrices)
        OrderButton = ttk.Button(frame, text = "Place Order", command = self.placeOrder)
        OrderButton.grid(row = len(self.menuItems)+2, columnspan = 3, padx = 10, pady= 10)


    def setupbackground(self,root):
        bgWidth, bgHeight = 800, 600
        Canvas = tk.Canvas(root, width = bgWidth, height = bgHeight)
        Canvas.pack()
        OriginalImg = tk.PhotoImage(file = "background.png")
        BgImg = OriginalImg.subsample(OriginalImg.width()//bgWidth, OriginalImg.height()//bgHeight)
        Canvas.create_image(0, 0, anchor = tk.NW, image = BgImg)
        Canvas.image = BgImg

    def updateMenuPrices(self, *args):
        currency = self.currencyVar.get()
        symbol = "रु" if currency == "NPR" else "$"
        rate = self.exchangerate if currency == "NPR" else 1
        for item, label in self.menuLabels.items():
            price = self.menuItems[item]*rate
            label.config(text = f"{item} ({symbol}{price}):")
            
    def placeOrder(self):
        totalCost = 0
        orderSum = "Order Summary: \n"
        currency = self.currencyVar.get()
        symbol = "रु" if currency == "NPR" else "$"
        rate = self.exchangerate if currency == "NPR" else 1
        for item, entry in self.menuQuantities.items():
            quantity = entry.get()
            if quantity.isdigit():
                quantity = int(quantity)
                price = self.menuItems[item]*rate
                cost = quantity*price
                totalCost += cost
                if quantity > 0:
                    orderSum += f"{item}: {quantity} x {symbol}{price} = {symbol}{cost}\n"
        if totalCost > 0:
            orderSum += f"\n Total Cost = {symbol}{totalCost}"
            messagebox.showinfo("Order Placed", orderSum)
        else:
            messagebox.showerror("Error", "Please order atleast one item.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantManagement(root)
    root.geometry("800x600")
    root.mainloop()