# Automatic dotfile stuff

define init_server::dotfile()
{
	file {"/etc/$name":
		source => "puppet:///modules/init_server/$name",
		ensure => present,
		owner => root,
		mode => 644,
	}
}
