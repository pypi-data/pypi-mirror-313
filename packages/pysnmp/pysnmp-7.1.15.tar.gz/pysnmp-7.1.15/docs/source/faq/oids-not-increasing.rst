
Dealing with the "OID not increasing" error
-------------------------------------------

Q. I'm walking a particular Agent with the `walk_cmd()` or `bulk_walk_cmd()`
   functions. It works for some OIDs, but invariably fails at certain
   OID with the *OID not increasing* error. What does it mean and
   how do I fix that?

A. The Agent you are talking to seems to be broken. The
   *OID not increasing* message means that in the course of fetching
   OIDs from the Agent, Manager receives an OID that is not greater than those
   passed in request.
   Due to the nature of GETNEXT/GETBULK algorithm, passing the same or
   lesser OID to Manager would result in fetching the same set of OIDs over
   and over again effectively creating an infinite loop between Manager
   and Agent so they may never reach the end of MIB. To prevent this the
   Manager tries to intervene and prevent such loop from happening.

   If you have to work with a broken Agent and can terminate the
   GETNEXT/GETBULK command at some point, you can pass the
   `ignoreNonIncreasingOid=True` keyword parameter to the `walk_cmd()` or `bulk_walk_cmd()`
   to disable OID verification at the Manager side.

.. code-block:: python

    snmpEngine = SnmpEngine()
    async for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in walk_cmd(snmpEngine,
                              CommunityData('public'),
                              await UdpTransportTarget.create(('demo.pysnmp.com', 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity('1.3.6')),
                              ignoreNonIncreasingOid=True):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind])

    snmpEngine.close_dispatcher()
