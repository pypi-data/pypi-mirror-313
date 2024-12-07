.. _troubleshooting:

Troubleshooting
===============

.. _troubleshooting_connections:

SSH Connection
--------------
If SSH connections are not working, look at the logs using the REST API sys/logs/ssh for errors. 
The logs may indicate that the user is not authorized or the connection may be in an invalid state.

HTTPS Connection
----------------
If HTTPS connections are not working, look at the logs using the REST API sys/logs/http-access for errors. 
The logs may indicate that the user is not authorized or the connection may be in an invalid state.

If Mutual TLS is enabled for HTTPs you may try disabling it via the Command Line Interface.

Most browsers will not allow a self signed certificate to be used for HTTPS. If you have a self signed certificate,
you may need to add an allowed security exception to your browser. The recommendation is to use a CA signed certificate.
see :ref:`tls_config`


.. _troubleshooting_login:

Login
-----
If attempts to login fail check the logs in sys/logs/user-auth and sys/log for errors.

Ensure that your user exists and that the password is correct.
If OTP is used ensure that the system time is correct and the OTP is generated using the same time.
When creating new users, ensure the password meets the minimum requirements.


.. _troubleshooting_ipsec_issues:

IPSec Connection
----------------
If IPsec connections are not connecting look at the logs in sys/logs/ipsec for errors. 
The logs may indicate a missing certificate or missing keys, or the connection may be in an invalid state.
The peer on the other end of the tunnel must have a matching configuration loaded and active in order to successfully connect.

If the activation of a connection fails, terminate the connection then re-try the activation.

For more information on IPsec see :ref:`ipsec_setup`

Traffic
-------
If IPsec connections are established but traffic is not being received or drops are occurring,
check the dataplane statistics - stats/ipsec, stats/errors, stats/hw, and stats/crypto for details.

The stats/errors may indicate drops due to Access Control List errors see :ref:`setup_acl_rules`

The stats/errors may indicate drops or missed packets due to crypto errors. This may occur if the 
traffic exceeds the capabilities of the system and some packets may be dropped. 

The stats/hw may indicate a hardware error due to a hardware issue or if missed* counters 
are increased this may indicate that traffic is exceeding the capabilities of the system.

The stats/crypto may indicate an issue with the crypto engine or indicate some other unexpected condition.


.. _troubleshooting_swupdate:

SWupdate
--------
If there are failures during SWupdate use the REST API sys/logs/swupdate to see the error logs.

The logs may indicate a failure to download a file in which case attempting the download again may help.

The logs may indicate a failure to install a file in which case attempting the installation again may help,
or a reboot then re-install may help.


.. _troubleshooting_system_errors:

System
------
If the system fails to boot or if there are system failures indicated by the sys/status or /sys/system-report endpoints,
a system failure may have occured in which case attempting the system via sys/reboot may help.

The sys/status will display the health of the major system components, each component may come available at different
times, generally the system should be ready within 30 seconds of reboot, but more time may be needed.


.. _troubleshooting_reporint_errors:

Reporting Issues
----------------
Use the github issues page to report issues.












