from tkinter import *

# window settings
window = Tk()

window.title("Positioned Widgets")
window.geometry("400x200")
# window.maxsize(500, 300)
# window.minsize(300, 200)

# widgets
text_frame = Label(justify=CENTER, text='Hello this is Peter \n'
'I am the maker of this window.\n'
'It was made in TKinter.', height=5, width=50, relief=SUNKEN, bg='purple', fg='white')

button_frame = Label(justify=CENTER, height=5, width=50, bg='purple')

button1 = Button(button_frame, text='Launch', width=20, bg='red', fg='white', activeforeground='yellow',
activebackground='red')
button2 = Button(button_frame, text='Exit', width=20, bg='green', fg='white', activeforeground='yellow',
activebackground='green', command=quit)

text_frame.pack(expand=True)
button_frame.pack(expand=True)
button1.pack(pady=5, padx=10, side=LEFT)
button2.pack(pady=5, padx=10, side=LEFT)

# end of program
window.mainloop()
