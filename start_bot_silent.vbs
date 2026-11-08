Set WScriptShell = CreateObject("WScript.Shell")
WScriptShell.CurrentDirectory = "d:\my project\telegram primum emoji bot"
WScriptShell.Run "pythonw main.py", 0, False
