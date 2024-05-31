# view.py
#A visão é a interface gráfica do programa. Ela é responsável por apresentar os dados ao usuário e por interagir com o usuário.
from tkinterdnd2 import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from data_infos import *
from pattern_infos import *

try:
    from tkinter import *
except ImportError:
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText


class Visao:
    def __init__(self, root):
        self.root = root
        self.data_infos_frame = data_infos()
        self.pattern_infos_frame = pattern_infos()
        self.generate_rules = False
        self.has_content = False
        self.root.title("Pattern Finder")
    
    def ask_for_data_infos(self):
        """Return a frame to collect the data information inputs.
        """
        if has_content:
            self.data_infos_frame.generate_data_frame()
        else:
            msg = 'You need to add a valid file path'
            showinfo(title='Error_invalid_path',message=msg)

    def ask_for_pattern_infos(self):
        """Return a frame to collect the pattern information inputs. 
        """
        if has_content:
            self.pattern_infos_frame.generate_rules_frame()
        else:
            msg = 'You need to add a valid file path'
            showinfo(title='Error_invalid_path',message=msg)

    def update_screen(self):
        Label(self.self.self.root, text='Welcome to Pattern Finder!').grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        Label(self.self.self.root, text='To start, drag and drop a file path here:').grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        buttonbox_set_data_info = Frame(self.self.self.root)
        buttonbox_set_data_info.grid(row=5, column=0, pady=5)
        Button(buttonbox_set_data_info, text='Select data columns', command=self.ask_for_data_infos).pack(padx=5)


        buttonbox_set_pattern_info = Frame(self.self.self.root)
        buttonbox_set_pattern_info.grid(row=5, column=1, pady=5)
        Button(buttonbox_set_pattern_info, text='Configure pattern restrictions', command=self.ask_for_pattern_infos).pack(padx=5)


        buttonbox_generate_rules = Frame(self.self.self.root)
        buttonbox_generate_rules.grid(row=6, column=0, columnspan=2 ,pady=2)
        Button(buttonbox_generate_rules, text='Generate Rules!', command=self.generate_rules).pack()

        #############################################################################
        ##                                                                         ##     
        #                     drag & drop files interface                           #
        ##                                                                         ##
        #############################################################################
        listbox = Listbox(self.self.self.root, name='dnd_demo_listbox',
                            selectmode='browse', width=1, height=5)
        listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='new')

        # link a scrollbar to a list
        scrollbar = ttk.Scrollbar(
            self.self.self.root,
            orient=VERTICAL,
            command=listbox.yview
        )

        listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=2, column=2, padx=5, pady=5, sticky='new')

        ################################LISTBOX FOR THE RULES FOUND####################################
        rules_found = Listbox(self.self.self.root, name='rules_listbox',
                            selectmode='browse', width=1, height=15)
        rules_found.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='sew')

        # link a scrollbar to a list
        scrollbar_rules = ttk.Scrollbar(
            self.self.self.root,
            orient=VERTICAL,
            command=listbox.yview
        )

        rules_found['yscrollcommand'] = scrollbar_rules.set
        scrollbar_rules.grid(row=3, column=2, padx=5, pady=5, sticky='sew')

        ################################LISTBOX FOR deeper investigation####################################
        elements_found = Listbox(self.self.self.root, name='elements_listbox',
                            selectmode='browse', width=1, height=5)
        elements_found.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='sew')

        # link a scrollbar to a list
        scrollbar_ant = ttk.Scrollbar(
            self.self.self.root,
            orient=VERTICAL,
            command=listbox.yview
        )

        elements_found['yscrollcommand'] = scrollbar_ant.set
        scrollbar_ant.grid(row=4, column=2, padx=5, pady=5, sticky='sew')



        
    def drop_enter(event):
        event.widget.focus_force()
        return event.action

    def drop_position(event):
        return event.action

    def drop_leave(event):
        return event.action

    def drop(event):
        if event.data:
            print('Dropped data:\n', event.data)
            if event.widget == listbox:
                files = listbox.tk.splitlist(event.data)
                for f in files:
                    if os.path.exists(f):
                        print('Dropped file: "%s"' % f)
                        listbox.insert('end', f)
        return event.action

    # define drag callbacks
    def drag_init_listbox(event):
        # use a tuple as file list, this should hopefully be handled gracefully
        # by tkdnd and the drop targets like file managers or text editors
        data_path = ()
        if listbox.curselection():
            data_path = tuple([listbox.get(i) for i in listbox.curselection()])
            print('Dragging :', data_path)
        # tuples can also be used to specify possible alternatives for
        # action type and DnD type:
        return ((ASK, COPY), (DND_FILES, DND_TEXT), data_path)

    def onselect(event):
        global apriori_raw_data
        global has_content
        # Note here that Tkinter passes an event object to onselect()
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            value = event.widget.get(index)
            if value:
                print('You selected item %d: "%s"' % (index, value))
                try:
                    apriori_raw_data = pd.read_excel(value)
                    has_content = True
                except:
                    try:
                        apriori_raw_data = pd.read_csv(value)
                        has_content = True
                    except FileNotFoundError as error:
                        print(error)
        # now make the Listbox and Text drop targets
        listbox.drop_target_register(DND_FILES)

        listbox.dnd_bind('<<DropEnter>>', drop_enter)
        listbox.dnd_bind('<<DropPosition>>', drop_position)
        listbox.dnd_bind('<<DropLeave>>', drop_leave)
        listbox.dnd_bind('<<Drop>>', drop)
        listbox.dnd_bind('<<ListboxSelect>>', onselect)
        rules_found.dnd_bind('<<ListboxSelect>>', rule_deep_analysis)
        elements_found.dnd_bind('<<ListboxSelect>>', element_deep_analysis)


        listbox.drag_source_register(1, DND_FILES)

        listbox.dnd_bind('<<DragInitCmd>>', drag_init_listbox)


        self.root.update_idletasks()
        self.root.deiconify()
        self.root.mainloop()

        
    def atualizar_dados(self, dados):
        self.caixa_processos.delete(1.0, tk.END)
        self.caixa_processos.insert(tk.END, dados)
