from tkinter import *
from tkinter.messagebox import showinfo

class pattern_infos:
    def __init__(self) -> None:
        self.min_rep = StringVar()
        self.confidence = StringVar()
        
        self.min_rep = None
        self.confidence = None
        self.period = {}
        self.ended = False

    def generate_rules_frame(self):
        msg = 'Confidence is a measure of the reliability or support for a given association rule. It is defined as the proportion of cases in which the association rule holds true, or in other words, the percentage of times that the items in the antecedent appear in the same transaction as the items in the consequent. For example, suppose we have a dataset of 1000 transactions, and the itemset {milk, bread} appears in 100 of those transactions. The itemset {milk} appears in 200 of those transactions. The confidence would be 100/200 = 0.5.'
        showinfo(title='Confiança',message=msg)

        def go_to_next_element(event):
            event.widget.tk_focusNext().focus()

        def confirm_rules_info():
            self.min_rep = support_entry.get()
            self.confidence = confidence_entry.get()
            self.period = {'days': days_entry.get(), 'hours': hours_entry.get(), 'minutes': minutes_entry.get()}
            rules_frame.destroy()
            if self.min_rep and self.confidence and self.period:
                self.ended = True
                msg = 'Information added'
                showinfo(title='Information',message=msg)

        rules_frame = Tk()

        rules_frame.grid_rowconfigure(1, weight=1, minsize=50)
        rules_frame.grid_rowconfigure(2, weight=1, minsize=50)
        rules_frame.grid_rowconfigure(3, weight=1, minsize=50)
        rules_frame.grid_rowconfigure(4, weight=1, minsize=50)
        rules_frame.grid_rowconfigure(5, weight=1, minsize=50)
        rules_frame.grid_rowconfigure(6, weight=1, minsize=50)
        rules_frame.grid_rowconfigure(7, weight=1, minsize=50)
        
        rules_frame.grid_columnconfigure(0, weight=1, minsize=300)
        rules_frame.grid_columnconfigure(1, weight=1, minsize=300)
        rules_frame.focus()
        # support
        support_label = Label(rules_frame, text="Número mínimo de repetições:")
        support_label.grid(row=1, column=0, padx=5, pady=1)

        support_entry = Entry(rules_frame, textvariable=self.min_rep)
        support_entry.grid(row=1, column=1, padx=5, pady=1)
        support_entry.insert(0, self.min_rep if self.min_rep else 0)

        # confidence
        confidence_label = Label(rules_frame, text="Confiança (0 ~ 1):")
        confidence_label.grid(row=2, column=0, padx=5, pady=1)

        confidence_entry = Entry(rules_frame, textvariable=self.confidence)
        confidence_entry.grid(row=2, column=1, padx=5, pady=1)
        confidence_entry.insert(0, self.confidence if self.confidence else 0)
        
        # period
        period_label = Label(rules_frame, text="Intervalo de tempo:")
        period_label.grid(row=3, column=0, padx=5, pady=1)

        # days
        days_label = Label(rules_frame, text="Dias:")
        days_label.grid(row=4, column=0, padx=5, pady=1)
        days_entry = Entry(rules_frame)
        days_entry.grid(row=4, column=1, padx=5, pady=1)
        days_entry.insert(0, self.period['days'] if self.period else 0)

        # hours
        hours_label = Label(rules_frame, text="Horas:")
        hours_label.grid(row=5, column=0, padx=5, pady=1)
        hours_entry = Entry(rules_frame)
        hours_entry.grid(row=5, column=1, padx=5, pady=1)
        hours_entry.insert(0, self.period['hours'] if self.period else 0)

        # minutes
        minutes_label = Label(rules_frame, text="Minutos:")
        minutes_label.grid(row=6, column=0, padx=5, pady=1)
        minutes_entry = Entry(rules_frame)
        minutes_entry.grid(row=6, column=1, padx=5, pady=1)
        minutes_entry.insert(0, self.period['minutes'] if self.period else 0)

        # confirm button
        confirm_button = Button(rules_frame, text="Confirmar", command=confirm_rules_info)
        confirm_button.grid(row=7, column=1, padx=5, pady=1)

        support_entry.bind('<Return>', go_to_next_element)
        confidence_entry.bind('<Return>', go_to_next_element)
        days_entry.bind('<Return>', go_to_next_element)
        hours_entry.bind('<Return>', go_to_next_element)
        minutes_entry.bind('<Return>', go_to_next_element)
    
    def reset(self):
        self.ended = False