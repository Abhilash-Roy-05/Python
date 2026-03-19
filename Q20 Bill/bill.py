from breezypythongui import EasyFrame

class BillingGUI(EasyFrame):
    def __init__(self):
        """Sets up the window and billing widgets."""
        EasyFrame.__init__(self, title="Billing System", width=300, height=200)

        # 1. Price Input Area
        self.addLabel(text="Item Price ($):", row=0, column=0)
        self.priceField = self.addFloatField(value=0.0, row=0, column=1)

        # 2. Quantity Input Area
        self.addLabel(text="Quantity:", row=1, column=0)
        self.quantityField = self.addIntegerField(value=0, row=1, column=1)

        # 3. Generate Bill Button
        self.addButton(text="Generate Bill", row=2, column=0, columnspan=2, command=self.generate_bill)

        # 4. Final Amount Output Area (Read-only)
        self.addLabel(text="Final Amount ($):", row=3, column=0)
        self.amountField = self.addFloatField(value=0.0, row=3, column=1, precision=2, state="readonly")

    def generate_bill(self):
        """Calculates the total, applies discounts if needed, and updates the display."""
        # Retrieve the numbers from the input fields
        price = self.priceField.getNumber()
        quantity = self.quantityField.getNumber()
        
        # Calculate the initial total
        total = price * quantity
        
        # Apply the 10% discount rule
        if total > 1000:
            final_amount = total * 0.90  # 90% of the original price is a 10% discount
            self.messageBox(title="Discount Applied", message="A 10% discount has been applied!")
        else:
            final_amount = total
            
        # Display the formatted result
        self.amountField.setNumber(final_amount)

def main():
    """Instantiates and runs the GUI."""
    BillingGUI().mainloop()

if __name__ == "__main__":
    main()