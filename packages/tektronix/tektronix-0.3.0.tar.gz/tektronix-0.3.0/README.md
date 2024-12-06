# tektronix

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[tektronix][] is a Python 3.8+ package providing modules and helpers to work
with data files from [Tektronix][tek] test equipment.

## Dependencies

### Runtime Dependencies

- [numpy][]

### Development Dependencies

- [invoke][]
- [nose][]
- [unipath][]

## Support Tektronix Equipment

### Spectrum Analyzers

Below are the modules available in the tektronix package and the
compatible equipment for each module:

- rsa500: RSA500 spectrum analyzer

## Contributing

Use the following commands to create a Python virtualenv using [pyenv][] and
[pyenv-virtualenv][], install the requirements in the virtualenv, and list the
available [Invoke][] tasks.

```bash
$ brew install pyenv pyenv-virtualenv
$ pyenv install 3.13
$ pyenv virtualenv 3.13 tektronix
$ pyenv activate tektronix
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ inv -l
```

### Sample CSV and other data files

Currently, the only sample files tested are the CSV files from a N9340B
and E4411B spectrum analyzer. If you have other data files saved from a
Keysight/Agilent/HP piece of test equipment and are willing to share it,
please open an issue or submit a pull request to let us know.

## Contributing

Contributions are welcome! To contribute please:

1. Fork the repository
2. Create a feature branch
3. Code
4. Submit a [pull request][]

## Testing

## License

[tektronix] is released under the MIT license. Please see the [LICENSE.txt] file
for more information.

[tek]: https://www.tek.com/
[tektronix]: https://github.com/questrail/tektronix
[coveralls image]: http://img.shields.io/coveralls/questrail/tektronix/master.svg
[coveralls link]: https://coveralls.io/r/questrail/tektronix
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[invoke]: http://www.pyinvoke.org
[LICENSE.txt]: https://github.com/questrail/tektronix/blob/develop/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/tektronix.svg
[nose]: http://nose.readthedocs.io/en/latest/
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pypi ver image]: http://img.shields.io/pypi/v/tektronix.svg
[pypi ver link]: https://pypi.python.org/pypi/tektronix
[python standard library]: https://docs.python.org/2/library/
[scott chacon]: http://scottchacon.com/about.html
[siganalysis]: https://github.com/questrail/siganalysis
[travis image]: http://img.shields.io/travis/questrail/tektronix/master.svg
[travis link]: https://travis-ci.org/questrail/tektronix
[unipath]: https://github.com/mikeorr/Unipath
