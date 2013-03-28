# Vim puppet class
class vim {
	package { ['vim', 'vim-nox'] :
		ensure => installed,
	   require => Exec['apt-key-update'],
	}

	package { 'ctags' :
		ensure => installed,
	   require => Exec['apt-key-update'],
	} 

	package { 'rake' :
		ensure => installed,
	   require => Exec['apt-key-update'],
	} 

	package { 'pep8' :
		ensure => installed,
	   require => Exec['apt-key-update'],
	} 

	# Ignore git files for bundles as git submodules:
	File { ignore => '.git' }

	file {'/usr/share/vim/vimcurrent/autoload':
		source => "puppet:///modules/vim/autoload",
		recurse => true,
		mode => 644,
		owner => root,
		group => root,
		require => File["/etc/vim/vimrc"],
	}

	file { 'vimrc' :
		path => '/etc/vim/vimrc',
		ensure => file,
		owner => root,
		group => root,
		require => Package['vim', 'vim-nox'],
		source => "puppet:///modules/vim/vimrc"
	}
}
