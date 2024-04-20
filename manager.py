import os

extensions = {
    'png':'images',
    'jpg':'images',
    'jpeg':'images',
    'mp4':'video',
    'pdf':'document'
}

path = os.getcwd()

for root, dir, files in os.walk(path):
    for file in files:
        ext = os.path.splitext(file)[-1][1:]
        if ext in extensions:
            try:
                folder = os.path.join(path,extensions[ext])
                if not os.path.isdir(folder):
                    os.mkdir(folder)
                os.rename(os.path.join(path,file),os.path.join(folder,file))
            except:
                print(f"{file} has an unlisted extension")
