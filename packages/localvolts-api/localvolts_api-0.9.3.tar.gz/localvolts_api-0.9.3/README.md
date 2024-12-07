# localvolts

This project is not ready for use yet. It is a work in progress.

## Tagging a new version

First update setup.py with the new version number. Then run the following command:

```bash
python setup.py sdist bdist_wheel
```

Also tag the release via a git tag and push it to the repository:

```bash
git tag -a v0.6 -m "Release 0.6"
git push origin v0.6
```

## Use

Link directly to this tag in your requirements.txt file:

```
localvolts_api @ git+https://github.com/iconnor/localvolts@v0.2
``` 