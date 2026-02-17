# activate the virtual environment for the lab
source vcwk/bin/activate

echo Running Flask

if ! [[ -z $1 ]]; then
    flask --app $1 run --debug
else
    flask run --debug
fi
