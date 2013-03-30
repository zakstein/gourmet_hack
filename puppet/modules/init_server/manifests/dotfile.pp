# Automatic dotfile stuff

define init_server::dotfile()
{
	file {"/etc/$name":
		source => "puppet:///modules/init_server/$name",
		ensure => present,
		owner => root,
		group => root,
		mode => 644,
	}
}

define init_server::local_dotfile()
{
    file {"/home/vagrant/$name":
		source => "puppet:///modules/init_server/$name",
		ensure => present,
		owner => vagrant,
		group => vagrant,
		mode => 644,
    }
}
