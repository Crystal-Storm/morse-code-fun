import time

from pynput import keyboard

SKILL_LEVEL_PUSH = {'m':(.1,.3)}
SKILL_LEVEL_WAIT = {'m':(.1,.3)}
CONVERSION_TABLE = {'.-':'a','-...':'b', '-.-.':'c', '-..':'d', '.':'e', '..-.':'f', '--.':'g', '....':'h', '..':'i', '.---':'j', '-.-':'k', '.-..':'l', '---':'o', '.--.':'p', '--.-':'q', '.-.':'r', '...':'s', '-':'t', '..-':'u', '...-':'v', '.--':'w', '-..-':'x', '-.--':'y', '--..':'z'}

def get_user_input():
    global last_time,all_times
    last_time = time.time()
    all_times = []
    with keyboard.Listener(
            on_press = add_time,
            on_release = add_time) as listener:
        listener.join()
    return all_times

def add_time(key):
    if key == keyboard.Key.space:
        global last_time
        new_time = time.time()
        d_t = new_time-last_time
        last_time = new_time
        all_times.append(d_t)
    elif key == keyboard.Key.esc:
        # Stop listener
        return False

def translate_times(times,bounds):
    return_string = ""
    short,long = bounds
    for a_time in times:
        divider = (long+short)/2
        if a_time>divider:
            return_string += '-'
            long = (long*3+a_time)/4
        else:
            return_string += '.'
            short = (short*3+a_time)/4
    return return_string

def add_spaces(push_string,wait_string):
    return_list = []
    offset = 0
    for spacers in wait_string.split("-"):
        size = len(spacers)+1
        return_list.append(push_string[offset:offset+size])
        offset += size
    return return_list

def write_data(filename,data):
    with open(filename,'w') as file:
        writing_data=[str(x) for x in data]
        file.write('\n'.join(writing_data))

def read_data(filename,type):
    with open(filename,'r') as file:
        string=file.read()
    return [type(x) for x in string.split('\n')]

def to_string(morse_letter_list):
    return_string = ""
    for letter in morse_letter_list:
        return_string += CONVERSION_TABLE[letter]
    return return_string

def times_to_morse_string(all_times):
    all_pushes = all_times[1::2]
    all_waits = all_times[2::2]
    push_string = translate_times(all_pushes,SKILL_LEVEL_PUSH['m'])
    wait_string = translate_times(all_waits,SKILL_LEVEL_WAIT['m'])
    morse_string = add_spaces(push_string,wait_string)
    return morse_string

def main():
    # times = get_user_input()
    times = read_data("hello.txt",float)

    final_result = times_to_morse_string(times)

    print(final_result)

    letters = to_string(final_result)

    print(letters)

if __name__ == "__main__":
    main()