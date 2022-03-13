* Update setup.py to reflect new version numbers

nano setup.py

* Commit updates

* Tag repository

git tag 0.0.5 -m"message"

* Push tags

git push --tags origin master

* Deploy to pypi via Twine (requires twine account)
make dist

