if [ "$(ls | grep venv)" ]
then
  . venv/bin/activate
else
  virtualenv venv
  . venv/bin/activate
  pip install -r requirements.txt
fi

python3 main.py
