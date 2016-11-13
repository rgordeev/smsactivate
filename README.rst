smsactivate
=====

.. image:: https://travis-ci.org/rgordeev/smsactivate.svg?branch=master
   :target: http://travis-ci.org/rgordeev/smsactivate

Wrapper for SMS activation service http://sms-activate.ru


Installation
------------

Download from github and put smsactivate directory into your root project folder.
And then use import expression.

Usage
-----

smsactivate can be imported as a Python package.


Python Package Usage
~~~~~~~~~~~~~~~~~~~~
Here are examples of all current features:

.. code-block:: pycon

    >>> import smsactivate
    >>> smsactivate.get_balance('my_api_key')
    ACCESS_BALANCE:490
    >>> smsactivate.get_numbers_status('my_api_key')
    {'av_0': '133', 'we_0': '605', 'av_1': '317', 'dt_0': '447', 'mm_0': '265', 'bd_0': '674', 'ym_0': '674', 'fb_0': '642', 'uk_0': '673', 'tw_0': '674', 'me_0': '672', 'vk_0': '0', 'ya_0': '638', 'wb_0': '0', 'ub_0': '31', 'gt_0': '127', 'kp_0': '607', 'sn_0': '637', 'tg_0': '604', 'go_0': '334', 'ot_0': '532', 'mb_0': '0', 'ok_0': '0', 'vi_0': '380', 'fd_0': '604', 'ss_0': '664', 'ma_0': '674', 'ig_0': '0', 'qw_0': '648', 'ot_1': '269', 'wa_0': '672'}
    >>> smsactivate.get_number('my_api_key')
    ACCESS_NUMBER:12608620:79036839671
    >>> smsactivate.get_status('my_api_key', '12608620')
    STATUS_WAIT_CODE
    >>> smsactivate.set_status('my_api_key',-1,'12608620')
    ACCESS_CONFIRM_GET


License
-------

This project is released under an `MIT License`_.

.. _mit license: http://th.mit-license.org/2013
