===============
berpublicsearch
===============

.. image:: https://img.shields.io/pypi/l/berpublicsearch
    :target: https://img.shields.io/pypi/l/berpublicsearch
    :alt: License

.. image:: https://img.shields.io/pypi/v/berpublicsearch
    :target: https://img.shields.io/pypi/v/berpublicsearch
    :alt: Pypi version

The aim of this repository is to simplify working work with SEAI's BER Public search dataset

... with the help of the open source `Python` software :code:`dask` and :code:`requests`

... via:

- A `Jupyter Notebook` sandbox environment
- A `berpublicsearch` `Python` library 

------------

Benefits 
--------

Sandbox:

- It's free
- It's fast ... can be run on the cloud via `Google Collab` 
- It downloads the dataset directly ... so no need to login to the SEAI data portal
- It enables wrangling of large, 'live' data (1GB) 

`berpublicsearch` library:

- It can be imported by other projects to automate the downloading of the ber dataset and (optionally) conversion to `parquet`

------------

This repository was setup by the `codema-dev` team as part of the SEAI RD&D funded `Dublin Region Energy Masterplan Project`__

__ https://www.codema.ie/projects/local-projects/dublin-region-energy-master-plan/

.. raw:: html

    <a href="https://www.codema.ie">
        <img src="images/codema.png" height="100px"> 
    </a> &emsp;

.. raw:: html

    <a href="https://www.seai.ie">
        <img src="images/seai.png" height="50px"> 
    </a> &emsp;

------------

Installation
------------

To setup the `berpublicsearch` sandbox:

- Click the Google Collab badge & open `setup.ipynb`:
    
    .. image:: https://colab.research.google.com/assets/colab-badge.svg
            :target: https://colab.research.google.com/github/codema-dev/berpublicsearch
