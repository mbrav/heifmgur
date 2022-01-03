<p align="center">
    <a href="https://github.com/mbrav/heifmgur" target="_blank" rel="noopener noreferrer">
        <img width="400" src="media/logo.png" title="heifmgur">
    </a>
</p>

[![Django and Pytest CI](https://github.com/mbrav/heifmgur/actions/workflows/django.yml/badge.svg?event=release)](https://github.com/mbrav/heifmgur/actions/workflows/django.yml)

<p align="center">Image upload service API in Django using High Efficiency Image File Format (HEIF)</p>

## Motivation

This project is a continuation of a job interview assignment. The intention was to create an image service REST API out of it, but not just any API, but one that uses more efficient image formats such as HEIF. Unfortunately however, HEIF format is not well supported in open source projects due to its [proprietary licensing](https://github.com/nokiatech/heif/blob/master/LICENSE.TXT) by Nokia. This includes in image libraries like Django and Pillow, which Django relies on for image validation:

-   [ Support for HEIF #2806 ](https://github.com/python-pillow/Pillow/issues/2806)

While there are existing python libraries that can decode HEIF files, there are none that **encode** into HEIF. Fortunately, there is an exception by using the Python [Wand library](https://pypi.org/project/Wand/) which is a wrapper for ImageMagick command tool. Although it must be system installed in order for the Python library to work, it does contain contain a HEIF decoder. This is why the project uses Wand and [Pillow-SIMD](https://python-pillow.org/pillow-perf/) to [bounce back files](api/utils/img.py) between them. Although Wand is faster than Pillow, it is slower than the x86 performance-optimized Pillow-SIMD.

Due to lack of HEIF support in Pillow, Django's ImageField does not support the format since it uses Pillow for image validation. As a result, a custom field based on Django's FileField had to be written with image validation using the Wand library, which leverages ImageMgick's usage of [libheif](https://github.com/strukturag/libheif) library.

Although writing this project was interesting, I rather wish Nokia Corporation to go bankrupt unless it open sources the HEIC format and allow it to flourish.

## Instructions

Before proceeding make sure [ImageMagick](https://imagemagick.org/script/download.php) is installed on your system and command `magick identify -list format` includes HEIC and HEIF fomrats.

```
$ git clone https://github.com/mbrav/heifmgur.git
$ cd heifmgur
```

Setup a local python environment:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies with poetry:

```
$ poetry install
```

Setup Django database and migrations:

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Setup an admin user (not required):

```
$ python3 manage.py createsuperuser
```

Run server

```
$ python3 manage.py runserver
```

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
