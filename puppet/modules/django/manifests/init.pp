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

    package { 'python-mock':
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

	exec { "pip install django-userena":
		cwd => '/',
			path => $path,
			user => 'root',
			group => 'root',
			require => [Package['python-pip'], Package['python-django']],
	}

	exec { "pip install django-denorm":
		cwd => '/',
			path => $path,
			user => 'root',
			group => 'root',
			require => [Package['python-pip'], Package['python-django']],
	}
}
