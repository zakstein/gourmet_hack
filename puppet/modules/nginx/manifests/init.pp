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

    # site config file 
    # @TODO: move to a template
    file {'nginx_gourmethack':
        path => '/etc/nginx/conf.d/gourmethack.conf',
        source => 'puppet:///modules/nginx/gourmethack.conf',
        owner => 'root',
        group => 'root',
        mode => 640,
        ensure => present,
        require => Package['nginx'],
    }
}
