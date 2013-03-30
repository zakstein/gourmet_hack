# Django puppet class
class django {
    package { 'python-django' :
        ensure => 'latest',
        require => [Exec['apt-key-update'], Package['python']],
    }
	
    package { 'python-jinja2':
		ensure => installed,
		require => Package['python-django'],
    }

	package { 'python-psycopg2' :
		ensure => installed,
		require => Package['python-django'],
	}

	package { 'python-django-registration' :
		ensure => installed,
		require => Package['python-django'],
	}

	package { 'python-django-south' :
		ensure => installed,
		require => Package['python-django'],
	}
}
