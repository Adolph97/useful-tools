import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                print(f"Cannot access file: {fp}")
    return total_size

def main(directory):
    folder_sizes = []
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            size = get_folder_size(folder_path)
            folder_sizes.append((folder_name, size))
    
    # Sort folders by size in descending order
    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    
    for folder_name, size in folder_sizes:
        print(f"{folder_name} ---> {size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    main(directory)
