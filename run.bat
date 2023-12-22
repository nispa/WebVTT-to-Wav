@echo off
REM Controlla se Python è installato
python --version >nul 2>&1 || (
    echo Python non è installato.
    exit /b 1
)

REM Controlla se l'ambiente virtuale esiste
if not exist .\venv\\Scripts\\activate (
    echo L'ambiente virtuale non esiste.
    echo Creazione di un nuovo ambiente virtuale...
    python -m venv .\venv
)

REM Attiva l'ambiente virtuale
call .\venv\\Scripts\\activate

REM Installa le dipendenze
echo Installazione delle dipendenze...
pip install -r .\requirements.txt

REM Esegui lo script Python con i parametri passati al file batch
python main.py %*