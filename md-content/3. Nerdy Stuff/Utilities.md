# Utilities

A collection of utilities that seem interesting to me (haven't used them all):

- Rich CMS: https://github.com/jzombie/rich-cms
- Pipper: https://github.com/jzombie/pipper
- Sitemap validator: https://www.xml-sitemaps.com/validate-xml-sitemap.html
- Docker Lynx: https://github.com/jzombie/docker-lynx
- Harlequin (The SQL IDE for Your Terminal [TUI]): https://github.com/tconbeer/harlequin?tab=readme-ov-file
- Textual library: https://textual.textualize.io/#what-is-textual (which Harlequin uses; apps over SSH)
- GitUI (Rust-based TUI): https://github.com/extrawurst/gitui?tab=readme-ov-file#installation
- Dive (Docker image explorer TUI): https://github.com/wagoodman/dive
- Pandaral·lel (Parallelize Pandas operations on all CPUs, by changing only one line of code): https://github.com/nalepae/pandarallel (https://github.com/jzombie/pandarallel)
- Ibis (lightweight, universal interface for data wrangling; Pandas compatible [mostly, according to what I've been lead to believe]): https://github.com/ibis-project/ibis
- Python time distribution as a heatmap: https://github.com/csurfer/pyheat
- Pip requirements.txt generator based on imports in project: https://pypi.org/project/pipreqs/
- MLflow: A Machine Learning Lifecycle Platform: https://github.com/mlflow/mlflow/
- Galactic: cleaning and curation tools for massive unstructured text datasets: https://github.com/taylorai/galactic
- Radicle: Open-Source, P2P GitHub Alternative: https://news.ycombinator.com/item?id=39600810
- Borg Backup: Deduplicating backup (compatible w/ rsync.net): https://github.com/borgbackup/borg
- Lightweight plotting to the terminal (4x resolution via Unicode): https://github.com/olavolav/uniplot
- node-red-contrib-machine-learning: https://flows.nodered.org/node/node-red-contrib-machine-learning
- Monolith: bundle any web page into a single HTML file: https://github.com/Y2Z/monolith
- Jampack: Optimizes static websites for best user experience and best Core Web Vitals scores: https://github.com/divriots/jampack
- QuantStats: Portfolio analytics for quants: https://github.com/ranaroussi/quantstats
- Markmap (Visualize Markdown as mindmaps): https://github.com/markmap/markmap (demo: https://markmap.js.org/repl)
- zerve (Data Science & AI Workbench): https://www.zerve.ai/
- miceforest: Fast, Memory Efficient Imputation with LightGBM (fill in missing values in datasets) https://github.com/AnotherSamWilson/miceforest (LinkedIn post: https://www.linkedin.com/posts/khuyen-tran-1401_miceforest-is-a-python-library-for-imputing-activity-7187108646344916994-Tqo7). Variable importance may be of additional interest: https://github.com/AnotherSamWilson/miceforest?tab=readme-ov-file#variable-importance
- Neural Forecast (User friendly state-of-the-art neural forecasting models): https://github.com/Nixtla/neuralforecast (LinkedIn thread: https://www.linkedin.com/posts/khuyen-tran-1401_timeseries-activity-7192169580264337411-BB6q)
- Itertools (vs. index slicing in Python): https://www.linkedin.com/posts/khuyen-tran-1401_python-activity-7193615521097920512-YwWK (itertools.islice() offers a more efficient approach by enabling the processing of only a portion of the data stream at a time, without the need to load the entire dataset into memory.)
- Insanely Fast Whisper (STT): https://github.com/Vaibhavs10/insanely-fast-whisper
- TimeGPT-1: The first foundation model for forecasting and anomaly detection: https://github.com/Nixtla/nixtla (https://www.linkedin.com/posts/khuyen-tran-1401_timegpt-is-a-powerful-generative-pre-trained-activity-7200865032140673026-uUhg)
- Modin (drop-in Pandas replacement which uses all CPU cores): https://github.com/modin-project/modin (related LinkedIn thread: https://www.linkedin.com/posts/yukikakegawa_python-datascience-dataengineering-activity-7200118431524818946-2-LM/)
- Dask (Python library for parallel and distributed computing): https://docs.dask.org/en/stable/
- PyOD (Python library for detecting anomalies in multivariate data): https://github.com/yzhao062/pyod (LinkedIn thread: https://www.linkedin.com/posts/eric-vyacheslav-156273169_amazing-python-library-pyod-use-it-to-detect-activity-7212107779673661443-hEt5?utm_source=share&utm_medium=member_desktop)
- Hyperfine (Compare the Speed of Two Commands): https://codecut.ai/hyperfine-compare-the-speed-of-two-commands/
- GPU.js (GPU accelerated JavaScript): https://gpu.rocks/
- Lunr (site search with vector support): https://lunrjs.com/ (Getting started: https://lunrjs.com/guides/getting_started.html)
- Text to icon: https://text2icon.app/
- Image to vector SVG: https://vectormaker.co/
- WASM-based image to vector SVG (lower quality, but much faster): https://igutechung.github.io/
- Datamuse (word-finding query engine for developers): https://www.datamuse.com/api/
- Cloudflare Tunnels (reverse-proxy tunnels):
  - https://www.cloudflare.com/products/tunnel/
  - https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
  - https://www.reddit.com/r/selfhosted/comments/ync1zd/cloudflare_tunnels_are_so_awesome/
- react-ts-tradingview-widgets docs: https://tradingview-widgets.jorrinkievit.xyz/docs/intro
- Record and share terminal sessions: https://asciinema.org/
- svg-term-cli: https://github.com/marionebl/svg-term-cli
- Hermes JS Engine [Facebook / React Native] (video: https://www.youtube.com/watch?v=ipYQpxAyunc): https://github.com/facebook/hermes
- ETF Matcher (match ETFs using potential fractional shares): https://etfmatcher.com/

## Services

- RichCMS Git Actions Monitoring: https://github.com/jzombie/rich-cms/actions/
- Rsync.net (cloud backup): https://www.rsync.net/cloudstorage.html

## Python Lists on Disks

- DiskList: A python list implementation that uses the disk to handle very large collections of pickle-able objects. https://github.com/Belval/disklist
- mmaparray: Disk-backed arrays witha  structure similar to Python's built-in array module. https://pypi.org/project/mmaparray/
- Darr: Python library designed for working with large, disk-based Numpy arrays. https://github.com/gbeckers/darr
