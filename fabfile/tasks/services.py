from fabfile.config import *
from misc import zoolink
from fabfile.utils.fabos import detect_ostype

@task
def stop_and_disable_qpidd():
    """stops the qpidd and disables it."""
    execute(stop_and_disable_qpidd_node, env.host_string)

@task
def stop_and_disable_qpidd_node(*args):
    """stops the qpidd and disables it in one node."""
    for host_string in args:
        with settings(host_string=host_string, warn_only=True):
            if not run('service qpidd status').succeeded:
                print "qpidd not running, skipping stop."
                return
        with settings(host_string=host_string):
            run('service qpidd stop')
            run('chkconfig qpidd off')

@task
@roles('database')
def stop_database():
    """stops the contrail database services."""
    run('service supervisord-contrail-database stop')

@task
@roles('cfgm')
def stop_cfgm():
    """stops the contrail config services."""
    execute('stop_cfgm_node', env.host_string)

@task
def stop_cfgm_node(*args):
    for host_string in args:
        with settings(host_string=host_string, warn_only=True):
            run('service supervisor-config stop')

@task
@roles('cfgm')
def start_cfgm():
    """starts the contrail config services."""
    with settings(warn_only=True):
        run('service supervisor-config start')

@task
@roles('database')
def start_database():
    """Starts the contrail database services."""
    run('service supervisord-contrail-database start')

@task
@roles('control')
def start_control():
    """Starts the contrail control services."""
    run('service supervisor-control start')

@task
@roles('webui')
def start_webui():
    """starts the contrail webui services."""
    run('service supervisor-webui start')

@task
@roles('collector')
def start_collector():
    """starts the contrail collector services."""
    run('service supervisor-analytics start')

@task
@roles('control')
def stop_control():
    """stops the contrail control services."""
    run('service supervisor-control stop')

@task
@roles('collector')
def stop_collector():
    """stops the contrail collector services."""
    with settings(warn_only=True):
        run('service supervisor-analytics stop')

@task
@roles('compute')
def stop_vrouter():
    """stops the contrail vrouter services."""
    run('service supervisor-vrouter stop')

@task
@roles('webui')
def stop_webui():
    """stops the contrail webui services."""
    run('service supervisor-webui stop')

@task
@roles('database')
def restart_database():
    """Restarts the contrail database services."""
    execute('restart_database_node', env.host_string)

@task
def restart_database_node(*args):
    """Restarts the contrail database services in once database node. USAGE:fab restart_database_node:user@1.1.1.1,user@2.2.2.2"""
    for host_string in args:
        with  settings(host_string=host_string):
            execute('zoolink_node', host_string)
            zoo_svc = 'contrail-zookeeper'
            if detect_ostype() in ['Ubuntu']:
                zoo_svc = 'zookeeper'
            run('service %s restart' % zoo_svc)

    for host_string in args:
        with  settings(host_string=host_string):
            run('service supervisord-contrail-database restart')

@task
@roles('openstack')
def restart_openstack():
    """Restarts the contrail openstack services."""
    execute('restart_openstack_node', env.host_string)

@task
def restart_openstack_node(*args):
    """Restarts the contrail openstack services in once openstack node. USAGE:fab restart_openstack_node:user@1.1.1.1,user@2.2.2.2"""
    openstack_services = ['rabbitmq-server', 'httpd', 'memcached', 'openstack-nova-api',
                          'openstack-nova-scheduler', 'openstack-nova-cert',
                          'openstack-nova-consoleauth', 'openstack-nova-novncproxy',
                          'openstack-nova-conductor', 'openstack-nova-compute']
    openstack_services = [ 'httpd', 'memcached', 'supervisor-openstack']
    if detect_ostype() in ['Ubuntu']:
        openstack_services = ['rabbitmq-server', 'memcached', 'nova-api',
                              'nova-scheduler', 'glance-api',
                              'glance-registry', 'keystone',
                              'nova-conductor', 'cinder-api', 'cinder-scheduler']
        openstack_services = ['memcached', 'supervisor-openstack']

    for host_string in args:
        with  settings(host_string=host_string):
            for svc in openstack_services:
                run('service %s restart' % svc)

@task
@roles('compute')
def restart_openstack_compute():
    """Restarts the contrail openstack compute service."""
    if detect_ostype() in ['Ubuntu']:
        run('service nova-compute restart')
        return
    run('service openstack-nova-compute restart')

@task
@parallel
@roles('cfgm')
def restart_cfgm():
    """Restarts the contrail config services."""
    execute("restart_cfgm_node", env.host_string)

@task
def restart_cfgm_node(*args):
    """Restarts the contrail config services in once cfgm node. USAGE:fab restart_cfgm_node:user@1.1.1.1,user@2.2.2.2"""
    for host_string in args:
        with  settings(host_string=host_string):
            run('service supervisor-config restart')

@task
@roles('control')
def restart_control():
    """Restarts the contrail control services."""
    execute("restart_control_node", env.host_string)

@task
def restart_control_node(*args):
    """Restarts the contrail control services in once control node. USAGE:fab restart_control_node:user@1.1.1.1,user@2.2.2.2"""
    for host_string in args:
        with  settings(host_string=host_string):
            run('service supervisor-control restart')

@task
@roles('collector')
def restart_collector():
    """Restarts the contrail collector services."""
    execute('restart_collector_node', env.host_string)

@task
def restart_collector_node(*args):
    """Restarts the contrail collector services in once collector node. USAGE:fab restart_collector_node:user@1.1.1.1,user@2.2.2.2"""
    for host_string in args:
        with  settings(host_string=host_string):
            run('service supervisor-analytics restart')

@task
@roles('compute')
def restart_vrouter():
    """Restarts the contrail compute services."""
    execute('restart_vrouter_node', env.host_string)

@task
def restart_vrouter_node(*args):
    """Restarts the contrail vrouter services in once vrouter node. USAGE:fab restart_vrouter_node:user@1.1.1.1,user@2.2.2.2"""
    for host_string in args:
        with  settings(host_string=host_string):
            run('service supervisor-vrouter restart')

@task
@roles('webui')
def restart_webui():
    """Restarts the contrail webui services."""
    execute('restart_webui_node', env.host_string)

@task
def restart_webui_node(*args):
    """Restarts the contrail webui services in once webui node. USAGE:fab restart_webui_node:user@1.1.1.1,user@2.2.2.2"""
    for host_string in args:
        with  settings(host_string=host_string):
            run('service supervisor-webui restart')

@task
@roles('build')
def stop_contrail_control_services():
    """stops the Contrail config,control,analytics,database,webui services."""
    execute('stop_cfgm')
    execute('stop_database')
    execute('stop_collector')
    execute('stop_control')
    execute('stop_webui')

@task
@roles('build')
def start_contrail_control_services():
    """Starts the Contrail config,control,analytics,database,webui services."""
    execute('start_cfgm')
    execute('start_database')
    execute('start_collector')
    execute('start_control')
    execute('start_webui')

@task
@roles('build')
def restart_contrail_control_services():
    """Restarts the Contrail config,control,analytics,database,webui services."""
    execute('restart_cfgm') 
    execute('restart_database')
    execute('restart_collector')
    execute('restart_control')
    execute('restart_webui')
