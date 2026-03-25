from typing import Dict, Any


def get_config(config_file: str) -> Dict[str, Any] | None:
    config: Dict[Any, Any] = dict()
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            line = line.rstrip('\n')
            current = line.split(sep='=')
            if len(current) != 2:
                err = 'Invalid config file. All lines must be <KEY>=<VALUE>.'
                raise ValueError(err)
            config[current[0]] = current[1]
    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    if not all(key in config for key in mandatory):
        ret_error = 'Missing mandatory entries in the config file. '
        ret_error += f'Mandatory entries: {mandatory}'
        raise ValueError(ret_error)
    config['WIDTH'] = int(config['WIDTH'])
    config['HEIGHT'] = int(config['HEIGHT'])
    entry = config['ENTRY'].split(sep=',')
    exit = config['EXIT'].split(sep=',')
    if len(entry) == 2 and len(exit) == 2:
        config['ENTRY'] = [int(entry[0]), int(entry[1])]
        config['EXIT'] = [int(exit[0]), int(exit[1])]
    else:
        raise ValueError("Entry and exit must be like '<x_coor>,<y_coor>")
    if config['PERFECT'] == 'True':
        config['PERFECT'] = True
    elif config['PERFECT'] == 'False':
        config['PERFECT'] = False
    else:
        raise ValueError("PERFECT must be 'True' or 'False'")
    if 'SEED' in config:
        if config['SEED'] == 'None':
            config['SEED'] = None
        else:
            try:
                int(config['SEED'])
            except ValueError:
                raise ValueError('Seed must be an int or None.')
            config['SEED'] = int(config['SEED'])
    return config
