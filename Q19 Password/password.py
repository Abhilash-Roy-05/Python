from breezypythongui import EasyFrame
import string

class PasswordStrengthGUI(EasyFrame):
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title="Password Strength Checker", width=350, height=150)

        # 1. Password Input Area
        self.addLabel(text="Enter Password:", row=0, column=0)
        self.passwordField = self.addTextField(text="", row=0, column=1)

        # 2. Check Strength Button
        self.addButton(text="Check Strength", row=1, column=0, columnspan=2, command=self.check_strength)

        # 3. Output Area (Read-only TextField)
        self.addLabel(text="Strength:", row=2, column=0)
        self.resultField = self.addTextField(text="", row=2, column=1, state="readonly")

    def check_strength(self):
        """Evaluates the password and updates the result field."""
        password = self.passwordField.getText()
        
        # Handle empty input
        if password == "":
            self.messageBox(title="Input Error", message="Please enter a password to check.")
            return

        # --- Evaluate Conditions ---
        
        # 1. Check Length (True if 8 or more characters)
        is_long_enough = len(password) >= 8
        
        # 2. Check Digits (True if any character is a number)
        has_digit = any(char.isdigit() for char in password)
        
        # 3. Check Special Characters (True if any character is punctuation)
        has_special = any(char in string.punctuation for char in password)

        # --- Determine Strength Category ---
        
        if is_long_enough and has_digit and has_special:
            strength = "Strong"
        elif is_long_enough and (has_digit or has_special):
            strength = "Moderate"
        else:
            strength = "Weak"

        # Display the result
        self.resultField.setText(strength)

def main():
    """Instantiates and runs the GUI."""
    PasswordStrengthGUI().mainloop()

if __name__ == "__main__":
    main()