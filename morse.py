import time

from pynput import keyboard

SKILL_LEVEL_PUSH={'m':(.1,.3)}
SKILL_LEVEL_WAIT={'m':(.1,.5)}
CONVERSION_TABLE={'.-':'a','-...':'b', '-.-.':'c', '-..':'d', '.':'e', '..-.':'f', '--.':'g', '....':'h', '..':'i', '.---':'j', '-.-':'k', '.-..':'l', '---':'o', '.--.':'p', '--.-':'q', '.-.':'r', '...':'s', '-':'t', '..-':'u', '...-':'v', '.--':'w', '-..-':'x', '-.--':'y', '--..':'z'}

def on_release(key):
    if key==keyboard.Key.space:
        add_time()
    elif key == keyboard.Key.esc:
        # Stop listener
        return False

def get_user_input():
    with keyboard.Listener(
            on_press=on_release,
            on_release=on_release) as listener:
        listener.join()
    all_pushes=all_times[1::2]
    all_waits=all_times[2::2]
    return all_pushes,all_waits

def add_time():
    global last_time
    new_time=time.time()
    d_t=new_time-last_time
    last_time=new_time
    all_times.append(d_t)

def translate_times(times,bounds):
    return_string=""
    short,long=bounds
    for a_time in times:
        divider=(long+short)/2
        if a_time>divider:
            return_string+='-'
            long=(long*3+a_time)/4
        else:
            return_string+='.'
            short=(short*3+a_time)/4
    return return_string

def add_spaces(push_string,wait_string):
    return_list=[]
    offset=0
    for spacers in wait_string.split("-"):
        size=len(spacers)+1
        return_list.append(push_string[offset:offset+size])
        offset+=size
    return return_list

def testing_data(filename=None):
    a=[0.07637715339660645, 0.07677507400512695, 0.07373428344726562, 0.11157822608947754, 0.07674241065979004, 0.07574653625488281, 0.41417884826660156, 0.11369895935058594, 0.07774066925048828, 0.07730817794799805, 0.3753635883331299, 0.11162710189819336, 0.11475610733032227, 0.3768496513366699, 0.37727952003479004, 0.3405294418334961]
    b=[0.09169340133666992, 0.09370136260986328, 0.1146693229675293, 0.6291744709014893, 0.9479961395263672, 0.1066441535949707, 0.17540597915649414, 0.06577539443969727, 0.5222854614257812, 0.11561298370361328, 0.1534864902496338, 0.07375001907348633, 0.7855353355407715, 0.06804227828979492, 0.07477712631225586]
    return a,b

def to_string(morse_letter_list):
    return_string=""
    for letter in morse_letter_list:
        return_string+=CONVERSION_TABLE[letter]
    return return_string

def main():
    # all_pushes,all_waits=get_user_input()
    all_pushes,all_waits=testing_data()
    
    # print(all_pushes)
    push_string=translate_times(all_pushes,SKILL_LEVEL_PUSH['m'])
    # print(push_string)
    # print(all_waits)
    wait_string=translate_times(all_waits,SKILL_LEVEL_WAIT['m'])
    # print(wait_string)

    final_result=add_spaces(push_string,wait_string)
    print(final_result)
    letters=to_string(final_result)
    print(letters)

if __name__=="__main__":
    last_time=time.time()
    all_times=[]
    main()