# Does some initialization
class init_server {
    exec { 'apt-key-update' :
        command => 'apt-key update && apt-key add /tmp/nginx_signing.key && apt-get update',
		cwd => '/',
		path => '/usr/bin:/bin',
		user => 'root',
		group => 'root',
		require => Package['python-software-properties', 'mktemp'],
    }

	exec {'add_rep_2':
		command => 'add-apt-repository ppa:nginx/stable',
		cwd => '/',
		path => '/usr/bin',
		user => 'root',
		group => 'root',
		require => Package['python-software-properties'],
		before => Exec['apt-key-update'],
	}

    file_line {'deb-add':
        path => '/etc/apt/sources.list',
        line => "deb http://nginx.org/packages/ubuntu/ $lsbdistcodename nginx",
		before => Exec['apt-key-update'],
    }

    file_line {'deb-src-add':
        path => '/etc/apt/sources.list',
        line => "deb-src http://nginx.org/packages/ubuntu/ ${lsbdistcodename} nginx",
        require => File_line['deb-add'],
		before => Exec['apt-key-update'],
    }

	file { '/var/lib/puppet/log' :
		ensure => 'directory',
		before => Exec['apt-key-update'],
	}

    file { '/tmp/nginx_signing.key':
		source => "puppet:///modules/init_server/nginx_signing.key",
		before => Exec['apt-key-update'],
    }
	
	package { 'python-software-properties' :
		ensure => latest,
	}

	package { 'mktemp' :
		ensure => latest,
	}

	package { 'curl' :
		ensure => latest,
	}

	#dotfiles
	init_server::dotfile{'bash.bashrc': }

	init_server::dotfile{'aliases': }

	init_server::dotfile{'bash_prompt': }

	init_server::dotfile{'inputrc': }

	init_server::dotfile{'functions': }

	init_server::dotfile{'exports': }

	init_server::local_dotfile{'.bashrc': }
}
