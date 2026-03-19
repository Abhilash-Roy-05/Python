from breezypythongui import EasyFrame

class CalculatorGUI(EasyFrame):
    def __init__(self):
        """Sets up the calculator window and widgets."""
        EasyFrame.__init__(self, title="Basic Calculator", width=350, height=200)

        # 1. Input Fields (IntegerFields)
        self.addLabel(text="First Number:", row=0, column=0)
        self.input1 = self.addIntegerField(value=0, row=0, column=1)

        self.addLabel(text="Second Number:", row=1, column=0)
        self.input2 = self.addIntegerField(value=0, row=1, column=1)

        # 2. Output Field (FloatField, read-only to prevent user typing)
        self.addLabel(text="Result:", row=2, column=0)
        self.resultField = self.addFloatField(value=0.0, row=2, column=1, state="readonly")

        # 3. Operation Buttons (arranged in a 2x2 grid)
        self.addButton(text="Add", row=3, column=0, command=self.add_nums)
        self.addButton(text="Subtract", row=3, column=1, command=self.subtract_nums)
        self.addButton(text="Multiply", row=4, column=0, command=self.multiply_nums)
        self.addButton(text="Divide", row=4, column=1, command=self.divide_nums)

    # --- Operation Methods ---
    
    def add_nums(self):
        """Adds the two numbers."""
        val1, val2 = self.get_inputs()
        self.resultField.setNumber(val1 + val2)

    def subtract_nums(self):
        """Subtracts the second number from the first."""
        val1, val2 = self.get_inputs()
        self.resultField.setNumber(val1 - val2)

    def multiply_nums(self):
        """Multiplies the two numbers."""
        val1, val2 = self.get_inputs()
        self.resultField.setNumber(val1 * val2)

    def divide_nums(self):
        """Divides the first number by the second, handling divide-by-zero."""
        val1, val2 = self.get_inputs()
        try:
            # Attempt the division
            result = val1 / val2
            self.resultField.setNumber(result)
        except ZeroDivisionError:
            # Catch the error if val2 is 0 and show a pop-up
            self.messageBox(title="Math Error", message="Cannot divide by zero!")
            self.resultField.setNumber(0.0)

    # --- Helper Method ---

    def get_inputs(self):
        """Helper function to retrieve values from the IntegerFields."""
        # Note: In a production app, you might want to wrap these in a try/except 
        # for ValueError in case the user leaves the field entirely blank.
        val1 = self.input1.getNumber()
        val2 = self.input2.getNumber()
        return val1, val2

def main():
    """Instantiates and runs the GUI."""
    CalculatorGUI().mainloop()

if __name__ == "__main__":
    main()