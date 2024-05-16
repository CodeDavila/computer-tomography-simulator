import tkinter as tk
from CTMachineApp import CTMachineApp

def main():
    # Create a Tkinter root window
    root = tk.Tk()
    # Create an instance of the CTMachineApp class, passing the root window as the master
    app = CTMachineApp(root)
    # Run the application
    app.run_app()

if __name__ == "__main__":
    # Call the main function when the script is executed
    main()
