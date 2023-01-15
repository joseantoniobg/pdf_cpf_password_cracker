# pdf_cpf_password_cracker
Python PDF password Brute Force

This project is based on the project pdf_crack from Oath93
https://github.com/oath93/pdf_crack

CPF is a unique ID for any Brazilian Citizen. It's composed by 9 digits, in any combination, plus 2 validation digits.

Run main.py in the same directory as your .pdf to be opened.
This is for education only, and may not work on all .pdf files.

The password needs to be a number only valid CPF, which is used for docs and invoices in multiple brazilian services.

You can test all possible combinations or provide a file with a list of cpfs you want to test. Use the file 'passwords', each combination in a line.

Written in python 3.11
