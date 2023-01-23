#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------
import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pyagentx2.network')
logger.addHandler(NullHandler())
# --------------------------------------------

import socket
import time
import threading

import pyagentx2
from pyagentx2.pdu import PDU
from pyagentx2.sethandler import GenErrException, NoAccessException, WrongTypeException, WrongLengthException, WrongEncodingException, WrongValueException, NoCreationException, InconsistentValueException, ResourceUnavailableException, NotWritableException, InconsistentNameException


class Network(threading.Thread):

    def __init__(self, mib, oid_list, sethandlers):
        threading.Thread.__init__(self)
        self.stop = threading.Event()
        self._oid_list = oid_list
        self._sethandlers = sethandlers
        self._transactions = {} # To store information about set-test,commit,cleanup open transactions

        self.session_id = 0
        self.transaction_id = 0
        self.debug = 1

        # Data Related Variables
        self.mib = mib

    def _connect(self):
        while True:
            try:
                self.socket = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
                self.socket.connect(pyagentx2.SOCKET_PATH)
                self.socket.settimeout(0.1)
                return
            except socket.error:
                logger.error("Failed to connect, sleeping and retrying later")
                time.sleep(2)

    def new_pdu(self, type):
        pdu = PDU(type)
        pdu.session_id = self.session_id
        pdu.transaction_id = self.transaction_id
        self.transaction_id += 1
        return pdu

    def response_pdu(self, org_pdu):
        pdu = PDU(pyagentx2.AGENTX_RESPONSE_PDU)
        pdu.session_id = org_pdu.session_id
        pdu.transaction_id = org_pdu.transaction_id
        pdu.packet_id = org_pdu.packet_id
        return pdu

    def send_pdu(self, pdu):
        if self.debug: pdu.dump()
        self.socket.send(pdu.encode())
        
    def recv_pdu(self):
        buf = self.socket.recv(1024)
        if not buf: return None
        pdu = PDU()
        pdu.decode(buf)
        if self.debug: pdu.dump()
        return pdu


    # =========================================

    def run(self):
        while True:
            try:
                self._start_network()
            except socket.error:
                logger.error("Network error, master disconnect?!")

    def _start_network(self):
        self._connect()

        logger.info("==== Open PDU ====")
        pdu = self.new_pdu(pyagentx2.AGENTX_OPEN_PDU)
        self.send_pdu(pdu)
        pdu = self.recv_pdu()
        self.session_id = pdu.session_id

        logger.info("==== Ping PDU ====")
        pdu = self.new_pdu(pyagentx2.AGENTX_PING_PDU)
        self.send_pdu(pdu)
        pdu = self.recv_pdu()

        logger.info("==== Register PDU ====")
        for oid in self._oid_list:
            logger.info("Registering: %s" % (oid))
            pdu = self.new_pdu(pyagentx2.AGENTX_REGISTER_PDU)
            pdu.oid = oid
            self.send_pdu(pdu)
            pdu = self.recv_pdu()

        logger.info("==== Waiting for PDU ====")
        while True:
            try:
                request = self.recv_pdu()
            except socket.timeout:
                continue

            if not request:
                logger.error("Empty PDU, connection closed!")
                raise socket.error

            tid = "%s_%s" % (request.session_id, request.transaction_id)
            response = self.response_pdu(request)
            if request.type == pyagentx2.AGENTX_GET_PDU:
                logger.info("Received GET PDU")
                for rvalue in request.range_list:
                    oid = rvalue[0]
                    logger.debug("OID: %s" % (oid))
                    value = self.mib.get(oid)
                    if value is not None:
                        response.values.append(value)
                    else:
                        logger.debug("OID Not Found!")
                        response.values.append({'type':pyagentx2.TYPE_NOSUCHOBJECT, 'name':rvalue[0], 'value':0})

            elif request.type == pyagentx2.AGENTX_GETNEXT_PDU:
                logger.info("Received GET_NEXT PDU")
                for rvalue in request.range_list:
                    value = self.mib.get_next(rvalue[0],rvalue[1])
                    if value is not None:
                        response.values.append(value)
                    else:
                        response.values.append({'type':pyagentx2.TYPE_ENDOFMIBVIEW, 'name':rvalue[0], 'value':0})

            elif request.type == pyagentx2.AGENTX_TESTSET_PDU:
                logger.info("Received TESTSET PDU")

                # Clean if the transaction already exists
                self._transactions[tid] = []

                idx = 0
                for row in request.values:
                    idx += 1
                    oid = row['name']
                    type = row['type']
                    type_ = pyagentx2.TYPE_NAME.get(row['type'], 'Unknown type')
                    value = row['data']
                    logger.info("Name: [%s] Type: [%s] Value: [%s]" % (oid, type_, value))

                    # Find matching sethandler
                    matching_oid = ''
                    for target_oid in self._sethandlers:
                        if oid.startswith(target_oid):
                            matching_oid = target_oid
                            break
                    if matching_oid == '':
                        logger.debug('TestSet request failed: not writeable #%s' % idx)
                        response.error = pyagentx2.ERROR_NOTWRITABLE
                        response.error_index = idx
                        break

                    # Call the test function and store varBind in transaction
                    try:
                        self._sethandlers[matching_oid].test(oid, type, value, self.mib)
                        self._transactions[tid].append((matching_oid, oid, type, value))
                    except GenErrException:
                        logger.debug('TestSet request failed: genErr #%s' % idx)
                        response.error = pyagentx2.ERROR_GENERR
                        response.error_index = idx
                        break
                    except NoAccessException:
                        logger.debug('TestSet request failed: noAccess #%s' % idx)
                        response.error = pyagentx2.ERROR_NOACCESS
                        response.error_index = idx
                        break
                    except WrongTypeException:
                        logger.debug('TestSet request failed: wrongType #%s' % idx)
                        response.error = pyagentx2.ERROR_WRONGTYPE
                        response.error_index = idx
                        break
                    except WrongLengthException:
                        logger.debug('TestSet request failed: wrongLength #%s' % idx)
                        response.error = pyagentx2.ERROR_WRONGLENGTH
                        response.error_index = idx
                        break
                    except WrongEncodingException:
                        logger.debug('TestSet request failed: wrongEncoding #%s' % idx)
                        response.error = pyagentx2.ERROR_WRONGENCODING
                        response.error_index = idx
                        break
                    except WrongValueException:
                        logger.debug('TestSet request failed: wrongValue #%s' % idx)
                        response.error = pyagentx2.ERROR_WRONGVALUE
                        response.error_index = idx
                        break
                    except NoCreationException:
                        logger.debug('TestSet request failed: noCreation #%s' % idx)
                        response.error = pyagentx2.ERROR_NOCREATION
                        response.error_index = idx
                        break
                    except InconsistentValueException:
                        logger.debug('TestSet request failed: inconsistentValue #%s' % idx)
                        response.error = pyagentx2.ERROR_INCONSISTENTVALUE
                        response.error_index = idx
                        break
                    except ResourceUnavailableException:
                        logger.debug('TestSet request failed: resourceUnavailable #%s' % idx)
                        response.error = pyagentx2.ERROR_RESOURCEUNAVAILABLE
                        response.error_index = idx
                        break
                    except NotWritableException:
                        logger.debug('TestSet request failed: notWritable #%s' % idx)
                        response.error = pyagentx2.ERROR_NOTWRITABLE
                        response.error_index = idx
                        break
                    except InconsistentNameException:
                        logger.debug('TestSet request failed: inconsistentName #%s' % idx)
                        response.error = pyagentx2.ERROR_INCONSISTENTNAME
                        response.error_index = idx
                        break
                    except:
                        logger.debug('Unexpected error')
                        break

                logger.debug('TestSet request passed')


            elif request.type == pyagentx2.AGENTX_COMMITSET_PDU:
                logger.info("Received COMMITSET PDU")
                if tid in self._transactions:
                    idx = 0
                    for matching_oid, oid, type, value in self._transactions[tid]:
                        idx += 1
                        try:
                            self._sethandlers[matching_oid].commit(oid, type, value, self.mib)
                        except:
                            logger.error('CommitSet failed')
                            response.error = pyagentx2.ERROR_COMMITFAILED
                            response.error_index = idx
                    del (self._transactions[tid])


            elif request.type == pyagentx2.AGENTX_UNDOSET_PDU:
                if tid in self._transactions:
                    del (self._transactions[tid])

            elif request.type == pyagentx2.AGENTX_CLEANUPSET_PDU:
                if tid in self._transactions:
                    del (self._transactions[tid])

            self.send_pdu(response)


