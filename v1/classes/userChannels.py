#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


# Librerías
from collections import OrderedDict


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