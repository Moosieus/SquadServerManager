from server_config import admin_file


def parse_admins():
    content_return = []
    with open(admin_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.split('#', 1)[0].strip(' ')
            try:
                int(line)
                content_return.append(
                    line
                )
            except ValueError:
                pass
    return content_return


def append_admin(user_id, comment=''):
    if len(user_id) != 18:
        raise Exception(f'Given channel ID is not the proper length! ({len(user_id)} != 18)')
    try:
        int(user_id)
    except ValueError:
        raise Exception("Given channel ID contains non-numeric characters!")
    with open(admin_file, 'r', encoding='utf-8') as file:
        contents = file.read()
    contents += f'\n{user_id} # {comment}'
    with open(admin_file, 'w', encoding='utf-8') as file:
        file.write(contents)


def remove_admin(user_id):
    if len(user_id) != 18:
        raise Exception(f'Given channel ID is not the proper length! {len(user_id)} != 18')
    try:
        int(user_id)
    except ValueError:
        raise Exception("Given channel ID contains non-numeric characters!")
    with open(admin_file, 'r', encoding='utf-8') as file:
        contents = file.readlines()
        for i in range(0, len(contents)):
            if user_id in contents[i]:
                contents.pop(i)
                break
    with open(admin_file, 'w', encoding='utf-8') as file:
        for line in contents:
            file.write(line)
