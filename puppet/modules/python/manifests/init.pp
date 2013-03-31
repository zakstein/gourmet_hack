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
}
