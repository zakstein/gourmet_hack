# Dev node
node precise32 {

	# Dev stuff
    include stdlib
    include nginx
	include unzip
	include apache2
	include vim
    include mod_wsgi
    include django
    include python
    include git

	# Common stuff
    include init_server
	# include shorewall

	# mail stuff
	# include postfix

    # DB stuff (to be moved to another machine at some point

    include postgresql::server

    postgresql::db {'gourmet':
        user => 'vagrant',
        password => '3atingmakesyouf4t',
    }

}
