import language_tool_python
tool = language_tool_python.LanguageTool('en-US')


file = open('C:/[CESTA ZDE]/Extrahovane komentare - The Sun.txt', encoding="utf8")

with file as fp:
   line = fp.readline()
   cnt = 1
   while line:
       #print(line.strip())
       line = fp.readline()
       fixed = tool.correct(line.strip())
       print(fixed)
       cnt += 1