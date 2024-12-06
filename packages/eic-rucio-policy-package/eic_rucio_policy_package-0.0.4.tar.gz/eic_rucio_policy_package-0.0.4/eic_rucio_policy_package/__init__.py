SUPPORTED_VERSION = ["1.29", "1.30", "1.31", "32", "33", "34", "35"]

def get_algorithms():
    return { 'lfn2pfn': { 'eic': lfn2pfn_eic },
             'surl': { 'eic': construct_surl_eic } }


def lfn2pfn_eic(scope, name, rse, rse_attrs, protocol_attrs):
    """
    Given a LFN, convert it directly to a path using the mapping:
    note: scopes do not appear in pfn.

        scope:name -> name

    :param scope: Scope of the LFN. 
    :param name: File name of the LFN.
    :param rse: RSE for PFN (ignored)
    :param rse_attrs: RSE attributes for PFN (ignored)
    :param protocol_attrs: RSE protocol attributes for PFN (ignored)
    :returns: Path for use in the PFN generation.
    """

    del rse
    del scope
    del rse_attrs
    del protocol_attrs
    return '%s' % name


def construct_surl_eic(dsn: str, scope: str, filename: str) -> str:
    """
    Defines relative SURL for new replicas. To be used for non-deterministic sites.

    @return: relative SURL for new replica.
    @rtype: str
    """
    fields = dsn.split("/")
    nfields = len(fields)
    if nfields == 0:
        return '/other/%s' % (filename)
    else:
        return '%s/%s' % (dsn, filename)

