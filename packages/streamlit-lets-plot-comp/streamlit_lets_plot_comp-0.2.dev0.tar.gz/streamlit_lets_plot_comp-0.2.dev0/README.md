
#### Running demo

```
python -m streamlit run examples/example.py
```


#### Using dev version of Lets-Plot

- `conda activate streamlit-lets-plot`  (it should be a Python 3.8 env)
- `pip install --no-index --find-links=/Users/Igor/Work/lets-plot/python-package/dist/ lets-plot --no-deps --force-reinstall`
- serve lets-plot 'dev' JS using local HTTP-server. 
  In the main lets-plot project:
  - set JS version to "dev" ???
  - build "dev" JS package
    `$ ./gradlew js-package:jsBrowserDevelopmentWebpack`
    (see [lets-plot/js-package/README.md](https://github.com/JetBrains/lets-plot/blob/master/js-package/README.md))
  - start local HTTP-server serving the JS dev-version:
    `$ python -m http.server 8000`
  