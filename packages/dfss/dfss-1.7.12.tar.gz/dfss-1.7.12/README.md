## How to build

rm dist/* build dfss.egg-info -rf
python3 setup.py sdist bdist_wheel --universal
python3 -m twine upload dist/*

