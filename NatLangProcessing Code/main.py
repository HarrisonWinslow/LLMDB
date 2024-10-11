import DBHelper as db
import AIHelper as ai
import PopulateDB as pdb
import tkinter as tk

DEBUGGING = True
textBox = None
output_label = None

userInput = ""

# output_label.config(text=f"You entered: {user_input.strip()}")  # Update the output label

def on_submit():
    global userInput
    if textBox is None or output_label is None:
        createAndRunGUI()
        return

    userInput = textBox.get("1.0", tk.END)  # Get all text from the Text widget
    query = ai.askAI(userInput)
    result = db.runGetQuery(query)
    niceResponse = ai.getNiceResponse(result, userInput)
    output_label.config(text=f"{niceResponse.strip()}")  # Update the output label

def createAndRunGUI():
    global textBox, output_label
    # Create the main application window
    root = tk.Tk()
    root.title("Your Concert Ticket Database -- Now with AI!")

    # Set the initial size of the window (width x height)
    root.geometry("600x300")  # Width: 400 pixels, Height: 300 pixels

    # Create a label for instructions
    instruction_label = tk.Label(root, text="What would you like to know/do?")
    instruction_label.pack()

    # Create an entry widget for user input
    textBox = tk.Text(root, height=5, width=60)
    textBox.pack()

    # Create a submit button
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    # Create a label to display output
    output_label = tk.Label(root, text="", wraplength=580)
    output_label.pack()

    # Run the application
    root.mainloop()


def main():
    if DEBUGGING:
        print("Hi from main! You are in debugging mode! In order to run without extra text, run with DEBUGGING set to False!")

    ai.storeTableInfo()
    createAndRunGUI()

    # print(chr(sum(range(ord(min(str(not()))))))) #Don't do it! Don't uncomment this line! I'm warning you now! He's among us...

    ### TODO make a "BandPlaysConcert" table that connects bands to specific concerts. The table should just have concertId and bandId, really. Many to many.

if __name__ == '__main__':
    main()