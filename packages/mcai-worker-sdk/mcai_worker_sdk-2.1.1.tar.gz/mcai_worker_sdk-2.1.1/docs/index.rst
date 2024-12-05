.. mcai-worker-sdk documentation master file, created by
   sphinx-quickstart on Thu Jan  5 15:29:45 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
  
.. toctree-filt::
   :maxdepth: 1
   :caption: Core components:
   :hidden:

   worker
   worker_description
   worker_parameters   

.. toctree-filt::
   :maxdepth: 1
   :caption: Advanced components:
   :hidden:
   
   :media: media/filter
   :media: media/format_context
   :media: media/frame
   job_status
   mcai_channel
   :media: media/stream_descriptor


Media Cloud AI Worker SDK 
+++++++++++++++++++++++++


This is the official SDK to develop Media Cloud AI Python workers. This SDK provides class implementations that must be inherited in order to implement your own worker.

Under the hood, this SDK relies on the official `Rust SDK <https://docs.rs/mcai_worker_sdk/latest/mcai_worker_sdk>`_ and uses the same mecanisms to ensure consistent behaviour between Python and Rust workers.

.. only:: media

  .. note::
      You are consulting the media version of this SDK.

.. only:: basic

  .. note::
      You are consulting the classic version of this SDK (without the media feature).

Quick start
-----------

This is a very fast introduction to worker development, please refer to these docs and `examples <https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/-/tree/develop/examples>`_ for more in depth knowledge.

You can also refer to the `official python worker template <https://gitlab.com/media-cloud-ai/workers/templates/python>`_ to help you getting started with worker development!

Install the Python SDK
======================

.. only:: media

  Install the SDK with pip::

    pip install mcai-worker-sdk-media

.. only:: basic

  Install the SDK with pip::

    pip install mcai-worker-sdk


Create your pyproject.toml file
===============================

To implement a worker, a `pyproject.toml` file must be created with metadata describing the worker.
It must at least contain both `project` and `build-system` sections. These information really matter because they will be used to send information to the backend.

Example of a minimal configuration file::

  [project]
  name = "my_python_worker"
  version = "1.2.3"
  description = "A dummy Python worker to help you figure out how it works!"
  license = { text = "MIT" }

  [build-system]
  requires = [
    "mcai_worker_sdk",
  ]


Implement your worker
=====================

You can now write the code of your worker. The SDK tries to provide a straightforward structure for your code. For further details, please check out the docs and examples.


Testing locally
---------------

You can make use of the SOURCE_ORDERS variable to test your worker locally. This variable should be set to the path of a source order file (json).
In that case, the SDK will mock the reception of a message from the backend and execute the job.

For example, you can run::

  SOURCE_ORDERS=examples/source_order.json python py_mcai_worker/worker.py


Logging
-------

This SDK automatically configures the native Python logging module to ensure consistency accross all workers logs.
You can choose to use another logging module or re-configure the default one but be aware that it can have huge drawbacks such as loosing job's ids in the logs.


Runtime configuration
---------------------

Logging
=======

  +----------------+----------------------------------------------------------------------------------------------+
  |   Variable     | Description                                                                                  |
  +================+==============================================================================================+
  | MCAI_LOG       | Log level of the worker (DEBUG, INFO, WARN, ERROR), default to INFO                          |
  +----------------+----------------------------------------------------------------------------------------------+
  | ONLY_JSON_LOGS | Emit only JSON formatted logs                                                                |
  +----------------+----------------------------------------------------------------------------------------------+



AMQP connection
===============

  +---------------------------+----------------------------------------------------------------------------------------------+
  |   Variable                | Description                                                                                  |
  +===========================+==============================================================================================+
  | AMQP_HOSTNAME             | IP or host of AMQP server (default: localhost)                                               |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_PORT                 | AMQP server port (default: 5672)                                                             |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_TLS                  | Enable secure connection using AMQPS (default: false)                                        |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_USERNAME             | Username used to connect to AMQP server (default: guest)                                     |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_PASSWORD             | Password used to connect to AMQP server (default: guest)                                     |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_VHOST                | AMQP virtual host (default: /)                                                               |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_QUEUE                | AMQP queue name used to receive job orders (default: job_undefined)                          |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_DELIVERY_MODE        | AMQP delivery mode. 2 for persistent, 1 for transient (default: 2 persistent)                |
  +---------------------------+----------------------------------------------------------------------------------------------+
  | AMQP_SERVER_CONFIGURATION | Configuration of the RabbitMQ instance. Either standalone or cluster (default: standalone)   |
  +---------------------------+----------------------------------------------------------------------------------------------+


Backend connection
==================

  +------------------+-------------------------------------------------------------------------------------------+
  |   Variable       | Description                                                                               |
  +==================+===========================================================================================+
  | BACKEND_HOSTNAME | URL used to connect to backend server (default: http://127.0.0.1:4000/api)                |
  +------------------+-------------------------------------------------------------------------------------------+
  | BACKEND_USERNAME | Username used to connect to backend server                                                |
  +------------------+-------------------------------------------------------------------------------------------+
  | BACKEND_PASSWORD | Password used to connect to backend server                                                |
  +------------------+-------------------------------------------------------------------------------------------+
