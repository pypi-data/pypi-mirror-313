# 🤖 ws-bom-robot-app

A `FastAPI` application serving ws bom/robot/llm platform ai

## 🌵 Minimal app structure

```env
app/
|-- .env
|-- main.py
```

Fill `main.py` with the following code:

```python
from ws_bom_robot_app import main
app = main.app
```

FIll `.env` with the following code:

```env
#robot_env=local/development/production
robot_env=local
robot_user='[user]'
robot_password='[pwd]'
robot_data_folder='./.data'
robot_cms_auth='[auth]'
robot_cms_host='https://[DOMAIN]'
robot_cms_db_folder=llmVectorDb
robot_cms_files_folder=llmKbFile
```

## 🚀 Run the app

- development

  ```bash
  fastapi dev --port 6001
  #uvicorn --reload --host 0.0.0.0 --port 6001 main:app
  ```  

- production

  ```bash
  fastapi run --port 6001
  ```

- production with [multipler workers](https://fastapi.tiangolo.com/deployment/server-workers/#multiple-workers)

  ```bash
  fastapi run --port 6001 --workers 4
  ```

### 🔖 Windows requirements  

  #### libmagic (mandatory)

  ```bash
  py -m pip install --upgrade python-magic-bin
  ```
  
  #### tesseract-ocr (mandatory)

  [Install tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  [Last win-64 release](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)

  Add tesseract executable (C:\Program Files\Tesseract-OCR) to system PATH
  
  ```pwsh
  $pathToAdd = "C:\Program Files\Tesseract-OCR"; `
  $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine); `
  if ($currentPath -split ';' -notcontains $pathToAdd) { `
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$pathToAdd", [System.EnvironmentVariableTarget]::Machine) `
  }
  ```

  #### libreoffice (optional: for robot_env set to development/production)

  [Install libreoffice](https://www.libreoffice.org/download/download-libreoffice/)
  [Last win-64 release](https://download.documentfoundation.org/libreoffice/stable/24.8.2/win/x86_64/LibreOffice_24.8.2_Win_x86-64.msi)

  Add libreoffice executable (C:\Program Files\LibreOffice\program) to system PATH

  ```pwsh
  $pathToAdd = "C:\Program Files\LibreOffice\program"; `
  $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine); `
  if ($currentPath -split ';' -notcontains $pathToAdd) { `
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$pathToAdd", [System.EnvironmentVariableTarget]::Machine) `
  }
  ```

  #### poppler (optional: for robot_env set to development/production)

  [Download win poppler release](https://github.com/oschwartz10612/poppler-windows/releases)
  Extract the zip, copy the nested folder "poppler-x.x.x." to a program folder (e.g. C:\Program Files\poppler-24.08.0)
  Add poppler executable (C:\Program Files\poppler-24.08.0\Library\bin) to system PATH

  ```pwsh
  $pathToAdd = "C:\Program Files\poppler-24.08.0\Library\bin"; `
  $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine); `
  if ($currentPath -split ';' -notcontains $pathToAdd) { `
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$pathToAdd", [System.EnvironmentVariableTarget]::Machine) `
  }
  ```

---

## 👷 Contributors

Build/distribute pkg from `websolutespa` bom [[Github](https://github.com/websolutespa/bom)]

> dir in `robot` project folder

```bash
  cd ./src/robot
```

### 🔖 requirements

```bash
py -m pip install --upgrade setuptools build twine streamlit 
```

### 🪛 build

```pwsh
if (Test-Path ./dist) {rm ./dist -r -force}; `
cp .\requirements.txt .\ws_bom_robot_app\ && `
py -m build && `
twine check dist/*
```

### 📦 test / 🧪 debugger

Install the package in editable project location

```pwsh
py -m pip install --upgrade -e .
py -m pip show ws-bom-robot-app
```

launch the debugger

```pwsh
streamlit run debugger.py --server.port 6002
```

### ✈️ publish

- [testpypi](https://test.pypi.org/project/ws-bom-robot-app/)

  ```pwsh
  twine upload --verbose -r testpypi dist/*
  #py -m pip install -i https://test.pypi.org/simple/ --upgrade ws-bom-robot-app 
  ```

- [pypi](https://pypi.org/project/ws-bom-robot-app/)

  ```pwsh
  twine upload --verbose dist/* 
  #py -m pip install --upgrade ws-bom-robot-app
  ```
