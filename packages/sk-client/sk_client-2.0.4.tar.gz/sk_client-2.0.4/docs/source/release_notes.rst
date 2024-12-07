.. _release_notes:

Release Notes
=============

Release v2.0
--------------

SecureKey Crypto Library v2.0 updates:
 * Improved AES throughput over SecureKey v1 (3X+ increase for small packets)
 * Added support for AES-256-CTR and AES-256-CBC modes
 * SecureKey OpenSSL Provider updates:
 * SecureKey provider protects Certificates, Private Keys and Secret data in memory for Authentication and Key Exchange
 * SecureKey provider protects AES keys in memory during encryption and decryption
 * FIPS Certification is in progress


* SecureKey OpenSSL Provider used for Management Plane (SSH, HTTPS, and IKEv2)
* Enforce strong algorithms/curves for SSH and HTTPS (AES-256, and CNSA v1.0 algorithms where available)
* Multi-layer encryption for stored Private Keys using LUKS and Database encryption
* Update SecureKey Logo and Web UI color scheme
* Stateful Firewall improvements - added ACL session management


Bug Fixes:

* Update COTS packages to latest versions
* Bug fixes for the REST API and Web UI


Release v1.3
--------------
Google Cloud support.

Bug Fixes and improvements:

* Support for Google Cloud (required drivers have been added)
* Update data plane package versions
* Bug fixes and new features for the Web UI


Release v1.2
--------------
Web User Interface improvements.

Bug Fixes and improvements:

* Historical statistics endpoints return a 10 minute history
* Fixes and new features for the Web UI
* Interface, Firewall, IPsec, and drop counters for charts now use historical data
* Changes to IPsec connection to allow editing existing connections
* Update certificate details for all certificate types
* Add Interface chart and Runtime staistics 
* Allow download of CSR PEM file data
* Add support for Extended Sequence Numbers (ESNs)
* Various API updates and bug fixes in support of the Web User Interface
* Open Source package updates and bug fixes



Release v1.1
--------------
Web User Interface has been added to allow management and configuration of the SK-VPN using a web browser.

Bug Fixes and improvements.

* Fix MAC/LAN address Role assignment - was failing if the initial LAN/WAN ip address was 10.X.0.X where X >= 10
* REST API now allows LAN/WAN MAC assignemnt even if initial IPs are not valid or unassigned
* ACL IP Rules now use an Integer for Protocol instead of string

 
New Features and REST API updates:

* Expand Version reporting in sys/version 
* Expand system report in sys/system-report to report "build-type"
* Web User Interface 
* Various API updates and bug fixes in support of the Web User Interface



Release v1.0
--------------
v1.0.1717174796

Initial Release of the SecureKey VPN.
SecureKey Crypto library v1.0 is used to secure keys used by the data plane.

