# -*- coding: utf-8 -*-
from .interfaces import IMessageQueue
from collective.taskqueue import taskqueue
from rer.newsletter import logger
from zope.interface import implementer


QUEUE_NAME = "rer.newsletter.redis"
VIEW_NAME = "message_sendout"


@implementer(IMessageQueue)
class TCMessageQueue(object):
    def start(self, context):
        """Queues message for sendout through collective.taskqueue"""
        jobid = taskqueue.add(
            "/".join(context.getPhysicalPath() + (VIEW_NAME,)),
            queue=QUEUE_NAME,
        )
        if jobid:
            logger.info("Processo in coda: " + str(jobid))
            return jobid
