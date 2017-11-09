* Update setup.py to reflect new version numbers

nano setup.py

* Commit updates

* Tag repository

git tag 0.0.5 -m"message"

* Push tags

git push --tags origin master

* Remove items from dist/

rm dist/*

* Build source distribution

python setup.py sdist

* Push to pypi

 twine upload dist/*
