# -*- coding: utf-8 -*-
import os
import platform
import multiprocessing
import subprocess
import time
import numpy as np



from tkinterdnd2 import *
from tkinter import ttk
from tkinter.messagebox import showinfo

try:
    from tkinter import *
except ImportError:
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText

import pandas as pd

from data_infos import *
from pattern_infos import *
from format_data import *
from apriori_input_data import *
from graph_timexlength import *
import clusterizacao

from efficient_apriori import apriori
from fim import eclat, fpgrowth, arules
from fim import apriori as fim_apriori

# File path to store the time data
data_filtering_time_taken = "data_filtering_timexleng_coords.txt"
apriori_time_taken = "apriori_execution_timexleng_coords.txt"
bucket_formation_time_taken = "bucket_formation_timexleng_coords.txt"
original_data_analysis_time_taken = "original_data_analysis_timexleng_coords.txt"
number_of_buckets_vs_apriori_time_taken = "number_of_buckets_vs_apriori_time_taken.txt"
itens_per_bucket = "itens_per_bucket.txt"   
# Check if the file exists, and if it does, delete it
if os.path.exists(number_of_buckets_vs_apriori_time_taken):
    os.remove(number_of_buckets_vs_apriori_time_taken)
if os.path.exists(itens_per_bucket):
    os.remove(itens_per_bucket)


def ask_for_data_infos():
    """Return a frame to collect the data information inputs.
    """
    if has_content:
        data_infos_frame.generate_data_frame()
    else:
        msg = 'You need to add a valid file path'
        showinfo(title='Error_invalid_path',message=msg)

def ask_for_pattern_infos():
    """Return a frame to collect the pattern information inputs. 
    """
    if has_content:
        pattern_infos_frame.generate_rules_frame()
    else:
        msg = 'You need to add a valid file path'
        showinfo(title='Error_invalid_path',message=msg)
         
def generate_rules():
    """Generates the association rules based on the given dataset and parameters.
        First, there is a filtering either by the restrictions of the data or the restriction of the rules,
        then the data is set to be a proper input to the apriori algorithm, which retturns the rules.
    """
    global apriori_raw_data
    global all_rules

    rules_found.delete(0,END)
    if has_content:
        if data_infos_frame.ended and pattern_infos_frame.ended:

            dayfirst = data_infos_frame.dayfirst
            yearfirst = data_infos_frame.yearfirst
            metadata = data_infos_frame.metadata
            antecedente = data_infos_frame.antecedente
            consequente = data_infos_frame.consequente
            min_rep = float(pattern_infos_frame.min_rep)
            
            confidence = float(pattern_infos_frame.confidence)
            confidence_percentage = confidence*100
            period = pattern_infos_frame.period 
            #get the number of rows of the dataset
            number_of_cells = apriori_raw_data.size
            number_of_rows = len(apriori_raw_data.index)
            key = (min_rep, confidence_percentage, period)
 

            filter_time1 = time.time()
            filtered_data = format_data(apriori_raw_data)
            filtered_data.select_columns(metadata, antecedente, consequente, dayfirst, yearfirst)
            filtered_data.apply_restrictions(min_rep)
            apriori_input = apriori_input_data(filtered_data.formated_data)   
            # clusters = clusterizacao(filtered_data.formated_data)
            # clusters.kmeans()
            # clusters.show_clusters()
            filter_time2 = time.time()

            filter_time = filter_time2 - filter_time1
            with open(data_filtering_time_taken, "a") as f:
                f.write(str(number_of_cells) + " " + str(filter_time) + "\n")
            
            #generate_graph_filtering_time_taken(data_filtering_time_taken)

            bucket_formation_time1 = time.time()
            buckets = apriori_input.generate_buckets(period, metadata)
            bucket_formation_time2 = time.time()


            #average number of itens per bucket
            number_of_items = 0
            for bucket in buckets:
                number_of_items += len(bucket)
            
            average_number_of_items = number_of_items/len(buckets)
            
            with open(itens_per_bucket, "a") as f:
                f.write(str(len(buckets)) + " " + str(average_number_of_items) + "\n")

            bucket_formation_time = bucket_formation_time2 - bucket_formation_time1
            with open(bucket_formation_time_taken, "a") as f:
                f.write(str(number_of_rows) + " " + str(bucket_formation_time) + "\n")

  
            print(min_rep, confidence_percentage, period)
            start_borgelt_apriori_time = time.time()
            borgelt_rules = arules(buckets,supp=-int(min_rep), conf=confidence_percentage, report='ab', zmin=2)
            end_apriori_borgelt_time = time.time()
            borgelt_apriori_time = end_apriori_borgelt_time - start_borgelt_apriori_time
            with open(apriori_time_taken, "a") as f:
                f.write(str(number_of_rows) + " " + str(borgelt_apriori_time) + "\n")
            

            with open(number_of_buckets_vs_apriori_time_taken, "a") as f:
                f.write(str(len(buckets)) + " " + str(borgelt_apriori_time) + "\n")

            columns_names = ['Consequente', 'Antecedente', 'Frequência da regra', 'Frequência do antecedente']
            reordered_columns_names = ['Antecedente', 'Consequente', 'Frequência da regra', 'Frequência do antecedente']
            borgelt_rules_df = pd.DataFrame(borgelt_rules, columns=columns_names)
            borgelt_rules_df = borgelt_rules_df[reordered_columns_names]
            borgelt_rules_df = borgelt_rules_df.loc[borgelt_rules_df['Frequência da regra'] >= int(min_rep)]
            borgelt_rules_df.reset_index(inplace=True, drop=True)
            all_rules = borgelt_rules_df.copy()

            borgelt_rules_df.to_csv('outcome_rules.csv')

            # Função para verificar se um conjunto é subconjunto de outro
            def is_subset(a, b):
                return set(a).issubset(set(b))

            # Lista para armazenar os índices das linhas a serem removidas
            indices_remover = []

            # Iterar sobre cada linha
            for i, row in borgelt_rules_df.iterrows():
                antecedente_atual = row['Antecedente']
                consequente_atual = row['Consequente']
                
                # Verificar se existe outra linha com antecedente subconjunto e mesmo consequente
                for j, other_row in borgelt_rules_df.iterrows():
                    if i != j:  # Evitar comparação com a mesma linha
                        antecedente_outro = other_row['Antecedente']
                        consequente_outro = other_row['Consequente']
                        
                        if is_subset(antecedente_atual, antecedente_outro) and consequente_atual == consequente_outro:
                            # Além disso, verificar se as outras métricas são iguais ou menores
                            if other_row['Frequência da regra'] >= row['Frequência da regra'] and other_row['Frequência do antecedente'] >= row['Frequência do antecedente']:
                                indices_remover.append(i)
                            break  # Parar de procurar outras correspondências

            # Remover as linhas com os índices identificados
            rules_found_df = borgelt_rules_df.drop(indices_remover)
            rules_found_df.reset_index(inplace=True, drop=True)
          

            if rules_found_df.empty:
                print('Nenhuma regra encontrada!')
                print('Processamento concluído!')
                print('C Apriori execution time:', borgelt_apriori_time , 'seconds')
            else:
                for index, row in rules_found_df.iterrows():
                    rules_found.insert(index, f'Rule {index}: {row["Antecedente"]} -> {row["Consequente"]}')
            
                
        else:
            msg = 'Something went wrong! Please check the parameters'
            showinfo(title='Error_bad_parameters',message=msg)
    else:
        msg = 'You need to add a valid file path'
        showinfo(title='Error_invalid_path',message=msg)
  
    
def generate_analysis(rule_index):
    """Find the selected rule in the original dataset and generate a csv file with all the occurrences of the rule.
    Transactions within the rule will only be considered if they occur within the time interval defined by the user alongside the other transactions of the rule.

    Args:
        rule_index (int): the index of the rule to be analyzed
    """

    global all_rules
    pairs = []
    result_slice = []
    dayfirst = data_infos_frame.dayfirst
    yearfirst = data_infos_frame.yearfirst
    metadata = data_infos_frame.metadata
    antecedente = data_infos_frame.antecedente
    consequente = data_infos_frame.consequente
    period = pattern_infos_frame.period
    rule = all_rules.loc[rule_index]
    print(rule)

    fc = pd.Timedelta(days=float(period['days']), hours=float(period['hours']), minutes=float(period['minutes']))
    print('Processamento de padrões iniciado...\n')
    analise_tempo_i = time.time()

    for par in rule['Antecedente']:
        pairs.append(tuple(par))
    pairs.append(rule['Consequente'])

    
    unique_elements = []
    elements_found.delete(0, END)
    for par in pairs:
        for element in par:
            unique_elements.append(element)
    
    count = 0
    for element in set(unique_elements):
        elements_found.insert(count, element)
        count += 1


    aux = apriori_raw_data.copy()
    aux[metadata] = pd.to_datetime(aux[metadata], dayfirst=dayfirst, yearfirst=yearfirst, errors='coerce')
    aux.sort_values(by=metadata, inplace=True)
    aux.set_index(metadata, inplace=True)
    #aux é o dataset ordenado por data e indexado pela coluna de data

    #O METODO A SEGUIR SO FUNCIONA COM TRANSACOES DE 2 ELEMENTOS
    found = 1
    for index, row in aux.iterrows(): 
        found=1  #se found=0, significa que o par não foi encontrado no intervalo de tempo           
        if (row[antecedente], row[consequente]) in pairs:
            end = pd.to_datetime(index + fc)
            aux1 = aux.loc[index:end].copy() #aux1 é o dataset que contem todas as ações que ocorreram no intervalo de tempo
            for pair in pairs:
                if (pair[0] in aux1[antecedente].values) and (pair[1] in aux1[consequente].values):
                    found = 1
                else: 
                    found = 0
                    break
            if found:
                for index2, row2 in aux1.iterrows():
                    if (row2[antecedente], row2[consequente]) in pairs:
                        result_slice.append(row2)

    result = pd.DataFrame(result_slice)
    result = result.drop_duplicates()

    print(result)

    result.to_csv(f'rule{rule_index}.csv')
    print('Processamento concluído!')
    analise_tempo_f = time.time()
    print('Tempo de análise das regras nos dados originais:', round(analise_tempo_f - analise_tempo_i, 3), 'segundos')
    analysis_time_taken = analise_tempo_f - analise_tempo_i
    with open(original_data_analysis_time_taken, "a") as f:
        f.write(str(len(apriori_raw_data)) + " " + str(analysis_time_taken) + "\n")
    
    #generate_graph_original_data_analysis_time_taken(original_data_analysis_time_taken)

def investigate_elements(index):
    """Investigate individual elements of the rule, showing all the transactions in which they occur.

    Args:
        index (int): the index of the element to be investigated
    """
    metadata = data_infos_frame.metadata
    dayfirst = data_infos_frame.dayfirst
    yearfirst = data_infos_frame.yearfirst
    antecedente = data_infos_frame.antecedente
    metadata = data_infos_frame.metadata
    element = str(elements_found.get(index))

    aux = apriori_raw_data.copy()
    aux[metadata] = pd.to_datetime(aux[metadata], dayfirst=dayfirst, yearfirst=yearfirst, errors='coerce')
    aux.sort_values(by=metadata, inplace=True)
    element_actions = []
    for index, row in aux.iterrows():
        if str(row[antecedente]) == element:
            element_actions.append(row)
    
    element_actions = pd.DataFrame(element_actions).drop_duplicates()
    element_actions.to_csv(f'element{index}.csv')
    print(element_actions)



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

def rule_deep_analysis(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        value = event.widget.get(index)
        if value:
            print('You selected rule %d: "%s"' % (index, value))
            generate_analysis(index)

def element_deep_analysis(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        value = event.widget.get(index)
        if value:
            print('You selected antecedent %d: "%s"' % (index, value))
            investigate_elements(index)
    
    # else:
    #     msg = 'No rule selected!'
    #     showinfo(title='Error_no_rule_selected',message=msg)



root = TkinterDnD.Tk()
root.withdraw()
root.title('RULE_FINDER')
root.grid_rowconfigure(6, weight=1, minsize=100)
root.grid_columnconfigure(0, weight=1, minsize=300)
root.grid_columnconfigure(1, weight=1, minsize=300)

apriori_raw_data = pd.DataFrame()
apriori_input = pd.DataFrame()

data_infos_frame = data_infos()
pattern_infos_frame = pattern_infos()
all_rules = pd.DataFrame()
# rules_found_per_param = {}
has_content = False

Label(root, text='Welcome to Pattern Finder!').grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(root, text='To start, drag and drop a file path here:').grid(row=1, column=0, columnspan=2, padx=10, pady=5)

buttonbox_set_data_info = Frame(root)
buttonbox_set_data_info.grid(row=5, column=0, pady=5)
Button(buttonbox_set_data_info, text='Select data columns', command=ask_for_data_infos).pack(padx=5)


buttonbox_set_pattern_info = Frame(root)
buttonbox_set_pattern_info.grid(row=5, column=1, pady=5)
Button(buttonbox_set_pattern_info, text='Configure pattern restrictions', command=ask_for_pattern_infos).pack(padx=5)


buttonbox_generate_rules = Frame(root)
buttonbox_generate_rules.grid(row=6, column=0, columnspan=2 ,pady=2)
Button(buttonbox_generate_rules, text='Generate Rules!', command=generate_rules).pack()

#############################################################################
##                                                                         ##     
#                     drag & drop files interface                           #
##                                                                         ##
#############################################################################
listbox = Listbox(root, name='dnd_demo_listbox',
                    selectmode='browse', width=1, height=5)
listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='new')

# link a scrollbar to a list
scrollbar = ttk.Scrollbar(
    root,
    orient=VERTICAL,
    command=listbox.yview
)

listbox['yscrollcommand'] = scrollbar.set
scrollbar.grid(row=2, column=2, padx=5, pady=5, sticky='new')

################################LISTBOX FOR THE RULES FOUND####################################
rules_found = Listbox(root, name='rules_listbox',
                    selectmode='browse', width=1, height=15)
rules_found.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='sew')

# link a scrollbar to a list
scrollbar_rules = ttk.Scrollbar(
    root,
    orient=VERTICAL,
    command=listbox.yview
)

rules_found['yscrollcommand'] = scrollbar_rules.set
scrollbar_rules.grid(row=3, column=2, padx=5, pady=5, sticky='sew')

################################LISTBOX FOR deeper investigation####################################
elements_found = Listbox(root, name='elements_listbox',
                    selectmode='browse', width=1, height=5)
elements_found.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='sew')

# link a scrollbar to a list
scrollbar_ant = ttk.Scrollbar(
    root,
    orient=VERTICAL,
    command=listbox.yview
)

elements_found['yscrollcommand'] = scrollbar_ant.set
scrollbar_ant.grid(row=4, column=2, padx=5, pady=5, sticky='sew')



#listbox.insert(END, os.path.abspath(__file__))

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


root.update_idletasks()
root.deiconify()
root.mainloop()