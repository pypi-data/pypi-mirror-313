.. _overview:

.. |SecureKey (TM)| unicode:: SecureKey U+2122
   .. with trademark sign



Overview
========

The |SecureKey (TM)| VPN (SK-VPN) is a IPsec VPN and Firewall gateway.
Combining the protections of the |SecureKey (TM)| Cryptographic Library and hardened open-source software
including VPP, DPDK, StrongSwan, and FastAPI, the SK-VPN offers next generation security and performance.
Protecting multi-cloud networks to secure enterprises from advaned threats.

.. _conops:

Concept of Operations
---------------------

The |SecureKey (TM)| VPN + Firewall lies at the heart of a secure cloud network. 
As a Point-to-Point VPN, it is used to connect private networks across the internet.
As a Stateful and Stateless Firewall it has the ability to filter inbound and outbound network traffic.
The SK-VPN uses the strongest commercially available IPsec Encryption standards to encrypt traffic between networks.


The SK-VPN protects multi-cloud networks and can be used as a cloud gateway for hybrid networks. 
The below image shows an example network protected by the SK-VPN. 
The SK-VPN virtual machine is a gateway device and a traffic aggregator, allowing multiple 
private network segments to connect securely. 


.. image:: images/SK-VPN-Overview.png
    :align: center

Each cloud provider has their own concept of virtual networks. SK-VPN is designed to operate accross all cloud providers,
details for networking specific to each cloud provider are found in the following sections:

* :ref:`Azure Cloud <azure_overview>`
* :ref:`Google Cloud <google_overview>`




.. _security:


Security
--------

The |SecureKey (TM)| VPN was designed with security at the forefront. 
The SK-VPN uses the Patent Pending |SecureKey (TM)| Cryptographic Library to protect keys and secure networks beyond existing commercial standards.

More information about the |SecureKey (TM)| Cryptographic Library can be found at https://www.jettechlabs.com

The SK-VPN supports the following security standards:

Data Plane:

* CNSA v1.0 Algorithms for IKEv2 and IPsec see: `CNSA v1.0 <https://media.defense.gov/2021/Sep/27/2002862527/-1/-1/0/CNSS%20WORKSHEET.PDF>`_ 
* RSA (3072-bit+), ECC (P-384), AES-256-GCM, SHA-384
* Certificate Based Authentication IKEv2
* *Disallow*: Pre-Shared Keys (PSK), IKEv1, non-CNSA v1.0 algorithms
   
Management Interface:

* HTTPS using TLS 1.2+
* Password Based Authentication + Multi-Factor Authentication (MFA)
* Client Certificate Authentication (Mutual TLS)
* Role Based Access Control (RBAC)
* OpenAPI 3.0 compatible REST API
* Secure Shell (SSH) certificate-based authentication
* Command Line Interface (CLI) accessible over SSH and serial console
* Authenticated + Encrypted Syslog over TLS
* Encrypted + Authenticated Software Update using our secure servers



.. _performance_features:


Performance and Features
------------------------

The |SecureKey (TM)| VPN and Firewall uses high performance, open-source software
enhanced with SecureKey Cryptography for a data plane capable of bandwidths above 10 Gbps+ (AES-256-GCM).
The SK-VPN bandwidth scales up when deployed on larger Virutal Machines with more vCPUs.

The SK-VPN supports the following features and standards:

* IPsec VPN
   * Certificate Based Authentication using IKEv2
   * Route Based Point-to-Point IPsec
   * High Speed AES-256-GCM encryption (10 Gbps+)
* Access Control List (ACL) based firewall
   * Stateful and Stateless Modes
   * Layer2-4 Filtering
* Dynamic Name Server (DNS) + DNS Security Extensions (DNSSEC)
* Network Time Protocol (NTP)
* Syslog + Authenticated/Encrypted Syslog over TLS
* Dynamic Host Configuration Portocol (DHCP)
* Certificate Signing Requests (CSR)
  
  





