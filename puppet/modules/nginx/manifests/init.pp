# nginx class
class nginx {
    ##
    # Installation stuff
    ##
    package { "nginx_pkgs" :
		name => ['openssl', 'libpcre3-dev', 'libpcre3', 'zlib1g', 'zlib1g-dev'],
        ensure => installed,
		require => [Exec['apt-key-update'], Package['apache2']],
    }

	package { "nginx" :
		ensure => latest,
		require => Package["nginx_pkgs"],
	}

    service {'nginx' :
        ensure => running,
        require => Package['nginx'],
    }

    ##
    # site config files and scripts
    ##

    file { '/etc/nginx/nginx.conf':
        source => 'puppet:///modules/nginx/nginx.conf',
        owner => 'root',
        group => 'root',
        mode => 770,
        ensure => present,
        require => Package['nginx'],
    }

    # These are equivalent to a2ensite and a2dissite
    file { '/usr/local/bin/nginx_ensite':
        source => 'puppet:///modules/nginx/nginx_ensite',
        owner => 'root',
        group => 'root',
        mode => 770,
        ensure => present,
    }

    file { '/usr/local/bin/nginx_dissite':
        source => 'puppet:///modules/nginx/nginx_dissite',
        owner => 'root',
        group => 'root',
        mode => 770,
        ensure => present,
    }

    # site config file 
    # @TODO: move to a template
    file {'nginx_gourmethack':
        path => '/etc/nginx/sites-available/gourmethack',
        source => 'puppet:///modules/nginx/gourmethack',
        owner => 'root',
        group => 'root',
        mode => 640,
        ensure => present,
        require => Package['nginx'],
    }

    file {'sites-available':
        path => '/etc/nginx/sites-available',
        owner => 'root',
        group => 'root',
        mode => 640,
        ensure => directory,
        before => File['nginx_gourmethack'],
    }

    file {'sites-enabled':
        path => '/etc/nginx/sites-enabled',
        owner => 'root',
        group => 'root',
        mode => 640,
        ensure => directory,
        before => File['sites-available'],
    }

    exec {'nginx_ensite gourmethack':
        path => "$::path",
        cwd => '/',
        require => File['nginx_gourmethack', '/usr/local/bin/nginx_ensite', '/usr/local/bin/nginx_dissite'],
        unless => ["test -f /etc/nginx/sites-enabled/gourmethack"],
    }
}
