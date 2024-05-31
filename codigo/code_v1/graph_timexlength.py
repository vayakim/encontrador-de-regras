import matplotlib.pyplot as plt
import time

# Function to measure time for a given dataset size for the bucket formation feature
def generate_graph_buckets_time_taken(file_path):
        # Read the file and extract dataset sizes and corresponding time taken
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extracting data from each line
    data = [line.strip().split() for line in lines]
    dataset_dict = {}

    # Grouping times by dataset size
    for size, time in data:
        size = int(size)
        time = float(time)
        if size not in dataset_dict:
            dataset_dict[size] = []
        dataset_dict[size].append(time)

    # Taking the average time for each dataset size
    dataset_sizes = []
    time_taken_values = []

    for key, values in dataset_dict.items():
        dataset_sizes.append(key)
        time_taken_values.append(sum(values) / len(values))

    print(dataset_sizes)
    print(time_taken_values)
    # Sort coordinates based on x-axis values
    sorted_coordinates = sorted(zip(dataset_sizes, time_taken_values), key=lambda x: x[0])
    x, y = zip(*sorted_coordinates)
    # Plotting the graph
    plt.figure(1)
    plt.plot(x, y, marker='o',linestyle='-',color='b')
    plt.title('Bucket formation computation time')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time Taken (seconds)')
    plt.grid(True)
    plt.show(block = False)

def generate_graph_filtering_time_taken(file_path):
        # Read the file and extract dataset sizes and corresponding time taken
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extracting data from each line
    data = [line.strip().split() for line in lines]
    dataset_dict = {}

    # Grouping times by dataset size
    for size, time in data:
        size = int(size)
        time = float(time)
        if size not in dataset_dict:
            dataset_dict[size] = []
        dataset_dict[size].append(time)

    # Taking the average time for each dataset size
    dataset_sizes = []
    time_taken_values = []

    for key, values in dataset_dict.items():
        dataset_sizes.append(key)
        time_taken_values.append(sum(values) / len(values))
    print(dataset_sizes)
    print(time_taken_values)
    # Sort coordinates based on x-axis values
    sorted_coordinates = sorted(zip(dataset_sizes, time_taken_values), key=lambda x: x[0])
    x, y = zip(*sorted_coordinates)
    # Plotting the graph
    plt.figure(2)
    plt.plot(x, y, marker='o',linestyle='-',color='b')
    plt.title('Filtering computation time')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time Taken (seconds)')
    plt.grid(True)
    plt.show(block = False)

def generate_graph_apriori_time_taken(file_path):
        # Read the file and extract dataset sizes and corresponding time taken
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extracting data from each line
    data = [line.strip().split() for line in lines]
    dataset_dict = {}

    # Grouping times by dataset size
    for size, time in data:
        size = int(size)
        time = float(time)
        if size not in dataset_dict:
            dataset_dict[size] = []
        dataset_dict[size].append(time)

    # Taking the average time for each dataset size
    dataset_sizes = []
    time_taken_values = []

    for key, values in dataset_dict.items():
        dataset_sizes.append(key)
        time_taken_values.append(sum(values) / len(values))

    # for size, times in dataset_dict.items():
    #     dataset_sizes.append(size)
    #     average_time = sum(times) / len(times)
    #     time_taken_values.append(average_time)
    print(dataset_sizes)
    print(time_taken_values)
   # Sort coordinates based on x-axis values
    sorted_coordinates = sorted(zip(dataset_sizes, time_taken_values), key=lambda x: x[0])
    x, y = zip(*sorted_coordinates)
    # Plotting the graph
    plt.figure(3)
    plt.plot(x, y, marker='o',linestyle='-',color='b')
    plt.title('Apriori computation time')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time Taken (seconds)')
    plt.grid(True)
    plt.show(block = False)

def generate_graph_original_data_analysis_time_taken(file_path):
        # Read the file and extract dataset sizes and corresponding time taken
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extracting data from each line
    data = [line.strip().split() for line in lines]
    dataset_dict = {}

    # Grouping times by dataset size
    for size, time in data:
        size = int(size)
        time = float(time)
        if size not in dataset_dict:
            dataset_dict[size] = []
        dataset_dict[size].append(time)

    # Taking the average time for each dataset size
    dataset_sizes = []
    time_taken_values = []

    for key, values in dataset_dict.items():
        dataset_sizes.append(key)
        time_taken_values.append(sum(values) / len(values))
    print(dataset_sizes)
    print(time_taken_values)
    # Sort coordinates based on x-axis values
    sorted_coordinates = sorted(zip(dataset_sizes, time_taken_values), key=lambda x: x[0])
    x, y = zip(*sorted_coordinates)
    # Plotting the graph
    plt.figure(4)
    plt.plot(x, y, marker='o',linestyle='-',color='b')
    plt.title('Original data analysis computation time')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time Taken (seconds)')
    plt.grid(True)
    plt.show(block = False)


#fazer o grafico do tempo de execucao do apriori vs quantidade de baldes
def generate_graph_buckets_quantity_vs_apriori_time_taken(file_path):
    # Read the file and extract dataset sizes and corresponding time taken
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extracting data from each line
    data = [line.strip().split() for line in lines]
    last_coord = data[-1]
    last_coord_x = int(last_coord[0])
    last_coord_y = float(last_coord[1])
    dataset_dict = {}

    # Grouping times by dataset size
    for size, time in data:
        size = int(size)
        time = float(time)
        if size not in dataset_dict:
            dataset_dict[size] = []
        dataset_dict[size].append(time)

    # Taking the average time for each dataset size
    dataset_sizes = []
    time_taken_values = []

    for key, values in dataset_dict.items():
        dataset_sizes.append(key)
        time_taken_values.append(sum(values) / len(values))
    print(dataset_sizes)
    print(time_taken_values)
    # Sort coordinates based on x-axis values
    sorted_coordinates = sorted(zip(dataset_sizes, time_taken_values), key=lambda x: x[0])
    x, y = zip(*sorted_coordinates)
    # Plotting the graph
    plt.figure(5)
    plt.plot(x, y, marker='o',linestyle='-',color='b')
    plt.scatter(last_coord_x, last_coord_y, marker='o', color='r', zorder=10)
    plt.title('Apriori computation time based on number of buckets')
    plt.xlabel('Number of buckets')
    plt.ylabel('Apriori Time Taken (seconds)')
    plt.grid(True)
    plt.show(block = False)


#fazer a media de quantos itens tem em cada balde e plotar em um grafico
#fazer o grafico do tempo de execucao do apriori vs quantidade de baldes
def generate_graph_average_number_of_items_per_bucket(file_path):
    # Read the file and extract dataset sizes and corresponding time taken
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extracting data from each line
    data = [line.strip().split() for line in lines]
    last_coord = data[-1]
    last_coord_x = int(last_coord[0])
    last_coord_y = float(last_coord[1])
    dataset_dict = {}

    # Grouping times by dataset size
    for number_of_buckets, average_number_of_items in data:
        print(average_number_of_items)
        number_of_buckets = int(number_of_buckets)
        average_number_of_items = float(average_number_of_items)
        if number_of_buckets not in dataset_dict:
            dataset_dict[number_of_buckets] = []
        dataset_dict[number_of_buckets].append(average_number_of_items)

    number_of_buckets_list = []
    average_number_of_items_list = []
    for key, value in dataset_dict.items():
        number_of_buckets_list.append(key)
        average_number_of_items_list.append(sum(value)/len(value))
    # Sort coordinates based on x-axis values
    sorted_coordinates = sorted(zip(number_of_buckets_list,average_number_of_items_list), key=lambda x: x[0])
    x, y = zip(*sorted_coordinates)
    # Plotting the graph
    plt.figure(6)
    plt.plot(x, y, marker='o',linestyle='-',color='b')
    plt.scatter(last_coord_x, last_coord_y, marker='o', color='r', zorder=10)
    plt.title('Average number of items per bucket vs number of buckets')
    plt.xlabel('Number of buckets')
    plt.ylabel('Average number of items per bucket')
    plt.grid(True)
    plt.show(block = False)

#arrumar encontrar o padrao no dataset original
