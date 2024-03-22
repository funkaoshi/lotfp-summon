# Summon

You can use this web app to go through the motions of casting the first level 
Magic-User's spell Summon, as outlined on page 142 of the Rules and Magic 
book of the role-playing game Lamentations of the Flame Princess. Who thought
letting first level characters cast this spell was a good idea?

## Install

1. Create a virtual environment: python -m venv <envlocation>
2. Activate the environment: sourve <envlocation>/bin/activate
3. pip install -r requirements.txt
4. gunicorn summon:app

That should get it running locally.
