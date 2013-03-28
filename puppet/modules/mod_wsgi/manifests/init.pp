# puppet class
class mod_wsgi {
    package {'libapache2-mod-wsgi' :
        ensure => latest,
        require => Package['apache2'],
    }

    file { '/etc/apache2/sites-available/gourmethack':
        source => 'puppet:///modules/mod_wsgi/gourmethack',
        owner => 'root',
        group => 'root',
        mode => '644',
        ensure => present,
        notify => Service['apache2'], # restart apache2 when we change this file
        require => Package['libapache2-mod-wsgi'],
    }

    exec { '/usr/sbin/a2dissite 000-default && /usr/sbin/a2ensite gourmethack && /etc/init.d/apache2 reload' :
        cwd => '/',
        user => 'root',
        require => Service['apache2'],
    }
}
