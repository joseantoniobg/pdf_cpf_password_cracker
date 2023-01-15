import PyPDF3
# import pikepdf
import fitz

"""
  Por questões de performance, foram testadas 3 bibliotecas para realizar a decodificacao do PDF:
  - PyPDF3
  - pikepdf
  - MyMuPDF

  As duas primeiras tiveram desempenho similar, demorando cerca de 3 minutos num teste controlado
  Já a MyMuPDF demorou menos de 1 minuto e meio no mesmo teste, então ela foi mantida por ser mais performática
"""

### MyMuPDF ###
###############
def run(pwd, pdf):
  with open(pdf, 'r+') as doc1:
    doc = fitz.Document(doc1)
    if doc.authenticate(pwd):
      log_file = open('found_password_' + pwd + '.txt', 'w')
      log_file.write("Found pwd of " + pwd)
      log_file.close()
      print('Found password: ' + pwd)
      exit()

### Pikepdf ###
###############
"""def run(pwd, pdf):
  try:
    with pikepdf.open(pdf, password = pwd):
      log_file = open('found_password_' + pwd + '.txt', 'w')
      log_file.write("Found pwd of " + pwd)
      log_file.close()
      exit()
  except pikepdf._qpdf.PasswordError as e:
    print(pwd)"""

### PyPDF3 ###
##############
"""def run(pwd, pdf):
    decrypt_result = pdf.decrypt(pwd)
    print(pwd)
    if decrypt_result > 0:
      log_file = open('found_password_' + pwd + '.txt', 'w')
      log_file.write("Found pwd of " + pwd)
      log_file.close()
      print(pwd +  ' : ' + str(decrypt_result))
      exit()
    try:
        with pikepdf.open("IOT.pdf", password = pwd) as p:
          log_file = open('found_password_' + pwd + '.txt', 'w')
          log_file.write("Found pwd of " + pwd)
          log_file.close()
          print(pwd +  ' : ' + str(decrypt_result))
          exit()
    except pikepdf._qpdf.PasswordError as e:
      print(pwd)"""