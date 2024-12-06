# Copyright 2023 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.

import logging

import pyrfc3339

from juju.errors import JujuAPIError

from . import model, tag
from .annotationhelper import _get_annotations, _set_annotations
from .client import client

log = logging.getLogger(__name__)


class Unit(model.ModelEntity):
    @property
    def agent_status(self):
        """Returns the current agent status string.

        """
        return self.safe_data['agent-status']['current']

    @property
    def agent_status_since(self):
        """Get the time when the `agent_status` was last updated.

        """
        return pyrfc3339.parse(self.safe_data['agent-status']['since'])

    @property
    def is_subordinate(self):
        """True if the unit is subordinate of another unit

        """
        return self.safe_data['subordinate']

    @property
    def principal_unit(self):
        """Returns the name of the unit of which this unit is a subordinate to.
        Returns '' for principal units themselves.
        """
        return self.safe_data['principal']

    @property
    def agent_status_message(self):
        """Get the agent status message.

        """
        return self.safe_data['agent-status']['message']

    @property
    def workload_status(self):
        """Returns the current workload status string.

        """
        return self.safe_data['workload-status']['current']

    @property
    def workload_status_since(self):
        """Get the time when the `workload_status` was last updated.

        """
        return pyrfc3339.parse(self.safe_data['workload-status']['since'])

    @property
    def workload_status_message(self):
        """Get the workload status message.

        """
        return self.safe_data['workload-status']['message']

    @property
    def machine(self):
        """Get the machine object for this unit.

        """
        machine_id = self.safe_data['machine-id']
        if machine_id:
            return self.model.machines.get(machine_id, None)
        else:
            return None

    @property
    def public_address(self):
        """ Get the public address.

        This property is deprecated, use get_public_address method.
        """
        return self.safe_data['public-address'] or None

    @property
    def tag(self):
        return tag.unit(self.name)

    def get_subordinates(self):
        """Returns the unit objects that are subordinates to this unit

        :return [Unit]
        """
        return [u for u_name, u in self.model.units.items() if u.is_subordinate and
                u.principal_unit == self.name]

    async def destroy(self):
        """Destroy this unit.

        """
        app_facade = client.ApplicationFacade.from_connection(self.connection)

        log.debug(
            'Destroying %s', self.name)

        return await app_facade.DestroyUnits(unit_names=[self.name])
    remove = destroy

    async def get_public_address(self):
        """Return the public address of this unit.

        :return int public-address
        """
        addr = self.safe_data['public-address'] or None
        if addr is not None:
            return addr

        app_facade = client.ApplicationFacade.from_connection(self.connection)
        defResult = await app_facade.UnitsInfo(entities=[client.Entity(self.tag)])
        if defResult is not None and len(defResult.results) > 1:
            raise JujuAPIError("expected one result")
        return defResult.results[0].result.get('public-address', None)

    async def resolved(self, retry=False):
        """Mark unit errors resolved.

        :param bool retry: Re-execute failed hooks
        :returns: A :class:`juju.client._definitions.ErrorResults` instance.
        """
        app_facade = client.ApplicationFacade.from_connection(self.connection)

        log.debug(
            'Resolving %s', self.name)

        return await app_facade.ResolveUnitErrors(
            all_=False,
            retry=retry,
            tags={'entities': [{'tag': self.tag}]})

    async def run(self, command, timeout=None):
        """Run command on this unit.

        :param str command: The command to run
        :param int timeout: Time, in seconds, to wait before command is
        considered failed
        :returns: A :class:`juju.action.Action` instance.

        """
        action = client.ActionFacade.from_connection(self.connection)

        log.debug(
            'Running `%s` on %s', command, self.name)

        if timeout:
            # Convert seconds to nanoseconds
            timeout = int(timeout * 1000000000)

        res = await action.Run(
            applications=[],
            commands=command,
            machines=[],
            timeout=timeout,
            units=[self.name],
        )
        return await self.model.wait_for_action(res.results[0].action.tag)

    async def run_action(self, action_name, **params):
        """Run an action on this unit.

        :param str action_name: Name of action to run
        :param **params: Action parameters
        :returns: A :class:`juju.action.Action` instance.

        Note that this only enqueues the action.  You will need to call
        ``action.wait()`` on the resulting `Action` instance if you wish
        to block until the action is complete.

        """
        action_facade = client.ActionFacade.from_connection(self.connection)

        log.debug('Starting action `%s` on %s', action_name, self.name)

        res = await action_facade.Enqueue(actions=[client.Action(
            name=action_name,
            parameters=params,
            receiver=self.tag,
        )])
        action = res.results[0].action
        error = res.results[0].error
        if error and error.code == 'not found':
            raise ValueError('Action `%s` not found on %s' % (action_name,
                                                              self.name))
        elif error:
            raise Exception('Unknown action error: %s' % error.serialize())
        action_id = action.tag[len('action-'):]
        log.debug('Action started as %s', action_id)
        # we mustn't use wait_for_action because that blocks until the
        # action is complete, rather than just being in the model
        return await self.model._wait_for_new('action', action_id)

    async def scp_to(self, source, destination, user='ubuntu', proxy=False,
                     scp_opts=''):
        """Transfer files to this unit.

        :param str source: Local path of file(s) to transfer
        :param str destination: Remote destination of transferred files
        :param str user: Remote username
        :param bool proxy: Proxy through the Juju API server
        :param scp_opts: Additional options to the `scp` command
        :type scp_opts: str or list
        """
        await self.machine.scp_to(source, destination, user=user, proxy=proxy,
                                  scp_opts=scp_opts)

    async def scp_from(self, source, destination, user='ubuntu', proxy=False,
                       scp_opts=''):
        """Transfer files from this unit.

        :param str source: Remote path of file(s) to transfer
        :param str destination: Local destination of transferred files
        :param str user: Remote username
        :param bool proxy: Proxy through the Juju API server
        :param scp_opts: Additional options to the `scp` command
        :type scp_opts: str or list
        """
        await self.machine.scp_from(source, destination, user=user,
                                    proxy=proxy, scp_opts=scp_opts)

    async def ssh(
            self, command, user='ubuntu', proxy=False, ssh_opts=None):
        """Execute a command over SSH on this unit.

        :param str command: Command to execute
        :param str user: Remote username
        :param bool proxy: Proxy through the Juju API server
        :param str ssh_opts: Additional options to the `ssh` command

        """
        return await self.machine.ssh(command, user, proxy, ssh_opts)

    async def is_leader_from_status(self):
        """
        Check to see if this unit is the leader. Returns True if so, and
        False if it is not, or if leadership does not make sense
        (e.g., there is no leader in this application.)

        This method is a kluge that calls FullStatus in the
        ClientFacade to get its information. Once
        https://bugs.launchpad.net/juju/+bug/1643691 is resolved, we
        should add a simple .is_leader property, and deprecate this
        method.

        """
        unit_parts = self.name.split("/")
        app = unit_parts[0]

        client_facade = client.ClientFacade.from_connection(self.connection)

        status = await client_facade.FullStatus(patterns=None)
        # FullStatus may be more up to date than our model, and the
        # unit may have gone away, or we may be doing something silly,
        # like trying to fetch leadership for a subordinate, which
        # will not be filed where we expect in the model. In those
        # cases, we may simply return False, as a nonexistent or
        # subordinate unit is not a leader.
        if not status.applications.get(app):
            return False

        # We will attempt to look in two places for a leader property based on
        # if the unit is subordinate or not. These variables allow for more
        # generic non discriminate checks
        target_apps = [app]
        is_subordinate = False

        # Is the application a subordinate? If so change our data variables to
        # the parent
        if status.applications[app].subordinate_to:
            is_subordinate = True
            target_apps = status.applications[app].subordinate_to

        for target_app in target_apps:
            app_data = status.applications[target_app]

            if not app_data.units:
                continue

            if app_data.units.get(self.name):
                is_leader = app_data.units[self.name].leader
                return is_leader if is_leader else False

            if not is_subordinate:
                continue

            for key, unit in app_data.units.items():
                if unit.subordinates and unit.subordinates.get(self.name):
                    is_leader = unit.subordinates[self.name].leader
                    return is_leader if is_leader else False

        return False

    async def get_metrics(self):
        """Get metrics for the unit.

        :return: Dictionary of metrics for this unit.

        """
        metrics = await self.model.get_metrics(self.tag)
        return metrics[self.name]

    async def get_annotations(self):
        """Get annotations on this unit.

        :return dict: The annotations for this unit
        """
        return await _get_annotations(self.tag, self.connection)

    async def set_annotations(self, annotations):
        """Set annotations on this unit.

        :param annotations map[string]string: the annotations as key/value
            pairs.

        """
        return await _set_annotations(self.tag, annotations, self.connection)
