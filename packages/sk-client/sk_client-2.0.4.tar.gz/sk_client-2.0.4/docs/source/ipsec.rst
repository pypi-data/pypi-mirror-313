.. _ipsec_setup:

IPSec Setup
===========

.. _ipsec_certificates:

Setup IPSec Certificates
------------------------

The SK-VPN supports certificate based IKEv2 Security Associations.

The SK-VPN Web UI Certificates page is used to install and manage IPsec certificates:

.. image:: images/UI/Certificates.png
    :align: center

|

To setup IKEv2 Certificates using the REST API:

(*Pre*) Generate a CA Root Certificate and Private Key pair which will be used to sign the device Certificate.
see :ref:`ca_generation`

* Export a Certificate Signing Request: POST ``/cert/signing-request`` see :ref:`cert_csr`
* Sign the CSR with the CA Root Private Key see :ref:`cert_signing`.
* Upload the signed certificate to the SK-VPN via the POST ``/cert/signed_csr`` endpoint with the `usage` field set to `IPSEC`
* Verify the Certificate detials using the GET ``/cert/certs`` and ``/cert/details``

.. _ipsec_connections:

IPSec Connections
-----------------
An IPsec Connection is a set of parameters to define an IKE (phase 1) connection and a set of (phase 2) Child Security Associations.
The SK-VPN supports IKEv2 Certificate-based authentication only (no Pre-Shared Key PSK support due to the lack of key security).

The SK-VPN requires a user to upload then activate the connection, activation loads the connection into the dataplane. 
Details of the active (loaded) connections along with the details of the child SAs are available via the REST API and the Web UI.

Active Connections and Connection Details and Statistics are available on the Web UI IPsec -> Active Sessions page:

.. image:: images/UI/IPsec_Active_Sessions.png
    :align: center

|

Connections can be created, modified, deleted and activated using the Web UI IPsec -> Saved Connections page:

.. image:: images/UI/IPsec_Activate_Conn_Menu.png
    :align: center
    :scale: 50%

|


IPSec Connections are managed using the REST API:

* Upload a new connection: POST ``/ipsec/connections``
* Activate a connection: POST ``/ipsec/connections/loaded/<name>``
* Deactivate a connection: DELETE ``/ipsec/connections/loaded/<name>``
* Get the list of saved connections: GET ``/ipsec/connections/saved``
* Get the list of active connections: GET ``/ipsec/connections/loaded``
* Delete a connection: DELETE ``/ipsec/connections``

.. _security_associations:

IPSec Security Associations
---------------------------
IPSec Connections define a set of Security Associations (SAs) that 
will be installed on the SK-VPN. IPsec ESP Tunnel Mode is used by default.

Each Security Association defines a secure tunnel between the SK-VPN and a remote peer.

Active SAs are managed using the Web UI IPsec -> Active Sessions page and selecting the 
Actions Menu item for the Active SA to activate or terminate:

.. image:: images/UI/IPsec_Activate_SA_Menu.png
    :align: center
    :scale: 50%

|


Security Associations are managed using the REST API. 

* Get the list of active SAs: GET ``/ipsec/sas``
* Force Initiation of an SA: POST ``/ipsec/sas/initiate-child``
* Force Termination of an SA: POST ``/ipsec/sas/terminate-child``
* Get list of a Connection's SAs: GET ``/ipsec/connections`` use the `children` field for the list of SAs


Next Steps
-----------
System Monitoring see :ref:`system_monitoring`