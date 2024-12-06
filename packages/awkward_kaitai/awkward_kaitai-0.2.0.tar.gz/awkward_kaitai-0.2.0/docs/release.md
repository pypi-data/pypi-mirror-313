# How to release the packages

## Python package

The Python package is released to PyPI:

<https://pypi.org/project/awkward-kaitai/>

To release a new version, tag it in the repository and push the tag:

```bash
git tag -a 0.x.0 -m "Release 0.x.0"
git push origin 0.x.0
```

Then, create a new release on Github with the same tag and generate the release notes.

Make sure the repository is clean and the submodule has no extra changes:

```bash
git submodule update
```

Then, run the following commands to check the version:

```bash
pip install hatch
hatch version
```

And finally, release the package:

```bash
hatch release
```





