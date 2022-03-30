rm -r build
rm -r dist
rm -r dongsw.egg-info
python setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*