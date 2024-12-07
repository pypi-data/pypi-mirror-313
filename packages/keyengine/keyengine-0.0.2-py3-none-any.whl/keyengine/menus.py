from . import keydetection as kd

def menu(choices: list[str]):
    c = 0
    if c == -1: c = 6
    if c == 7: c = 0
    for option in choices:
        if choices[c] == option:
            print(f"{colorama.Style.BRIGHT}{option} <{colorama.Style.RESET_ALL}")
        else:
            print(option)
    while kd.current_key != 'enter':
        time.sleep(0.08)
        if kd.current_key != '':
            clear()
            if kd.current_key == 'up':
                c -= 1
            if kd.current_key == 'down':
                c += 1
            if c == -1: c = 6
            if c == 7: c = 0
            for option in choices:
                if choices[c] == option:
                    print(f"{colorama.Style.BRIGHT}{option} <{colorama.Style.RESET_ALL}")
                else:
                    print(option)

    return c