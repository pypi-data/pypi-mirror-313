.. _system_monitoring:

System Monitoring
=================

.. _syslog_monitoring:

Setup Syslog
------------

Syslog is used for system event logging see :ref:`syslog_configuration`.

.. _system_enpoints:

    
Web UI System Monitoring 
------------------------

The Web UI System Admin Page is used to monitor overall system health and status:

.. image:: images/UI/System_Admin_Status.png
    :align: center
    :scale: 25%

System Monitoring API 
---------------------

The REST API `/sys/` endpoints are used to retrieve information about the system state.
It can be used to gather information about the current state of the system
including security relevant information.


System Endpoints are accessible using the REST API:

* Loing as an administrator to access all system endpoints 
* GET ``/sys/status`` returns the current status for all major sub-systems
* GET ``/sys/system-report`` includes information about security settings and open ports.
* GET ``/sys/time`` returns the current system time
* GET ``/sys/version`` returns the system software version
* GET ``/sys/machine-id`` returns the unique identifier for the machine
* GET ``/sys/hostname`` returns the system Hostname
* POST ``/sys/hostname`` set the system Hostname
* POST ``/sys/reboot`` to reboot the system immediately
* POST ``/sys/swupdate`` to upload a new version of system software
* POST ``/sys/swupdate-install`` to install the system software

System endpoints for TLS settings: see :ref:`tls_config`
System endpoints for syslog settings: see :ref:`syslog_configuration`
System endpoints for DNS: see :ref:`dns_config`

.. _system_logs:

System Logs 
-----------


The Web UI can be used to retrieve System Log Files from System -> System Logs:

.. image:: images/UI/System_Admin_Logs.png
    :align: center
    :scale: 25%


System Logs can be retrieved using the REST API:

* Get the system logs: GET ``/sys/logs/[log_name]``

.. note::
  The logs may be rotated if they grow too large and need to be trimmed.
  The default log size is 10MB, if any log is larger than 10MB it will be trimmed.

  Syslog is the most common way of logging system events and 
  is recommended for production systems.

.. _statistics:

System Statistics 
-----------------
System Statistics are available to retrieve informaton about the system hardware and software.


The Web UI can be used to retrieve System Statistics from the Statistics page:

.. image:: images/UI/Stats_HW.png
    :align: center
    :scale: 40%

System Statistics can be viewed using the REST API:

* Get system statistics: GET ``/stats/[stat_name]``

System Statics can also be viewed in the CLI:

* View system statistics: ``show_stats_*``


