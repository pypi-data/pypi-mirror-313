#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

################################################################
from abc import ABC, abstractmethod
################################################################
from . import job
from . import bdlogging
from . import jobselector
################################################################
import os
import getpass
import sys
__all__ = ["Base"]
print = bdlogging.invalidPrint
logger = bdlogging.getLogger(__name__)
################################################################


class AbstractBase(ABC):
    """
    """

    @property
    def Job(self):
        raise RuntimeError('abstractmethod')

    @property
    def Run(self):
        raise RuntimeError('abstractmethod')

    @abstractmethod
    def getSchemaList(self, filter_names=True):
        return []

    @abstractmethod
    def retreiveSchemaName(self, creation=False, **kwargs):
        pass

    @abstractmethod
    def insert(self, zeoobject, keep_state=False):
        pass

    @abstractmethod
    def commit(self):
        pass

    def getRunFromID(self, run_id):
        myrun = self.Run(self)
        myrun["id"] = run_id
        myrun.id = run_id
        run_list = myrun.getMatchedObjectList()
        if len(run_list) != 1:
            raise Exception('Unknown run {0}'.format(run_id))

        return run_list[0]

    def getJobFromID(self, job_id):
        myjob = self.Job(self)
        myjob["id"] = job_id
        myjob.id = job_id
        job_list = myjob.getMatchedObjectList()
        if len(job_list) != 1:
            raise Exception('Unknown run {0}'.format(job_id))

        return job_list[0]

    def createParameterSpace(self, myjob, entry_nb=0,
                             tmp_job=None, nb_inserted=0):
        """
        This function is a recursive call to generate the points
        in the parametric space

        The entries of the jobs are treated one by one
        in a recursive manner
        """

        # keys() gives a non-indexable view
        keys = list(myjob.entries.keys())
        nparam = len(keys)

        # if this is the case I have done all the
        # entries of the job
        # it is time to insert it (after some checks)
        if entry_nb == nparam:
            if tmp_job is None:
                raise RuntimeError("internal error")

            # check if already inserted
            jselect = jobselector.JobSelector(self)
            jobs = jselect.selectJobs(tmp_job, quiet=True)
            if len(jobs) > 0:
                return nb_inserted

            # insert it
            nb_inserted += 1
            logger.info("insert job #{0}".format(nb_inserted) +
                        ': ' + str(tmp_job.entries))
            self.insert(tmp_job)
            return nb_inserted

        if tmp_job is None:
            tmp_job = self.Job()

        # the key that I am currently treating
        key = keys[entry_nb]
        e = myjob[key]

        # if this is a list I have to create several parametric points
        if not isinstance(e, list):
            e = [e]
        for value in e:
            tmp_job[key.lower()] = value
            nb_inserted = self.createParameterSpace(
                myjob, entry_nb+1, tmp_job, nb_inserted)

        if self.truerun:
            self.commit()
        return nb_inserted

    @abstractmethod
    def getStudySize(self, study):
        raise RuntimeError("abstract method")

    def checkStudy(self, dico):
        if "study" not in dico:
            schemas = self.getSchemaList()
            if len(schemas) == 1:
                dico['study'] = schemas[0]
                return
            message = "\n" + "*"*30 + "\n"
            message += "Parameter 'study' must be provided at command line\n"
            message += "possibilities are:\n"
            for s in schemas:
                message += "\t" + s + "\n"
            message += "\n"
            message += "FATAL => ABORT\n"
            message += "*"*30 + "\n"
            logger.error(message)
            sys.exit(-1)

    def __init__(self, connection=None, truerun=False, **kwargs):
        self.connection = connection
        if self.connection is None:
            raise RuntimeError("This class must be derived")

        if 'user' in kwargs:
            self.user = kwargs["user"]
        else:
            self.user = getpass.getuser()

        if ("should_not_check_study" not in kwargs):
            self.checkStudy(kwargs)

        if 'study' in kwargs:
            self.retreiveSchemaName(**kwargs)

        self.truerun = truerun

        if "list_parameters" in kwargs and kwargs["list_parameters"] is True:
            message = self.getPossibleParameters()
            logger.info("\n{0}".format(message))
            sys.exit(0)

    def getPossibleParameters(self):
        myjob = self.Job()
        message = ""
        message += ("*"*65 + "\n")
        message += ("Job parameters:\n")
        message += ("*"*65 + "\n")
        params = [str(j[0]) + ": " + str(j[1])
                  for j in myjob.types.items()]
        message += ("\n".join(params)+"\n")

        myrun = self.Run()
        message += ("*"*65 + "\n")
        message += ("Run parameters:\n")
        message += ("*"*65 + "\n")
        params = [str(j[0]) + ": " + str(j[1])
                  for j in myrun.types.items()]
        message += ("\n".join(params))
        return message

################################################################


def find_root_path(path):
    tmp = os.path.join(path, '.bd')
    if os.path.exists(tmp):
        return path

    abs_path = os.path.abspath(path)
    head, tail = os.path.split(abs_path)
    while (head != '') and (head != '/'):
        tmp = os.path.join(head, '.bd')
        if os.path.exists(tmp):
            return head
        head, tail = os.path.split(head)
    raise RuntimeError(
        f"Could not find a BlackDynamite root directory from {path}")


def Base(**params):
    if 'host' in params and params['host'] is not None:
        host = params['host']
        host_split = host.split('://')
        if host_split[0] == 'file':
            raise RuntimeError("cannot use sqlit anymore")
            # from . import base_sqlite
            # params['host'] = host_split[1]
            # return base_sqlite.BaseSQLite(**params)
        elif host_split[0] == 'zeo':
            from . import base_zeo
            return base_zeo.BaseZEO(**params)
        else:
            raise RuntimeError("broken")
            # from . import base_psql
            # return base_psql.BasePSQL(**params)

    else:
        from . import base_zeo
        path = find_root_path(os.path.realpath('./'))
        params['host'] = 'zeo://' + path
        base = base_zeo.BaseZEO(**params)
        if base.schema is not None:
            params['study'] = base.schema
        return base
    raise RuntimeError("Should not happen")
