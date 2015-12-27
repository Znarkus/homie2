config = {
    'transmitters': [
        {'house': 15323014, 'unit': 11}
    ]
}

lamps = {
    'taklampor': core.add_device("Taklampor", "arctech", "selflearning-dimmer", house=13, unit=1, id=1),
    'byra': core.add_device("Byrå", "arctech", "selflearning-dimmer", house=21079520, unit=1, id=2),
    'bordslampor': core.add_device("Bordslampor", "arctech", "selflearning-switch", house=12345, unit=11, id=3)
}
