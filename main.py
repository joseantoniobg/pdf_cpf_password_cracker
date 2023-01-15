import sys
import break_password
import asyncio
from timing import *
from cpf_helpers import generateCpfValidationDigits

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

if choice == 1:
    while True:
        try:
            initial_combination = int(input("Enter the initial combination. Example, if you want to start by 001000001, type 1000001"))
            if initial_combination < 1 or initial_combination > 999999999:
                print("Invalid input, try from 1 to 999999999")
                continue
            final_combination = int(input("Enter the initial combination. Example, if you want to and by 991000001, type 991000001"))
            if final_combination < initial_combination:
                print("Final Combination needs to be at least equal to initial combination")
                continue
            if final_combination < 1 or final_combination > 999999999:
                print("Invalid input, try from 1 to 999999999")
                continue
            break
        except NameError:
            print("You must enter a value!")
            continue
        except ValueError:
            print("Invalid Input. Try again.\n")

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

### SE ESCOLHEU A OPCAO 1, VAI TENTAR COM TODAS AS COMBINACOES POSSIVEIS, O QUE PODE DEMORAR TEMPO CONSIDERAVEL ###
###################################################################################################################

async def all_cpf_combinations():
    i = initial_combination
    while i <= final_combination:
        gen_pwd = generateCpfValidationDigits(str(i).zfill(9))
        break_password.run(gen_pwd, file_name)
        i+=1
        if i % 10000 == 0:
            print('Tryed ' + str(i) + ' combinations = ' + now())

async def envelop():
    await all_cpf_combinations()

asyncio.run(envelop())