.. _user_management:

User Management
===============

The SK-VPN supports user management via the REST API and CLI. The users created can login using a username + password 
via the CLI or the REST API.

Users may be non-administrators or administrators where administrators can add and remove other users 
and perform all other tasks in the SK-VPN. Non-administrators can only perform basic statistics monitoring
and user management for their own account.


.. _initial_user:

Adding an Initial User
----------------------

The SK-VPN requires an initial user to be setup before any other functionality can be enabled.
The initial user must be an administrator and should be set following the instructions below. 
The REST API and CLI both support creation of the initial user.

From the Web UI:

On initial login the Web interface will prompt for creation of an initial user.


From the REST API:

* Use the ``users/initial`` endpoint to create an initial user
* This user is an administrator and these credentials should be used to add other users.
* Login with the username and password using the ``/auth/token`` endpoint.

From the CLI:

* If an initial user does not exist the CLI will prompt for creation of an initial user.
* Provide the username and password for the initial administrator.
* Login with the username and password.


User Management
---------------

The Web UI allows administrators to manage users and user account settings.

Access User Management from the System -> Users page:

.. image:: images/UI/System_Admin_Users.png
    :align: center
    :scale: 50%

|

User Settings including Profile, Password Changes, and OTP settings are available in the User Settings page:

.. image:: images/UI/User_Settings_Profile.png
    :align: center
    :scale: 50%

|

------------
Adding Users
------------

From the REST API:

* Login with an administrator user.
* Use the ``users/register`` endpoint to create an new user.
* Provide the username and password and the desired role.

From the CLI:

* Login with an administrator user.
* Use the ``add_user`` command to create an new user.
* Provide the username and password and the desired role.

--------------------
Change User Password
--------------------

From the REST API:

* Login with as a user.
* Use the ``users/change-password`` endpoint to change the password for the current user.
* Provide the current username and password and the new password.

From the CLI:

* Login as a user.
* Use the ``change_password`` command to change the password for the current user.
* Provide the current username and password and the new password.

--------------
Removing Users
--------------

From the REST API:

* Login with an administrator user.
* DELETE ``users/[username]``

From the CLI:

* Login with an administrator user.
* Use the ``add_user`` command to create an new user.
* Provide the username and password and the desired role.

----------------------------------
Enable Multi-Factor Authentication
----------------------------------

SK-VPN supports Multi-Factor Authentication (MFA) for users via Timebased One-Time Password (TOTP).
The REST API and CLI can generate QRCodes which can be imported into Duo Security, Google Authenticator and other
MFA applications. Once enabled, users will be required to provide an OTP on login.

Web UI OTP settings are available in the User Settings -> OTP page:

.. image:: images/UI/User_Settings_OTP.png
    :align: center
    :scale: 50%

|

From the REST API:

* Sign in with your Username and Password. 
* Use the ``auth/otp/generate-qrcode`` endpoint to generate a QRCode.
* Use Duo Security or Google Authenticator to scan the QRCode.
* To enable OTP for your user, use the ``auth/otp/enable`` endpoint.
* Re-login and provide the OTP in the auth/token "client_secret" field .


From the CLI:

* Sign in with your Username and Password. 
* Generate a QRCode by running the following command: ``generate_otp_qrcode``
* Use Duo Security or Google Authenticator to scan the QRCode.
* To enable OTP for your user, run the following command: ``enable_otp``
* Logout and re-login now with MFA enabled an OTP will be required on login.
  
.. image:: images/sk_vpn_cli_otp_qrcode.png
    :align: center

|

.. _ssh_user_mgmt:

SSH User Management
-------------------
SSH users can be added allowing for SSH access to the SK-VPN. 

From the Web UI:

System -> SSH Users allows administrators to manage SSH users.

From the REST API:

* Login with an administrator user.
* To add a new SSH user: POST `name` and `public_key` to the ``users/ssh`` endpoint.
* To delete an SSH user: DELETE ``users/ssh/[username]`` endpoint.
* To get all current SSH users: Get ``users/ssh/all`` endpoint.

.. note::
    SSH users are independent from the password based username(s) that are used to login to the CLI and REST API.
    SSH users access the command line interface via SSH with the ``ssh -i [keyfile] [ssh_user]@[hostname]`` command.

    Once the SSH user is authenticated (using SSH public key authentication), the user must login 
    via the CLI using a username + password (+ MFA if enabled). 
    see :ref:`user_management`.
    
    It is possible to use the same username for SSH and CLI/REST API but it is not required.


Next Steps:
Configure System Security see :ref:`security_configuration`



