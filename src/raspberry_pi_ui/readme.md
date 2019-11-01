# raspberry-pi-ui

## Install Dependencies
### Raspbian
One of the main dependencies is the `gi` module. For Raspbian, it is included in system site-packages. However, system site-packages are by default not included in the virtual environment. In order to not flood our `requirements.txt` with unused system site-packages, we should refrain from including system site-packages in the virtual environment. In order to install the `gi` module, follow the steps below (thanks to [this SO answer](https://stackoverflow.com/questions/26678457/how-do-i-install-python3-gi-within-virtualenv)):

1. Install GTK+ 3 / GIR.
`sudo apt-get install libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0`
2. Activate your virtual environment, and then install `pygobject`: `pip3 install pygobject`
3. Test whether `gi` module is available now:

### MacOS
`gi` module is NOT included in MacOS at all. We have to install it via `homebrew` (for details, check [this doc](https://pygobject.readthedocs.io/en/latest/getting_started.html#macosx-getting-started)). And then install `pygobject` in the virtual environment (again, thanks to [this SO answer](https://stackoverflow.com/questions/26678457/how-do-i-install-python3-gi-within-virtualenv)):

1. Install GTK+ 3 with Homebrew: `brew install gtk+3`. 
2. Activate your virtual environment, and then install `pygobject`: `PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig ARCHFLAGS="-arch x86_64" pip3 install pygobject`
3. Test whether `gi` module is available now.

## Spin up UI Window
To spin up the UI window, run `python3 rpi_in_driver.py` from root directory and under virtual environment.