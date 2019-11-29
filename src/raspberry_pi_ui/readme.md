# raspberry-pi-ui

## Install Dependencies
### Raspbian
One of the main dependencies is the `gi` module. For Raspbian, it is included in system site-packages. However, system site-packages are by default not included in the virtual environment. In order to not flood our `requirements.txt` with unused system site-packages, we should refrain from including system site-packages in the virtual environment. In order to install the `gi` module, follow the steps below (thanks to [this SO answer](https://stackoverflow.com/questions/26678457/how-do-i-install-python3-gi-within-virtualenv)):

1. Install GTK+ 3 / GIR.
`sudo apt-get install libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0 gir1.2-webkit-3.0`
2. Activate your virtual environment, and then install `pygobject`: `pip3 install pygobject`
3. Test whether `gi` module is available now:

### MacOS
`gi` module is NOT included in MacOS at all. We have to install it via `homebrew` (for details, check [this doc](https://pygobject.readthedocs.io/en/latest/getting_started.html#macosx-getting-started)). And then install `pygobject` in the virtual environment (again, thanks to [this SO answer](https://stackoverflow.com/questions/26678457/how-do-i-install-python3-gi-within-virtualenv)):

1. Install GTK+ 3 with Homebrew: `brew install gtk+3`. 
2. Activate your virtual environment, and then install `pygobject`: `PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig ARCHFLAGS="-arch x86_64" pip3 install pygobject`
3. Test whether `gi` module is available now.

`webkit` is also NOT included in MacOS. One might need to download it from [the official website](https://webkit.org/downloads/). However, this is not tested.

## Spin up UI Window
To spin up the UI window, run `python3 rpi_in_driver.py -p [public_id]` from root directory and under virtual environment. `public_id` is a unique string to specify MQTT channel. It must be the same for `rpi_in_driver` and `rpi_out_driver` to enable communication between the two.

## Testing
UI testing is tricky. So far, we haven't found an easy solution to simulate button click to fully test our UI. But we are able to run simple test on non-event related functions in the UI object. According to the [documentation](https://pygobject.readthedocs.io/en/latest/guide/testing.html), Travis-ci doesn't have up-to-date GTK version in its Ubuntu virtual machine, so testing of PyGObject has to be done in a Docker container. This is no longer correct, as of 11/05/2019, Travis-ci provides Ubuntu 18.04 (Bionic) which has GTK version 3.22, enough to test UI built from PyGObject.

On the other hand, using Docker container might be able to test UI, but since all the Docker images shown on [the example](https://github.com/pygobject/pygobject-travis-ci-docker-examples) have Python version no higher than 3.5, compatibility with code written in Python 3.7 is a serious issue (e.g. support for f-string starts in Python 3.6). Therefore, it is much easier to test directly on Travis-CI's virtual machine by specifying `dist: bionic`.