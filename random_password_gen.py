import random
import string

#password requirements
num_char_min = 10
num_char_max = 16
num_low_case = 2
num_up_case = 2
num_sp_char = 2
num_num = 2

low_case = list(string.ascii_lowercase)
up_case = list(string.ascii_uppercase)
num = [chr(i) for i in range(48,58)]
sp_char = [chr(i) for i in [33,35,36,37,38,63,64,94,126]]

#assign password length and number of each character type
pass_char = random.choice(range(num_char_min,num_char_max+1)) 
pass_num_low_case = random.choice(range(num_low_case,pass_char-num_up_case-num_sp_char-num_num+1))
pass_num_up_case = random.choice(range(num_up_case,pass_char-pass_num_low_case-num_sp_char-num_num+1))
pass_num_num = random.choice(range(num_num,pass_char-pass_num_low_case-pass_num_up_case-num_sp_char+1))
pass_num_sp_char = random.choice(range(num_sp_char,pass_char-pass_num_low_case-pass_num_up_case-pass_num_num+1))

pass_low_case = (random.choices(low_case,k = pass_num_low_case))
pass_up_case = (random.choices(up_case,k = pass_num_up_case))
pass_num = (random.choices(num,k = pass_num_num))
pass_sp_char = (random.choices(sp_char,k = pass_num_sp_char))

password = pass_low_case + pass_up_case + pass_num + pass_sp_char
random.shuffle(password)
password = ''.join(password)
print(password)