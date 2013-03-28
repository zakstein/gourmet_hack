# Git puppet class
class git {
    package { 'git':
        ensure => installed,
		require => Exec['apt-key-update'],
    }

	file { '/etc/gitconfig':
		source => 'puppet:///modules/git/gitconfig',
		ensure => present,
		owner => root,
		mode => 644,
	}
}
