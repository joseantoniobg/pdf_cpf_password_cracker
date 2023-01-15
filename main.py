import sys
import break_password
import asyncio
from timing import *

"""
    Esse projeto é uma refatoração e adaptação a partir do projeto pdf_crack de Oath93
    https://github.com/oath93/pdf_crack
"""

### RECEBE O NOME DO ARQUIVO, QUE DEVE ESTAR NO MESMO DIRETORIO DO PROJETO ###
##############################################################################

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
pdf = break_password.PyPDF3.PdfFileReader(pdfFile)

if not pdf.isEncrypted:
    print("The selected pdf is not encrypted. No password needed.")
    sys.exit()

### ESCOLHE SE QUER TENTAR DA LISTA DE CPFS OU COM TODAS AS COMBINACOES POSSIVEIS ###
#####################################################################################

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

start = string_to_float(now())

### CASO TENHA ESCOLHIDO A OPCAO 2, VERIFICA A EXISTENCIA DO ARQUIVO COM OS CPFS ###
####################################################################################

if choice == 2:
    try:
        pwd_file = open('passwords','r')
        large_pwd = pwd_file.read()
        top_pwd = large_pwd.splitlines()
        pwd_file.close()
    except FileNotFoundError:
        print("There was no passwords file found!")

async def run_tasks(top_pwd):
    for passw in top_pwd:
       break_password.run(passw, file_name)

async def envelop_passwords():
    await run_tasks(top_pwd)
    exit()

### CASO TENHA ESCOLHIDO A OPCAO 2, TENTA ACHAR O CPF VALIDO NA LISTA, E EM SEGUIDA ENCERRA A APLICACAO ###
###########################################################################################################

if len(top_pwd) > 0:
    asyncio.run(envelop_passwords())

def validCpf(cpf):
    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    numbers.append(expected_digit)
    cpf = cpf + str(expected_digit)
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    return cpf + str(expected_digit)

### SE ESCOLHEU A OPCAO 1, VAI TENTAR COM TODAS AS COMBINACOES POSSIVEIS, O QUE PODE DEMORAR TEMPO CONSIDERAVEL ###
###################################################################################################################

async def all_cpf_combinations():
    i = 1
    while i <= 999999999:
        gen_pwd = validCpf(str(i).zfill(9))
        break_password.run(gen_pwd, file_name)
        i+=1
        if i % 10000 == 0:
            print('Tryed ' + str(i) + ' combinations = ' + now())

async def envelop():
    await all_cpf_combinations()

asyncio.run(envelop())