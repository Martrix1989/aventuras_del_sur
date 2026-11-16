from cuentas.decorators import roles_permitidos

solo_administrador = roles_permitidos("admin")
administrador_o_guia = roles_permitidos("admin", "guia")
solo_turista = roles_permitidos("turista")
