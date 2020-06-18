#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


# Librerías
from collections import OrderedDict


class User:
    @staticmethod
    def get_ordered_options(user_options):
        """
        Returns user options as a list of ordered dictionaries.

        Keywords arguments:
        user_options -- user menu options
        """

        # Variables locales
        opts = []  # Lista de listas de tuplas

        for opt in user_options:
            # No tiene padre
            if opt['id_padre'] == 0:
                parent = []  # Lista de tuplas
                parent.append(('id', opt['id']))
                parent.append(('nombre', opt['nombre']))
                parent.append(('descripcion', opt['descripcion']))
                parent.append(('path', opt['path']))
                parent.append(('habilitada', opt['habilitada']))
                parent.append(('controlador', opt['controlador']))
                parent.append(('accion', opt['accion']))
                parent.append(('icono_clase_html', opt['icono_clase_html']))
                if 'id_opcion_menu_cliente' in opt:
                    parent.append((
                        'id_opcion_menu_cliente',
                        opt['id_opcion_menu_cliente']
                    ))

                # Sin hijos
                if opt['path'] != '':
                    parent.append(('abm', opt['abm']))
                    parent.append(
                        ('acceso', opt['acceso'] if 'acceso' in opt else 0)
                    )
                    if opt['abm'] == 1:
                        parent.append((
                            'alta',
                            opt['alta'] if 'alta' in opt else 0
                        ))
                        parent.append((
                            'modifica',
                            opt['modifica'] if 'modifica' in opt else 0
                        ))
                        parent.append((
                            'elimina',
                            opt['elimina'] if 'elimina' in opt else 0
                        ))
                        parent.append((
                            'recupera',
                            opt['recupera'] if 'recupera' in opt else 0
                        ))
                else:
                    # Con hijos, entonces buscar hijos
                    children = []  # Lista de listas de tuplas
                    for child_opt in user_options:
                        if child_opt['id_padre'] == opt['id']:
                            child = []  # Lista de tuplas
                            child.append(('id', child_opt['id']))
                            child.append(('nombre', child_opt['nombre']))
                            child.append(
                                ('descripcion', child_opt['descripcion'])
                            )
                            child.append(('path', child_opt['path']))
                            child.append(('abm', child_opt['abm']))
                            child.append((
                                'acceso',
                                child_opt['acceso'] if 'acceso' in child_opt
                                else 0
                            ))
                            child.append(
                                ('controlador', child_opt['controlador'])
                            )
                            child.append(('accion', child_opt['accion']))
                            child.append((
                                'icono_clase_html',
                                child_opt['icono_clase_html']
                            ))
                            if 'id_opcion_menu_cliente' in child_opt:
                                child.append((
                                    'id_opcion_menu_cliente',
                                    child_opt['id_opcion_menu_cliente']
                                ))
                            if child_opt['abm'] == 1:
                                child.append((
                                    'alta',
                                    child_opt['alta'] if 'alta' in child_opt
                                    else 0
                                ))
                                child.append((
                                    'modifica',
                                    child_opt['modifica'] if 'modifica' in child_opt
                                    else 0
                                ))
                                child.append((
                                    'elimina',
                                    child_opt['elimina'] if 'elimina' in child_opt
                                    else 0
                                ))
                                child.append((
                                    'recupera',
                                    child_opt['recupera'] if 'recupera' in child_opt
                                    else 0
                                ))
                            children.append(OrderedDict(child))
                    parent.append(('hijos', children))

                opts.append(OrderedDict(parent))

        return opts

    @staticmethod
    def get_user_channels(user_results_list):
        """
        Returns user channels as a list of ordered dictionaries.

        Keyword arguments:
        user_results_list -- results list of each channel for the user
        """

        # Variables locales
        channels = []  # Lista de listas de tuplas

        for result in user_results_list:
            parent = []  # Lista de tuplas
            parent.append(('id', result['M.id']))
            parent.append(('descripcion', result['descripcion']))

            channels.append(OrderedDict(parent))

        return channels

    @staticmethod
    def get_users_list(users_results_list):
        """
        Returns client's users as a list of ordered dictionaries.

        Keyword arguments:
        users_results_list -- resutls list of each user for the client
        """

        # Variables locales
        users = []  # Lista de listas de tuplas

        for user in users_results_list:
            new_user = []  # Lista de tuplas
            new_user.append(('id', user['id']))
            new_user.append(('id_cliente', user['id_cliente']))
            new_user.append(('nombre', user['nombre']))
            new_user.append(('email', user['email']))

            users.append(OrderedDict(new_user))

        return users
