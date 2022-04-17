# SPAtaREST

SPAtaREST este o aplicație IoT pentru un scaun de birou inteligent.

## Instalare

Utilizati package manager-ul [pip](https://pip.pypa.io/en/stable/) pentru a instala dependințele specificate în fișierul `requriements.txt`.
```bash
pip install -r requirements.txt
```

## Utilizare

(Recomandat - setarea unui virtual environment pentru proiect)

```bash
# Setări server Flask
set FLASK_ENV=development
set FLASK_APP=flask_app

# Inițializarea bazei de date SQLite
python -m flask init-db

# Pornirea serverului
python -m flask run --host=0.0.0.0 --port=5000 
```

## Testare

### Unit Testing, Integration Testing
S-au folosit pachetele [pytest](https://docs.pytest.org/en/6.2.x/) pentru testare și [coverage](https://coverage.readthedocs.io/en/6.3/) pentru test coverage. 
Configurația pentru *coverage* se află în fișierul `.coveragerc`, așa că trebuie să rulați doar:
```bash
coverage run
coverage report
```

### Automated Fuzz Testing
S-a folosit tool-ul [RESTler](https://github.com/microsoft/restler-fuzzer). Acesta își construiește o gramatică de testare din specificația de OpenAPI, iar mai apoi generează teste pe endpoint-uri cu payload-uri de forma specificată.
```bash
cd ..
git clone https://github.com/microsoft/restler-fuzzer
mkdir restler_bin
cd restler_bin

# build
python ./build-restler.py --dest_dir .\restler_bin

cd .\restler_bin\restler

# Compilare gramatică
Restler.exe compile --api_spec ..\..\ingineria-programarii\docs\openapi.yaml

# Test
Restler.exe test --grammar_file .\Compile\grammar.json --dictionary_file .\Compile.\dict.json --no_ssl

# Fuzz
Restler.exe fuzz-lean --grammar_file .\Compile\grammar.json --dictionary_file .\Compile.\dict.json --no_ssl
```

## Driver
S-a folosit tool-ul [electron](https://www.electronjs.org/). 
```bash
npm install

npm run electron
```