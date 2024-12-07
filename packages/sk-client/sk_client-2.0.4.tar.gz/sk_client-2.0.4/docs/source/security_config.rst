.. _security_configuration:

Security Configuration
======================

The SK-VPN supports optional security features that are recommended for production networks.

.. _tls_config:

Enable Certificate Based Authentication (Mutual TLS)
----------------------------------------------------
SK-VPN supports Certificate Based Authentication (Mutual TLS) to enhance the security of the HTTPS REST API.
When enabled for the system, the REST API will require client certificates in addition to the Password, and (optionally) a OTP for login.

The SSH user login is always Certificate based, while client side certificates for 
HTTPS REST API is optional - though recommended. 

To Enable Client Certificate Authentication (Mutual TLS) for HTTPS:

* See :ref:`cert_generation` for Generating new client private keys and certificates
* Login as an administrator.
* Upload a client certificate via the POST ``/cert/tls/client-cert`` endpoint
* verify the certificate is in the list using the GET ``/cert/tls/client-cert`` endpoint
* Enable Mutual TLS for the system using: POST ``/sys/tls_settings enpoint`` with `verify_client` field set to true

Now the client certificate is trusted by the system and must be provided in order to access the REST API.
If the client certificate is not provided, the SK-VPN will respond with a 400 error as shown below.

.. image:: images/mutual_tls_error.png
    :align: center

If using the python REST Client library, you can use the `cert` parameter to provide the Client Private Key and Certificate files for Authentication.

.. code-block:: python

    requests_kwargs["cert"] = (client_cert_file, client_key_file)
    requests.post(url, **requests_kwargs)

.. _https_certificates:

Custom HTTPS Certificates
-------------------------

By default, the SK-VPN uses a (self-signed) Certificate for HTTPS Authentication. 
Most Browsers will require adding a security acception to allow using self-signed certificates, 
and in general it is not recommended to use self-signed certificates in production networks.

The SK-VPN allows custom certificates to be used for HTTPS authentication.
As part of a secure network an SK-VPN administrator may use a Certificate Authority (CA) to sign the SK-VPN HTTPS certificate.
The CA Root Certificate can be used by client and browsers so that the SK-VPN can be authenticated. 

In order to use a custom signed HTTPS certificate, use the REST API:

* Generate a Certificate Authority Root Certificate and Private Key pair which will be used to sign the HTTPs Certificate
* Export a Certificate Signing Request: POST ``/cert/signing-request`` see :ref:`cert_csr`

  * Set the `ip_addrs` field to include the Management Interface IP Address. 
  * Set the `dns_names` field to include the Management Interface DNS Name.
  * Note the SK-VPN generates a Private Key and exports the CSR for you to sign.

* Sign the CSR with the CA Root Private Key
* Upload the signed certificate to the SK-VPN via the POST ``/cert/signed_csr`` endpoint with the `usage` field set to https_server
* Upon success the new HTTPS certificates will be used by the SK-VPN.
* Verify the HTTPS Server Certificate detials using the GET ``/cert/tls/server-cert`` endpoint


.. _syslog_configuration:

Syslog Configuration
--------------------
The SK-VPN uses industry standard Syslog formats for system event logging. 
A remote Syslog Server can be used to receive these events. 

Alternatively the System logs may be retrieved using the Web UI System -> System Logs
and using the REST API `sys/logs/*`` endpoints.

The Syslog server may be on a LAN or WAN network and must accessible to the SK-VPN over the Management Interface.

------------------------
Web UI Syslog Management
------------------------

The Web UI can be used to manage Syslog settings.

.. image:: images/UI/System_Admin_Syslog.png
    :align: center
    :scale: 40%

|

Remote Syslog setup is achieved via the REST API with a POST to ``sys/syslog/settings``.

* `server_address` field must be set to the IP address of the remote Syslog Server.
* `server_port` field must be set to the port of the remote Syslog Server.
* `enable_remote_syslog` field must be set to True to enable remote Syslog.
* (Optional *Recommended*) `enable_authentication` field is set to True to enable Syslog Authentication (see below).

------------------------------------
Syslog Authentication and Encryption
------------------------------------

Syslog Authentication and encryption over TLS is supported.

The SK-VPN allows certificates to be created and uploaded for Syslog authentication via the CSR mechanism.
An SK-VPN administrator may use a Certificate Authority (CA) to sign the SK-VPN Syslog certificate and 
must provide the CA certificate to the SK-VPN to allow mutual authentication.

The CA Root Certificate is uploaded via the REST API `cert/syslog/ca` enpoint and 
allows the SK-VPN to authenticate the Syslog Server.

In order to generate a Syslog client certificate, use the REST API:

* (*Pre*) Generate a Certificate Authority Root Certificate and Private Key pair which will be used to sign the Certificate
* Export a Certificate Signing Request: POST ``/cert/signing-request``  see :ref:`cert_csr`
* Sign the CSR with the CA Root Private Key
* Upload the signed certificate to the SK-VPN via the POST ``/cert/signed_csr`` endpoint with the `usage` field set to `SYSLOG_CLIENT`
* Verify the Certificate detials using the GET ``/cert/syslog/client-cert``, ``/cert/syslog/ca-cert`` and ``/cert/syslog/ca``
* Enable syslog authentication: POST ``sys/syslog/settings`` with the `enable_authentication` field set to True


.. _dns_config:

DNS Configuration
-----------------
The SK-VPN supports DNS configuration allowing for DNS based authentication (DNSSEC) and custom servers.

A list of servers and fallback_servers is configurable. 
Users specify a list of IP address, port and domains for DNS servers.

The default DNS servers are Cloudflare and Google:

* 1.1.1.1
* 1.0.0.1
* 8.8.8.8
* 8.8.4.4

The Web UI can be used to manage DNS settings.

.. image:: images/UI/System_Admin_DNS.png
    :align: center
    :scale: 40%

|

The REST API can be used to configure DNS:

* Upload DNS Settings POST ``/sys/dns/settings`` endpoint





Once Security is configured, the SK-VPN can be used to setup IPSec connections see :ref:`ipsec_setup`



