import PyPDF3

def run(pwd, pdf):
    decrypt_result = pdf.decrypt(pwd)
    print(pwd)
    if decrypt_result > 0:
      log_file = open('found_password_' + pwd + '.txt', 'w')
      log_file.write("Found pwd of " + pwd)
      log_file.close()
      print(pwd +  ' : ' + str(decrypt_result))
      exit()