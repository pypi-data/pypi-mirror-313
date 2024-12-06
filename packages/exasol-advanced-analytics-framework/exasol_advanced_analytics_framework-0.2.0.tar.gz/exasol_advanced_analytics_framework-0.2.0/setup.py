# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol',
 'exasol.analytics',
 'exasol.analytics.query_handler',
 'exasol.analytics.query_handler.context',
 'exasol.analytics.query_handler.context.proxy',
 'exasol.analytics.query_handler.deployment',
 'exasol.analytics.query_handler.graph',
 'exasol.analytics.query_handler.graph.stage',
 'exasol.analytics.query_handler.graph.stage.sql',
 'exasol.analytics.query_handler.graph.stage.sql.execution',
 'exasol.analytics.query_handler.query',
 'exasol.analytics.query_handler.query.drop',
 'exasol.analytics.query_handler.query.result',
 'exasol.analytics.query_handler.udf',
 'exasol.analytics.query_handler.udf.runner',
 'exasol.analytics.schema',
 'exasol.analytics.sql_executor',
 'exasol.analytics.sql_executor.testing',
 'exasol.analytics.udf.communication',
 'exasol.analytics.udf.communication.discovery',
 'exasol.analytics.udf.communication.discovery.localhost',
 'exasol.analytics.udf.communication.discovery.multi_node',
 'exasol.analytics.udf.communication.peer_communicator',
 'exasol.analytics.udf.communication.peer_communicator.background_thread',
 'exasol.analytics.udf.communication.peer_communicator.background_thread.connection_closer',
 'exasol.analytics.udf.communication.socket_factory',
 'exasol.analytics.udf.utils',
 'exasol.analytics.utils']

package_data = \
{'': ['*'],
 'exasol.analytics': ['lua/src/*',
                      'lua/test/*',
                      'resources/outputs/*',
                      'resources/templates/*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'exasol-bucketfs>=0.6.0,<1.0.0',
 'importlib-resources>=6.4.0,<7.0.0',
 'jinja2>=3.0.3,<4.0.0',
 'nox>=2024.4.15,<2025.0.0',
 'pandas>=2.2.3,<3.0.0',
 'pydantic>=2.10.2,<3.0.0',
 'pyexasol>=0.25.0,<1.0.0',
 'pyzmq>=26.0.3,<27.0.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'structlog>=24.2.0,<25.0.0',
 'typeguard>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'exasol-advanced-analytics-framework',
    'version': '0.2.0',
    'description': 'Framework for building complex data analysis algorithms with Exasol',
    'long_description': '# Exasol Advanced Analytics Framework\n\n**This project is at an early development stage.**\n\nFramework for building complex data analysis algorithms with Exasol.\n\n\n## Information for Users\n\n- [User Guide](doc/user_guide/user_guide.md)\n- [System Requirements](doc/system_requirements.md)\n- [Design](doc/design.md)\n- [License](LICENSE)\n\n## Information for Developers\n\n- [Developers Guide](doc/developer_guide/developer_guide.md)\n\n',
    'author': 'Umit Buyuksahin',
    'author_email': 'umit.buyuksahin@exasol.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/exasol/advanced-analytics-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
