# -*- coding: utf-8 -*-

import codecs

file_ler = codecs.open("../txt/cientista_clerico.txt", "r", 'utf-8')
file_grava = codecs.open("../aiml/fcn_cientista_clerico.aiml", "w", 'utf-8')        

# Cria o cabeçario do arquivo aiml
file_grava.writelines('''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="1.0"> \n\n''')

# le arquivo texto com dados 
for linha in file_ler:
    if len(linha) > 10:
        filtrada = linha.split("(")
        upCientista = filtrada[0].upper()
        descritivo = "("+filtrada[1]
        #
        file_grava.write("    <category>\n")
        file_grava.write("        <pattern>")
        file_grava.write("* "+upCientista.strip())
        file_grava.write("</pattern>\n")
        file_grava.write("        <template>\n") 
        file_grava.write("            "+descritivo.rstrip()+"\n")
        file_grava.write("        </template>\n")
        file_grava.write("    </category>\n\n")

# fim do arquivo aiml
file_grava.writelines('''</aiml>''')

file_ler.close()
file_grava.close()




