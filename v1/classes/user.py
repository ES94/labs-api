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
                parent.append(('descripcion', opt['descripcion']))
                parent.append(('path', opt['path']))

                # Sin hijos
                if opt['path'] != '':
                    parent.append(('abm', opt['abm']))
                    parent.append(('habilitada', opt['habilitada']))
                    parent.append(('acceso', opt['acceso']))
                    if opt['abm'] == 1:
                        parent.append(('alta', opt['alta']))
                        parent.append(('baja', opt['baja']))
                        parent.append(('modifica', opt['modifica']))
                        parent.append(('elimina', opt['elimina']))
                else:
                    # Con hijos, entonces buscar hijos
                    children = []  # Lista de listas de tuplas
                    for child_opt in user_options:
                        if child_opt['id_padre'] == opt['id']:
                            child = []  # Lista de tuplas
                            child.append(('id', child_opt['id']))
                            child.append(
                                ('descripcion', child_opt['descripcion'])
                            )
                            child.append(('path', child_opt['path']))
                            child.append(('abm', child_opt['abm']))
                            parent.append(('habilitada', opt['habilitada']))
                            child.append(('acceso', child_opt['acceso']))
                            if opt['abm'] == 1:
                                parent.append(('alta', opt['alta']))
                                parent.append(('baja', opt['baja']))
                                parent.append(('modifica', opt['modifica']))
                                parent.append(('elimina', opt['elimina']))
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