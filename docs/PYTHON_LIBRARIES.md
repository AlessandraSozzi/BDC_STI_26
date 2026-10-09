# Python libraries and licenses

All Python packages used by the workshop notebooks in [`notebooks/`](../notebooks/), with the license of each.

Licenses come from each package's PyPI metadata, cross-checked against the license file in its source repository. Last updated September 11, 2026.

| Package | Imported as | Category | License | Version | Notebooks |
| --- | --- | --- | --- | --- | --- |
| `numpy` | `numpy` | Data handling | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | 2.5.3 | Data Extract Satellite Data; Data Preprocessing for GDP Nowcasting; GDP Nowcasting ML Workflow; NTLs Analysis; Trade Nowcasting AIS PortWatch; NLP Fundamentals; Sentiment Analysis; Text Classification; Challenge: GDP Nowcasting; Challenge: Trade Nowcasting |
| `pandas` | `pandas` | Data handling | BSD-3-Clause | 3.0.5 | All except GEE Setup and GEE Account Setup |
| `scipy` | `scipy` | Data handling | BSD-3-Clause | 1.18.1 | NLP Fundamentals |
| `matplotlib` | `matplotlib` | Plotting | Matplotlib License (PSF-based) | 3.11.2 | All except NLP Fundamentals and the three Getting Started notebooks |
| `seaborn` | `seaborn` | Plotting | BSD-3-Clause | 0.13.2 | Data Preprocessing for GDP Nowcasting; GDP Nowcasting ML Workflow; Text Classification; Challenge: GDP Nowcasting |
| `plotly` | `plotly` | Plotting | MIT | 7.0.0 | GDP Nowcasting ML Workflow; Working with AIS PortWatch; Challenge: GDP Nowcasting |
| `pillow` | `PIL` | Plotting | MIT-CMU | 12.3.0 | NTLs Analysis; GDP Nowcasting ML Workflow; Challenge: GDP Nowcasting |
| `tqdm` | `tqdm` | Data handling | MPL-2.0 AND MIT | 4.70.1 | Sentiment Analysis |
| `requests` | `requests` | Data access | Apache-2.0 | 2.34.2 | NTLs Analysis; Google Trends explore; Google Trends extract; Working with AIS PortWatch; Trade Nowcasting AIS PortWatch; Sentiment Analysis; Challenge: Trade Nowcasting |
| `scikit-learn` | `sklearn` | Machine learning | BSD-3-Clause | 1.9.1 | GDP Nowcasting ML Workflow; NLP Fundamentals; Sentiment Analysis; Text Classification; Challenge: GDP Nowcasting |
| `statsmodels` | `statsmodels` | Statistics | BSD-3-Clause | 0.15.0 | Data Extract Satellite Data; Data Preprocessing for GDP Nowcasting |
| `imbalanced-learn` | `imblearn` | Machine learning | MIT | 0.14.2 | Text Classification |
| `shap` | `shap` | Machine learning | MIT | 0.52.0 | GDP Nowcasting ML Workflow; Challenge: GDP Nowcasting |
| `pdpbox` | `pdpbox` | Machine learning | MIT | 0.3.0 | GDP Nowcasting ML Workflow; Challenge: GDP Nowcasting |
| `keras` | `keras` | Machine learning | Apache-2.0 | 3.15.1 | GDP Nowcasting ML Workflow; Challenge: GDP Nowcasting |
| `tensorflow` | Not imported | Machine learning | Apache-2.0 | 2.21.0 | Default backend for `keras`: GDP Nowcasting ML Workflow; Challenge: GDP Nowcasting |
| `torch` | Not imported | Machine learning | Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT | 2.14.0 | Backend for `transformers`, `sentence-transformers` and `sent2vec`: Sentiment Analysis; NLP Fundamentals |
| `earthengine-api` | `ee` | Geospatial | Apache-2.0 | 1.7.43 | GEE Setup; NTLs Analysis; Cropland statistics; Built-up statistics; Data Extract Satellite Data; Data Preprocessing for GDP Nowcasting |
| `geemap` | `geemap`, `geemap.foliumap`, `geemap.cartoee` | Geospatial | MIT | 0.38.5 | GEE Setup; NTLs Analysis; Cropland statistics; Built-up statistics; Data Extract Satellite Data; Data Preprocessing for GDP Nowcasting |
| `geopandas` | `geopandas` | Geospatial | BSD-3-Clause | 1.1.4 | NTLs Analysis; Cropland statistics; Built-up statistics; Working with AIS PortWatch; Challenge: Buildings |
| `shapely` | `shapely` | Geospatial | BSD-3-Clause | 2.1.2 | Built-up statistics; Working with AIS PortWatch; Challenge: Buildings |
| `h3` | `h3` | Geospatial | Apache-2.0 | 4.5.0 | Built-up statistics; Challenge: Buildings |
| `mercantile` | `mercantile` | Geospatial | BSD-3-Clause | 1.2.1 | Built-up statistics |
| `overturemaps` | `overturemaps` | Geospatial | MIT | 1.0.2 | Built-up statistics; Challenge: Buildings |
| `mapclassify` | Not imported | Geospatial | BSD-3-Clause | 2.11.0 | Needed by `GeoDataFrame.explore()`: Built-up statistics; Working with AIS PortWatch; Challenge: Buildings |
| `folium` | Not imported | Geospatial | MIT | 0.20.0 | Needed by `geemap.foliumap` and `GeoDataFrame.explore()`: Built-up statistics; Data Extract Satellite Data; Data Preprocessing for GDP Nowcasting; Working with AIS PortWatch; Challenge: Buildings |
| `ipyleaflet` | Not imported | Geospatial | MIT | 0.20.0 | Needed by interactive `geemap.Map` widgets: GEE Setup; Cropland statistics; Built-up statistics |
| `pyarrow` | Not imported | Geospatial | Apache-2.0 | 25.0.1 | Needed for the Arrow tables returned by `overturemaps`: Built-up statistics; Challenge: Buildings |
| `nltk` | `nltk` | Text analytics | Apache-2.0 | 3.10.3 | NLP Fundamentals; Sentiment Analysis; Text Classification |
| `gensim` | `gensim` | Text analytics | LGPL-2.1-only | 4.4.0 | NLP Fundamentals |
| `sent2vec` | `sent2vec` | Text analytics | MIT | 0.3.0 | The PyPI package is [pdrm83/sent2vec](https://github.com/pdrm83/sent2vec), not the [epfml/sent2vec](https://github.com/epfml/sent2vec) project linked in the notebook: NLP Fundamentals |
| `sentence-transformers` | `sentence_transformers` | Text analytics | Apache-2.0 | 6.0.1 | NLP Fundamentals |
| `transformers` | `transformers` | Text analytics | Apache-2.0 | 5.17.0 | Sentiment Analysis |
| `python-Levenshtein` | `Levenshtein` | Text analytics | GPL-2.0-or-later | 0.27.4 | NLP Fundamentals |
| `beautifulsoup4` | `bs4` | Text analytics | MIT | 4.15.0 | Sentiment Analysis |
| `pysentiment2` | `pysentiment2` | Text analytics | GPL-2.0 (the `License` metadata field says MIT, but the `LICENSE` file in the wheel and in the [GitHub repository](https://github.com/nickderobertis/pysentiment) is GPL v2) | 0.1.1 | Sentiment Analysis |
| `fasttext-numpy2` | `fasttext` | Text analytics | MIT | 0.10.4 | A build of Facebook's fastText packaged for NumPy 2: Text Classification |
| `google-api-python-client` | `googleapiclient` | Data access | Apache-2.0 | 2.200.0 | Google Trends explore; Google Trends extract |
| `pycountry` | `pycountry` | Data access | LGPL-2.1-only | 26.2.16 | Google Trends extract |
| `sdmx1` | Not imported | Data access | Apache-2.0 | 2.27.0 | Installed before importing the `pw_nowcasting_functions` helper module: Trade Nowcasting AIS PortWatch; Challenge: Trade Nowcasting |
| `openpyxl` | Not imported | Data access | MIT | 3.1.5 | Needed by `pandas.read_excel` and `DataFrame.to_excel` for `.xlsx` files: Google Trends explore; Text Classification |
| `google.colab` | `google.colab` (`drive`, `userdata`) | Notebook environment | Apache-2.0 | Not on PyPI ([googlecolab/colabtools](https://github.com/googlecolab/colabtools)) | All except Google Trends explore, GEE Setup and GEE Account Setup |
| `ipython` | `IPython.display` | Notebook environment | BSD-3-Clause | 9.17.1 | Working with AIS PortWatch |
| `ipywidgets` | `ipywidgets` | Notebook environment | BSD-3-Clause | 8.1.9 | Working with AIS PortWatch |
| `jupyter-book` | Not imported | Site build | BSD-3-Clause | 1.0.4 (pinned `>=1,<2`) | Not used by the notebooks; listed in `requirements.txt` |
| `docutils` | Not imported | Site build | Public domain, Python (PSF), BSD-2-Clause and GPL-3.0 parts (see its `COPYING.txt`) | 0.17.1 (pinned) | Not used by the notebooks; listed in `requirements.txt` |
| `jupyterlab` | Not imported | Local setup | BSD-3-Clause | 4.6.3 | Not used by the notebooks; listed in `requirements-notebooks.txt` for running outside Colab |

The notebooks also import these standard library modules, covered by the Python Software Foundation License (PSF-2.0): `builtins`, `collections`, `datetime`, `getpass`, `io`, `json`, `math`, `os`, `pickle`, `random`, `re`, `string`, `sys`, `tempfile`, `time`, `unicodedata`.
