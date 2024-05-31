from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk

class data_infos:
    def __init__(self):
        self.dayfirst = int()
        self.yearfirst = int()
        self.metadata = StringVar()
        self.antecedente = StringVar()
        self.consequente = StringVar()
        self.ended = False

    def generate_data_frame(self):
        """Basic tkinter usage to create a frame asking for information about the data inputs.
        """
        informations_frame = Tk()

        def go_to_next_element(event):
            event.widget.tk_focusNext().focus()

        def confirm_data_infos():
            if format_cb.current() == 0:
                self.dayfirst = 1
                self.yearfirst = 0
            else:
                self.dayfirst = 0
                self.yearfirst = 1
            self.metadata = metadata_entry.get()
            self.antecedente = antecedente_entry.get()
            self.consequente = consequente_entry.get()
            if self.metadata and self.antecedente and self.consequente:
                self.ended = True
                msg = f'Information added'
                showinfo(title='Information',message=msg)
                informations_frame.destroy()
                # bind the selected value changes

            

        informations_frame.grid_rowconfigure(1, weight=1, minsize=50)
        informations_frame.grid_rowconfigure(2, weight=1, minsize=50)
        informations_frame.grid_rowconfigure(3, weight=1, minsize=50)

        informations_frame.grid_columnconfigure(0, weight=1, minsize=300)
        informations_frame.grid_columnconfigure(1, weight=1, minsize=300)
        informations_frame.focus()
        # metadata
        metadata_label = Label(informations_frame, text="Metadata attribute (Unique):")
        metadata_label.grid(row=1, column=0, padx=5, pady=1)

        metadata_entry = Entry(informations_frame, textvariable=self.metadata)
        metadata_entry.grid(row=1, column=1, padx=5, pady=1)
        metadata_entry.focus()

        # target attributes
        #antecedente
        antecedente_label = Label(informations_frame, text="Atributo de origem:")
        antecedente_label.grid(row=2, column=0, padx=5, pady=1)

        antecedente_entry = Entry(informations_frame, textvariable=self.antecedente)
        antecedente_entry.grid(row=2, column=1, padx=5, pady=1)

        #consequente
        consequente_label = Label(informations_frame, text="Atributo de destino:")
        consequente_label.grid(row=3, column=0, padx=5, pady=1)

        consequente_entry = Entry(informations_frame, textvariable=self.consequente)
        consequente_entry.grid(row=3, column=1, padx=5, pady=1)


        # confirm button
        confirm_button = Button(informations_frame, text="Confirm", command=confirm_data_infos)
        confirm_button.grid(row=4, column=1, padx=5, pady=10)

        #dayfirst/yearfirst che
        # ckboxes
            # create a combobox

        format_cb = ttk.Combobox(informations_frame)

        # get first 3 letters of every month name
        format_cb['values'] = ['day first (dd/mm/yy)', 'year first (yy/mm/dd)']

        # prevent typing a value
        format_cb['state'] = 'readonly'
        format_cb.current(0)

        # place the widget
        format_cb.grid(row=4, column=0, padx=5, pady=10)

        metadata_entry.bind('<Return>', go_to_next_element)
        antecedente_entry.bind('<Return>', go_to_next_element)
        consequente_entry.bind('<Return>', go_to_next_element)
    
    def reset(self):
        self.dayfirst = int()
        self.yearfirst = int()
        self.metadata = StringVar()
        self.antecedente = StringVar()
        self.consequente = StringVar()
        self.ended = False


    