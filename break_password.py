import PyPDF2
import asyncio

async def run(pwd, pdf):
  if pwd == None:
      raise ValueError("No password to check")
  while True:
      try:
          decrypt_result = pdf.decrypt(pwd)
          break
      except PyPDF2.utils.PdfReadError:
          print("Pdf Decrypt PdfReadError Occured. Retrying.")
      except ValueError:
          print("Pdf Decrypt ValuError Occured. Retrying.")
  if decrypt_result > 0:
      log_file = open('found_password_' + pwd + '.txt', 'w')
      log_file.write("Found pwd of " + pwd)
      log_file.close()
      try:
          raise FoundPwd(pwd)
      except FoundPwd:
          import sys
          exc_info = sys.exc_info()
          if exc_info:
              return exc_info
  else:
    print(pwd +  ' : ' + str(decrypt_result))

class FoundPwd(Exception):
    def __init__(self, pwd):
        self.pwd = pwd