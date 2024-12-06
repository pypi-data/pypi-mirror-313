# EIC Rucio policy package

This is a prototype of the Rucio policy package for eic



## Source files

The package currently contains the following files :
* `eic_rucio_policy_package/__init__.py` - registers the SURL and LFN2PFN algorithms when the package is loaded.
* `eic_rucio_policy_package/permission.py` - permission functions for the policy package.
* `eic_rucio_policy_package/schema.py` - schema functions and data for the policy package.

## How to use this policy package

*  Make sure the directory containing the `eic_rucio_policy_package` is in the PYTHONPATH for the Rucio server.
* add/edit follwoing to rucio.cfg
```
[policy]
package = eic_rucio_policy_package
lfn2pfn_algorithm_default = eic
support = https://github.com/rucio/rucio/issues/
support_rucio = https://github.com/rucio/rucio/issues/
```
* On docker run for rucio-server you need add following:

```
docker run --name=rucio-https-server \
       -e RUCIO_HTTPD_ENCODED_SLASHES=True \
       -e PYTHONPATH=/opt/rucio/  \
```
