def parse_response(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    title = None
    description = None
    prompt_list = []

    for line in lines:
        line = line.strip()
        if '/' in line and title is None:
            title, description = line.split('/', 1)
        elif line == '':
            continue
        else:
            prompt_list.append(line)

    return title, description, prompt_list
