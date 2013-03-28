# Django puppet class
class django {
    package { 'python-django' :
        ensure => 'latest',
        require => [Exec['apt-key-update'], Package['python']],
    }
	
	package { 'python-django-south' :
		ensure => installed,
		require => Package['python-django'],
	}
}
