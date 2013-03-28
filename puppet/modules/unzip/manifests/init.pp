# unzip module

class unzip {
	package { 'unzip':
		ensure => installed,
		require => Exec['apt-key-update'],
	}
}
