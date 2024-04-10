from tkinter import *

def setup_entry(entry, placeholder):
        entry.insert(0, placeholder)
        entry.configure(fg='#ABB2B9')
        entry.bind("<FocusIn>", lambda event, entry=entry, placeholder=placeholder: entry_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event, entry=entry, placeholder=placeholder: entry_focus_out(event, entry, placeholder))

def entry_focus_in(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, 'end')
        entry.configure(fg='white')

def entry_focus_out(event, entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)
        entry.configure(fg='#ABB2B9')
