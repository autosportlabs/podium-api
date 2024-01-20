# podium_api
Oauth2 API for the motorsports live streaming platform Podium http://podium.live

# development setup
* Install pyenv with >= python 3.8.9 support

* create virtual env
```
pyenv virtualenv 3.8.9 podium-api
```

* activate virtualenv
```
pyenv activate podium-api
```

* install requirements
```
pip install -r requirements.txt
```


After making changes and updating unit tests, run tests:
```
python ./runtests.py
```

# How to deploy

* Determine the next version. Use Semantic Versioning https://semver.org/

* Update setup.py to reflect new version numbers. 

* Commit updates and push

* Tag repository

```
git tag x.y.z -m"message"
```

* Push tags

```
git push --tags origin master
```

* Launch github Publish action to deploy to pypi

