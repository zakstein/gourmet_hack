# Python puppet class
class python {
    package { 'python':
        ensure => 'latest',
		require => Exec['apt-key-update'],
    }

	package { 'python-gdata':
		ensure => 'latest',
		require => Exec['apt-key-update'],
	}

	package { 'pyflakes':
		ensure => 'latest',
		require => Exec['apt-key-update'],
	}

    package {'python-imaging':
        ensure => 'latest',
        require => Package['python'],
    }

    package { 'python-pip':
        ensure => 'latest',
        require => Package['python'],
    }

    file { '/tmp/xlrd':
                source => "puppet:///modules/python/xlrd",
        ensure => 'present',
        recurse => true,
        require => Package['python'],
    }

    exec {'python setup.py install':
                cwd => '/tmp/xlrd',
                path => $path,
                user => 'root',
                group => 'root',
        require => Package['python'],
    }
}
