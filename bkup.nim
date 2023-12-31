import os
import osproc
import strutils

proc openProgram(program: string, arguments: seq[string]) =
  let _ = execCmd(program & " " & join(arguments, " "))
   
proc main =
  # Abre o programa login.py
  openProgram("python", @["bakup.py"])

  # Espera um curto período para garantir que o programa login.py tenha iniciado
  # sleep(2000)

  # Abre o navegador Chrome no endereço http://127.0.0.1:5000/
  # let chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" # Substitua pelo caminho correto do executável do Chrome no seu sistema
  # let url = "http://127.0.0.1:5000/"
  # openProgram(chromePath, @[url])

when isMainModule:
  main()
