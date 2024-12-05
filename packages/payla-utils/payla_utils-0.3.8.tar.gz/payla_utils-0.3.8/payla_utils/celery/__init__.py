import structlog
from django.conf import settings

logger = structlog.get_logger(__name__)


def patch_celery_default_queue(celery_app):
    try:
        from celery import bootsteps
        from kombu import Exchange, Queue
        from kombu.common import QoS
    except ImportError:
        logger.exception("Celery is not installed")
        return

    if "amqp://" in settings.CELERY_BROKER_URL:
        # The following is only needed when using RabbitMQ
        # See https://github.com/celery/celery/issues/6067#issuecomment-724003961
        # only needed until a new major version of Celery is released

        class NoChannelGlobalQoS(bootsteps.StartStopStep):
            requires = {"celery.worker.consumer.tasks:Tasks"}

            def start(self, c):
                qos_global = False
                c.connection.default_channel.basic_qos(
                    0,
                    c.initial_prefetch_count,
                    qos_global,
                )

                def set_prefetch_count(prefetch_count):
                    return c.task_consumer.qos(
                        prefetch_count=prefetch_count,
                        apply_global=qos_global,
                    )

                c.qos = QoS(set_prefetch_count, c.initial_prefetch_count)

        # Only use the custom QoS when using RabbitMQ
        # Make sure to create the queue with the x-queue-type quorum argument as this ensure that the queue is durable
        # and replicated across multiple nodes.
        celery_app.steps["consumer"].add(NoChannelGlobalQoS)
        celery_app.conf.task_queues = [
            Queue(
                settings.CELERY_TASK_DEFAULT_QUEUE,
                Exchange(settings.CELERY_TASK_DEFAULT_QUEUE),
                routing_key=settings.CELERY_TASK_DEFAULT_QUEUE,
                queue_arguments={'x-queue-type': 'quorum'},
            ),
        ]
