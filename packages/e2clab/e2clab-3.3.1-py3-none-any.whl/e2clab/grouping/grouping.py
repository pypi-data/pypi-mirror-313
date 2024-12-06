"""
Groupings module
"""

import copy
import itertools
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from enoslib import Host

from e2clab.log import get_logger


@dataclass
class Grouping:
    """Base class for our grouping strategy."""

    __metaclass__ = ABCMeta

    def __init__(self, hosts: list[Host], service_extra_info: list[dict], prefix: str):
        """
        :param hosts: List[Host]. List of enoslib hosts.
        :param service_extra_info: List[Dict] with extra information:
               e.g., [{key: value},...,{key: value}].
        :param prefix: str. Prefix to access an extra info of a Service in workflow.yaml
               file, e.g.: prefix.extra_info ({{ kafka.url }})
        """
        self.hosts = hosts
        self.service_extra_info = service_extra_info
        self.prefix = prefix

        self.logger = get_logger(__name__, ["GROUP"])

    @abstractmethod
    def distribute(self) -> list[Host]:
        """
        Adds `extra` info in Hosts.
        :return: List[Host]. List of enoslib hosts.
        """
        pass


class AddressMatch(Grouping):
    """
    This is used internally by E2Clab.
    It adds the Service extra information (generated after service registration) in
    '_self' attribute of the Service.

    Extra information generated after service registration refer to:
        - extra information defined by users `self.register_service(..., extra=extra)`
          for instance `container_name`, 'workers', etc.
        - extra information defined by E2Clab, for instance, the service id, IPv4,
          IPv6, and URL.

          {
             ``_id``: '1_1_1',
             ``__address__``: '10.52.0.9',
             ``url``: '10.52.0.9:9999',
             ``__address4__``: '10.52.0.9',
             ``url4``: '10.52.0.9:9999',
             ``container_name``: "master",
             ``workers``: ['wk_id_1', 'wk_id_2', 'wk_id_3']
          }

    It allows the following:
            [any service]:
                command... {{ _self.url }} {{ _self.container_name }} -->
                command... 10.52.3.90:9999 master
    """

    def distribute(self):
        new_hosts = []
        for h in self.hosts:
            infos = [
                info
                for info in self.service_extra_info
                if info["__address__"] == h.address
            ]
            if len(infos) > 0:
                _h = copy.deepcopy(h)
                to_inject = {self.prefix: infos[0]}
                # TODO: use set_extra() method instead
                if self.prefix in _h.extra:
                    _h.extra[self.prefix].update(to_inject[self.prefix])
                else:
                    _h.extra.update(to_inject)
                new_hosts.append(_h)
        return new_hosts


class RoundRobin(Grouping):
    """
    Groups Services in round-robin.
    For instance, considering that:
    we have 2 Cloud servers and 4 Edge devices; and
    Edge devices depend on metadata from the Cloud servers:

    - hosts: edge.*
          depends_on:
            - service_selector: cloud.*
              grouping: "round_robin"
              prefix: server

    'edge devices 1 and 3' will have access to metadata from 'cloud server 1',
    'edge device 2 and 4' will have access to metadata from 'cloud server 2'

    It allows the following:
        [device_1]:
            command... {{ server.__address__ }} --> command... 10.52.2.226
        [device_2]:
            command... {{ server.__address__ }} --> command... 192.168.87.254
    """

    def distribute(self):
        cycle_app_info = itertools.cycle(self.service_extra_info)
        new_hosts = []
        for h in self.hosts:
            _h = copy.deepcopy(h)
            to_inject = {self.prefix: next(cycle_app_info)}
            # TODO: Not necessary ?
            # TODO: use set_extra() method instead
            if self.prefix in _h.extra:
                _h.extra[self.prefix].update(to_inject[self.prefix])
            else:
                _h.extra.update(to_inject)
            new_hosts.append(_h)
        return new_hosts


class Asarray(Grouping):
    """
    Groups Services "id".
    For instance, considering that:
    we have 2 Cloud servers and 4 Edge devices; and
    Edge devices depend on metadata from the Cloud servers:

    - hosts: edge.*
        depends_on:
            - service_selector: cloud.*
              grouping: "asarray"
              prefix: server

    'all edge devices' will have access to the "id" of 'all cloud servers'.

    It allows the following:
        [all_devices]:
            command... {{ server }} --> command... ['111', '112']
            command... {{ server[0] }} {{ server[1] }} --> command... 111 112
    """

    def distribute(self):
        new_hosts = []
        for h in self.hosts:
            _h = copy.deepcopy(h)
            to_inject = {self.prefix: []}
            for info in self.service_extra_info:
                to_inject[self.prefix].append(self.__get_id(info["_id"]))
            if self.prefix in _h.extra:
                # Cant't properly update a dict by updating with a list
                # _h.extra[self.prefix].update(to_inject[self.prefix])
                # TODO: fix this behavior of overwriting
                # TODO: use set_extra() method instead
                self.logger.warning(f"{_h.extra[self.prefix]} OVERWRITTEN in {_h}")
                _h.extra[self.prefix] = to_inject[self.prefix]
            else:
                _h.extra.update(to_inject)
            new_hosts.append(_h)
        return new_hosts

    @staticmethod
    def __get_id(_id: str) -> str:
        return "".join(_id.split("_"))


class Aggregate(Grouping):
    """
    Aggregates metadata from various Services.
    For instance, considering that we have:
        2 Cloud servers (1 SERVICE named 'horovod') and
        4 Edge devices (4 SERVICES named 'a', 'b', 'c', 'd');

    [
        CASE 1: Aggregates metadata from a SINGLE Service
                (metadata from all machines that compose this Service)
    ]
        Edge devices depend on metadata from the Cloud servers
        (the 'horovod' service):

        - hosts: edge.*
            depends_on:
                - service_selector: cloud.horovod.*
                  grouping: "aggregate"
                  prefix: horovod

        'all edge devices' will have access to the metadata from 'all cloud servers'
        in 'horovod' service.

        It allows the following:
            [all_devices]:
                command... {{ horovod1_1.url }} {{ horovod1_2.url }} -->
                command... 10.52.3.90:9999 10.52.3.47:9999

    NOTE: In 'horovod1_1', '1_1' is the last part of the Service ID.
          The Service ID is defined as "LayerID_ServiceID_MachineID". For instance:
            'horovod1_1' --> '1_1' means 'ServiceID_MachineID': machine 1 of service 1
            'horovod1_2' --> '1_2' means 'ServiceID_MachineID': machine 2 of service 1

    [
        CASE 2: Aggregates metadata from VARIOUS Services
                (metadata from all machines that compose each Service)
    ]

        All the services in the cloud depends on metadata from the Edge devices.
        Each device is placed in a different service (named 'a', 'b', 'c', 'd').

        - hosts: cloud.*
          depends_on:
            - service_selector: edge.*
              grouping: "aggregate"
              prefix: client

        'all cloud services' will have access to the metadata from 'all edge servers'
        in 'a', 'b', 'c', 'd' services.

        It allows the following:
            [all cloud services]:
                command... {{ client1_1.url }} ... {{ client4_1.url }} -->
                command... 10.152.23.90:9999 ... 10.52.113.147:9999

        NOTE: In 'client1_1', '1_1' is the last part of the Service ID.
          The Service ID is defined as "LayerID_ServiceID_MachineID". For instance:
            'client1_1' --> '1_1' means 'ServiceID_MachineID': machine 1 of service 'a'
            'client4_1' --> '4_1' means 'ServiceID_MachineID': machine 1 of service 'd'
    """

    def distribute(self):
        new_hosts = []
        for h in self.hosts:
            _h = copy.deepcopy(h)
            for info in self.service_extra_info:
                new_prefix = f"{self.prefix}{self.__get_service_id(info['_id'])}"
                to_inject = {new_prefix: info}
                # TODO: use set_extra() method instead
                if new_prefix in _h.extra:
                    _h.extra[new_prefix].update(to_inject[new_prefix])
                else:
                    _h.extra.update(to_inject)
            new_hosts.append(_h)
        return new_hosts

    @staticmethod
    def __get_service_id(_id):
        if len(_id.split("_")) == 3:
            return f"{_id.split('_')[1]}_{_id.split('_')[2]}"  # service id + machine id
        else:
            raise Exception(
                "Service '_id' not compatible. ID must be like: "
                "'LayerIndex_ServiceID_MachineID'."
            )
