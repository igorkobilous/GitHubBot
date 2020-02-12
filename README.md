# GitHub parser
Bot for search repositories, wikis, issues in GitHub

# How to run

1. Via virtualenv
```bash
sudo apt-get install virtualenv

virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt

python main.py search inputs/input_search.json
```
First argument - controller name (example: search)
Second argument - path to input file (example: inputs/input_search.json)
   
2. Via docker:
```
docker-compose build
docker-compose up search
```
You can change controller name or path to input file in docker-compose.yml file

# Result of work
All result put into outputs directory as json files
   
# Run Tests
```bash
python -m unittest discover
# or
docker-compose up test
```

Test coverage:
```bash
coverage run -m unittest discover
coverage report -m --omit */venv/*,*tests*.py
```