# Apache puppet class
class apache2 {
	package { 'apache2':
		ensure => installed,
		require => Exec['apt-key-update'],
	}

	service { 'apache2':
		name => 'apache2',
		ensure => running,
		enable => true,
        require => File['/etc/apache2/ports.conf'],
	}

    file { '/etc/apache2/ports.conf':
        source => 'puppet:///modules/apache2/ports.conf',
        owner => 'root',
        group => 'root',
        mode => 644,
        ensure => present,
        notify => Service['apache2'],
        require => Package['apache2'],
        before => Package['nginx'],
    }
}
