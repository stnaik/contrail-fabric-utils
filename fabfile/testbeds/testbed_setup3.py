from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.84.15.1'
host2 = 'root@10.84.15.2'
host3 = 'root@10.84.15.3'
host4 = 'root@10.84.15.4'
host5 = 'root@10.84.15.5'

ext_routers = [('mx1', '10.84.15.252'), ('mx2', '10.84.15.253')]
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.43.0/24"

host_build = 'rajreddy@10.84.5.112'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5],
    'openstack': [host1],
    'cfgm': [host1, host2],
    'control': [host1, host2],
    'compute': [host4, host5],
    'collector': [host1, host2],
    'webui': [host1],
    'database': [host1, host2, host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['a3s3', 'a3s4', 'a3s5','a3s6', 'a3s7']
}


env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',

    host_build: 'rajreddy123',
}

env.ostypes = {
    host1: 'centos',
    host2: 'centos',
    host3: 'centos',
    host4: 'centos',
    host5: 'centos',
}

env.test_repo_dir='/users/rajreddy/test/mainline/contrail-test'
