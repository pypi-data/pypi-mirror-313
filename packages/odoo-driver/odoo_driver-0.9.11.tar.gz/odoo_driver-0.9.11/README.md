![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/odoo-driver)
![PyPI - Downloads](https://img.shields.io/pypi/dm/odoo-driver)
![GitLab last commit](https://img.shields.io/gitlab/last-commit/60778766)
![GitLab stars](https://img.shields.io/gitlab/stars/60778766?style=social)

# Odoo Drivers

This tools is intented to be used with the Odoo Point of sale application. It replaces the Odoo [IoT Box](https://www.odoo.com/app/iot) or the
Community [pywebdriver](https://github.com/pywebdriver/pywebdriver) library.

Once installed locally in the cashier computer, devices will be discovered by the tool,
once plugged, and communication can be done with the Odoo Point of Sale module.

# Table of contents

1. [Run](#run)
2. [Usage](#usage)
3. [Installation](#installation)
4. [Related Odoo Modules](#related-odoo-modules)
5. [Compatible Devices](#compatible-devices)
6. [How to Contribute](#how-to-contribute)
7. [Development](#development)
7. [Roadmap and Known Issues](#roadmap-and-known-issues)
8. [Credits](#credits)

## <div id="run">Run</div>

```shell
odoo-driver\
  --address 0.0.0.0\
  --port 8069\
  --secure\
  --refresh-devices-delay 1\
  --log-level INFO\
  --log-folder false\
  --options EXTRA_OPTIONS
```

(The values displayed above are the default values.

* ``-a / --address``: address where the web service will be available

* ``-p / --port``: port where the web service will be available

* ``--secure/--unsecure``: expose webservice with https
  (or http, if ``--unsecure`` is selected).

* ``-r / --refresh-devices-delay``: interval in seconds
  between two checks of devices connected to usb ports.

* ``-l / --log-level``: Possible values:
  ``TRACE`` / ``DEBUG`` / ``INFO`` / ``SUCCESS`` /
  ``WARNING`` / ``ERROR`` / ``CRITICAL``.
  Note:
  - ``TRACE`` will log all the http call.
  - ``DEBUG`` will log all the data received, including images received by the
    printer device.
  - Use ``INFO`` level or higher in production outside a debugging situation.

* ``-f / --log-folder``: Optional directory that will contains logs.
  If defined, it should exist and be writable.

* ``--options``: Json formatted data to pass to devices. Ex:
  ``'{"scale": {"polynomial": 123456}}'``
  That will pass the polynomial value to the scale device.
  Note: don't forget the simple quote at the beginning and the end of the
  dictionnary.

## <div id="usage">Usage</div>

Go the home page of the tool, via https://localhost:8069.

If you choose https deployment, you should accept the first time
a security exception in your browser.

![security_exception](https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/odoo_driver/static/readme/security_exception.png)


Pages are available to test connections, see errors, etc.

![home_page](https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/odoo_driver/static/readme/home_page.png)

## <div id="installation">Installation</div>

### Installation (to run it manually)

* install the latest released version:

```shell
pipx install odoo-driver
```odoo

* _or_ Install the latest version:

```shell
pipx install git+https://gitlab.com/grap-rhone-alpes/odoo-driver.git
```

Note: use ``--python python3.9`` (or higher) option, if your default python environment is under python 3.9 version.

### Installation (as a service)

This will create a service (via systemd) that will execute odoo-driver in the background and launches at startup.

```shell
wget https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/debian_install.sh
# (OPTIONAL) adapt the installation script before execution
# adding specific argument in the call of odoo-driver in the .service file
sudo sh debian_install.sh
```

Once installed, you can run the following system command.

```shell
# Get status of the service
sudo systemctl status odoo-driver.service

# Follow the logs of the service
sudo journalctl -fu odoo-driver.service
```

## <div id="related-odoo-modules">Related Odoo Modules</div>

Compatibility of the library with Odoo Modules, depending on the version.

### V16

- Printer (+ Cashbox): ``point_of_sale`` (Odoo CE)

- Display: [``pos_odoo_driver_display``](https://github.com/grap/odoo-addons-pos)

- Payment: [``pos_odoo_driver_payment``](https://github.com/grap/odoo-addons-pos)

- Scale: ``point_of_sale`` (Odoo CE)

## <div id="compatible-devices">Compatible Devices</div>

<table style="width: 100%;">
    <tbody>
        <tr>
            <th colspan="2"><h3>Printers</h3></th>
        </tr>
        <tr>
            <td>
              <li>
                Epson - TM-T20II<br/>
                Epson - TM-T20III<br/>
                Epson - TM-T88V
              </li>
            </td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/odoo_driver/static/devices/printer__epson__tm_t20.png" width="200" height="200" />
            </td>
        </tr>
        <tr>
            <th colspan="2"><h3>Display</h3></th>
        </tr>
        <tr>
            <td>Aures - OCD 300</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/odoo_driver/static/devices/display__aures__ocd_300.png" width="200" height="200" />
            </td>
        </tr>
        <tr>
            <th colspan="2"><h3>Payment Terminal</h3></th>
        </tr>
        <tr>
            <td>Ingenico - Move/5000</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/odoo_driver/static/devices/payment__ingenico__move_5000.png" width="200" height="200" />
            </td>
        </tr>
        <tr>
            <th colspan="2"><h3>Scale</h3></th>
        </tr>
        <tr>
            <td>Mettler Toledo - Ariva S</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-driver/-/raw/main/odoo_driver/static/devices/scale__mettler_toledo__ariva_s.png" width="200" height="200" />
            </td>
        </tr>
    </tbody>
</table>

## <div id="how-to-contribute">How to Contribute</div>

### Welcome contributions

* If the project is not translated into your language,
  you can propose a translation.

* If you've encountered a problem or bug that you've solved,
  the patch will be very welcome !

### Unwelcome contributions

Please **do not propose** a Merge Request before opening first an issue on gitlab,
if you want to add new feature, new devices, etc.

Maintaining a driver library is an impossible task if you don't own the device.
If the device or the feature you propose is not in the Roadmap of the GRAP company,
it will be refused, to avoid rising technical debt.

In that case, do not hesitate to fork the project, to implement your change
in a dedicated branch.

## <div id="development">Development</div>

See the dedicated section [here](https://gitlab.com/grap-rhone-alpes/odoo-driver/-/blob/main/DEVELOP.md).

## <div id="roadmap-and-known-issues">Roadmap and Known Issues</div>

See the dedicated section [here](https://gitlab.com/grap-rhone-alpes/odoo-driver/-/blob/main/ROADMAP.md).

## <div id="credits">Credits</div>

### Authors

* GRAP <https://www.grap.coop>

### Contributors

* Sylvain LE GAL <sylvain.legal@grap.coop>

### Extra authorship

Part of the code in this project comes from the following projects, including:

  * [Pywebdriver](https://github.com/pywebdriver/pywebdriver) (AGPL-3.0), by GRAP. Main contributors are:

    * Sylvain LE GAL <sylvain.legal@grap.coop>
    * Sylvain CALADOR <sylvain.calador@akretion.com>
    * Sébastien BEAU <sebastien.beau@akretion.com>
    * Carmen BIANCA BAKKER <carmen@coopiteasy.be>
    * Alexis DE LATTRE <alexis.delattre@akretion.com>
    * Quentin DUPONT <quentin.dupont@grap.coop>
    * Pierrick BRUN <pierrick.brun@akretion.com>
    * Hugues DE KEYZER  <hugues@coopiteasy.be>

  * [hw_dialog06_scale](https://github.com/coopiteasy/iot/tree/12.0-dialog06/hw_dialog06_scale) (AGPL-3.0), by Coop It Easy. Main contributors are:

    * Vincent Van Rossem <vincent.vanrossem@camptocamp.com>

  * [pyposdisplay](https://github.com/akretion/pyposdisplay) (AGPL-3.0), by Akretion. Main contributors are:

    * Alexis DE LATTRE <alexis.delattre@akretion.com>
    * Sébastien BEAU <sebastien.beau@akretion.com>

The following projects were also useful and were studied to realize this library.

  * [Odoo](https://github.com/odoo/odoo) (AGPL-3.0 up to version 8.0, and then LGPL-3.0 from version 9.0 onwards), by Odoo SA, specially "hw_" modules.

### Images

* [Main Application icon](https://www.flaticon.com/fr/icones-gratuites/hub-usb), by AbtoCreative (Flaticon).

* [Credit Card Payment Terminal Icon](https://www.flaticon.com/fr/icone-gratuite/terminal-de-paiement_6137350), created by ToZ Icon (Flaticon).

* [LCD Customer Display Icon](https://www.flaticon.com/fr/icone-gratuite/lcd_9622586), created by Iconic Panda (Flaticon).

* [Thermal Receipt Printer Icon](https://www.flaticon.com/fr/icone-gratuite/facture_1649343), created by Icongeek26 (Flaticon).

* [Scale Icon](https://www.flaticon.com/fr/icone-gratuite/pesee_1104592), created by itim2101 (Flaticon).
