from breezypythongui import EasyFrame

class DemoGUI(EasyFrame):
    def __init__(self):
        """Sets up the window and widgets."""
        # Initialize the main frame
        EasyFrame.__init__(self, title="GUI Demo Application", width=300, height=100)

        # 1. Create the Label (spans across 2 columns so it sits centered above the buttons)
        self.demoLabel = self.addLabel(text="Python GUI Demo", row=0, column=0, columnspan=2, sticky="NSEW")

        # 2. Create the Buttons
        self.clearBtn = self.addButton(text="Clear", row=1, column=0, command=self.clear_label)
        self.restoreBtn = self.addButton(text="Restore", row=1, column=1, command=self.restore_label)

        # Disable the Restore button initially since the text is already showing
        self.restoreBtn["state"] = "disabled"

    def clear_label(self):
        """Clears the label text and toggles button states."""
        self.demoLabel["text"] = ""
        self.clearBtn["state"] = "disabled"
        self.restoreBtn["state"] = "normal"

    def restore_label(self):
        """Restores the label text and toggles button states."""
        self.demoLabel["text"] = "Python GUI Demo"
        self.restoreBtn["state"] = "disabled"
        self.clearBtn["state"] = "normal"

def main():
    """Instantiates and runs the GUI."""
    DemoGUI().mainloop()

if __name__ == "__main__":
    main()