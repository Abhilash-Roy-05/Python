from breezypythongui import EasyFrame

class TempConverter(EasyFrame):
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title="Temperature Converter", width=300, height=150)

        # 1. Celsius Input Area
        self.addLabel(text="Celsius:", row=0, column=0)
        self.celsiusField = self.addTextField(text="", row=0, column=1)

        # 2. Fahrenheit Output Area (Read-only FloatField with precision 2)
        self.addLabel(text="Fahrenheit:", row=1, column=0)
        self.fahrenheitField = self.addFloatField(value=0.0, row=1, column=1, precision=2, state="readonly")

        # 3. Conversion Button
        self.addButton(text="Convert to Fahrenheit", row=2, column=0, columnspan=2, command=self.convert)

    def convert(self):
        """Converts the Celsius input to Fahrenheit or displays an error."""
        try:
            # Attempt to read the text and convert it to a float
            celsius = float(self.celsiusField.getText())
            
            # Apply the conversion formula
            fahrenheit = (celsius * 9 / 5) + 32
            
            # Display the result in the read-only FloatField
            self.fahrenheitField.setNumber(fahrenheit)
            
        except ValueError:
            # Handle the error if the user typed letters or symbols
            self.messageBox(title="Invalid Input", message="Please enter a valid numeric temperature.")

def main():
    """Instantiates and runs the GUI."""
    TempConverter().mainloop()

if __name__ == "__main__":
    main()