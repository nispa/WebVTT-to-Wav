@echo off

REM Attiva l'ambiente virtuale
call .\venv\\Scripts\\activate

REM Esegui lo script Python con i parametri passati al file batch
python main.py %*