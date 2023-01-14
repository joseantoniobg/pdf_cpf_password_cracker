import sys
import break_password
import asyncio

while True:
    try:
        file_name = input("Enter a file name located in the same directory.")
        if not file_name[-4:] == '.pdf':
            file_name = file_name + '.pdf'
        print("Do you want to try to crack " + file_name + '?')
        uinput = input("1 = yes 0 = no \n")
        if int(uinput) == 1:
            break
    except ValueError:
        print("Invalid Input. Try again.\n")

pdfFile = open(file_name, 'rb')
pdf = break_password.PyPDF2.PdfReader(pdfFile) #PyPDF2 imported in thread_pwd.py, not imported again

if not pdf.is_encrypted:
    print("The selected pdf is not encrypted. No password needed.")
    sys.exit()

while True:
    try:
        print("Choose what to add to check: ")
        print("1: All CPFs")
        print("2: Dictionary-based (CPF list)\n")
        choice = int(input("Enter an option: "))
    except NameError:
        print("You must enter a value!")
        continue
    except ValueError:
        print("Only input a number!")
        continue
    if choice != 1 and choice != 2:
        print("Enter a number in the menu.")
        continue
    break

top_pwd = []

if choice == 2:
    try:
        pwd_file = open('passwords','r')
        large_pwd = pwd_file.read()
        top_pwd = large_pwd.splitlines()
        pwd_file.close()
    except FileNotFoundError:
        print("There was no passwords file found!")

async def run_tasks(top_pwd):
    tasks = []
    print('Creating Tasks...')
    for passw in top_pwd:
        tasks.append(asyncio.create_task(break_password.run(passw, pdf)))
    print('All Tasks created, now it will run as soon as possible')
    await asyncio.wait(tasks)
    exit()

if len(top_pwd) > 0:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_tasks(top_pwd))

def validCpf(cpf):
    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    numbers.append(expected_digit)
    cpf = cpf + str(expected_digit)
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    return cpf + str(expected_digit)

async def all_cpf_combinations():
    tasks = []
    print('Creating Tasks...')
    for i in range(1, 999999999):
        gen_pwd = validCpf(str(i).zfill(9))
        tasks.append(asyncio.create_task(break_password.run(gen_pwd, pdf)))
        if i % 1000000 == 0:
            print('Created ' + str(i) + ' of 999999999 Tasks...')
    print('All Tasks created, now it will run as soon as possible')
    await asyncio.wait(tasks)
    exit()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(all_cpf_combinations())