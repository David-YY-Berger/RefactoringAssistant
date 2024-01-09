
#add place for param!!
def run_file(file_rel_path):
    print("running file " + file_rel_path)
    exec(open(file_rel_path).read())


def write_to_txt_file(path, content):
    with open(path, 'w') as file:
        file.write(content)



