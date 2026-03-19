from breezypythongui import EasyFrame

class LoginScreen(EasyFrame):
    def __init__(self):
        """Sets up the window and login widgets."""
        EasyFrame.__init__(self, title="System Login", width=300, height=150)

        # 1. Username Area
        self.addLabel(text="Username:", row=0, column=0)
        self.usernameField = self.addTextField(text="", row=0, column=1)

        # 2. Password Area
        self.addLabel(text="Password:", row=1, column=0)
        self.passwordField = self.addTextField(text="", row=1, column=1)
        
        # Mask the text in the password field for security
        self.passwordField["show"] = "*"

        # 3. Login Button
        self.addButton(text="Login", row=2, column=0, columnspan=2, command=self.login)

    def login(self):
        """Validates the inputs and checks credentials."""
        # Grab the text from the input fields
        username = self.usernameField.getText()
        password = self.passwordField.getText()
        
        # Check if either field is completely empty
        if username == "" or password == "":
            self.messageBox(title="Input Error", message="Username and password cannot be empty.")
            return # Stop the function here so it doesn't check credentials
            
        # Check if the credentials match our hardcoded "correct" values
        if username == "admin" and password == "secret":
            self.messageBox(title="Success", message="Login Successful!")
        else:
            self.messageBox(title="Login Failed", message="Invalid username or password.")

def main():
    """Instantiates and runs the GUI."""
    LoginScreen().mainloop()

if __name__ == "__main__":
    main()