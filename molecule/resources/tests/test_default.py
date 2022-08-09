import os
import pytest
from time import sleep, time
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


OMERO = '/opt/omero/server/OMERO.server/bin/omero'


def test_db_running_and_enabled(host):
    if host.system_info.distribution == 'ubuntu':
        service = host.service('postgresql@11-main')
    else:
        service = host.service('postgresql-13')
    assert service.is_running
    assert service.is_enabled


def test_srv_running_and_enabled(host):
    service = host.service('omero-server')
    assert service.is_running
    assert service.is_enabled


def test_omero_login(host):
    # Ubuntu sudo doesn't set HOME so it tries to write to /root
    env = 'OMERO_USERDIR=/tmp/omero-{}'.format(time())
    with host.sudo('omero-server'):
        host.check_output(
            '%s %s login -C -s localhost -u root -w ChangeMe' % (env, OMERO))


@pytest.mark.parametrize('name', ['omero-web', 'nginx'])
def test_services_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled


def test_omero_web_first_page(host):
    out = host.check_output('curl -fsL http://localhost/')
    assert 'omero:4064' in out


def get_cookie(cookietxt, name):
    for line in cookietxt.splitlines():
        tokens = line.split()
        try:
            if tokens[5] == name:
                return tokens[6]
        except IndexError:
            pass


# https://github.com/openmicroscopy/omero-grid-docker/blob/0.1.0/test_login.sh
def test_omero_web_login(host):
    LOGIN_URL = 'http://localhost/webclient/login/'
    CURL = 'curl -f -i -k -s -c cookies.txt -b cookies.txt -e %s' % LOGIN_URL

    for i in range(60):
        sleep(2)
        host.check_output('%s %s' % (CURL, LOGIN_URL))
        csrf = get_cookie(host.file('cookies.txt').content_string, 'csrftoken')
        if csrf:
            break
    assert csrf

    data = '&'.join([
        'csrfmiddlewaretoken=%s' % csrf,
        'username=root',
        'password=ChangeMe',
        'server=1',
        'url=%2Fwebclient%2F',
        ])

    for i in range(60):
        sleep(2)
        host.check_output('%s -d "%s" -X POST %s' % (
            CURL, data, LOGIN_URL))
        sessionid = get_cookie(
            host.file('cookies.txt').content_string, 'sessionid')
        if sessionid:
            break
    assert sessionid
