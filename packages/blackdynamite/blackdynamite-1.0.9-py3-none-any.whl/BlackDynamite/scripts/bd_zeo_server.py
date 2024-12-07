#!/usr/bin/env python

import BlackDynamite as BD


def main(argv=None):
    parser = BD.bdparser.BDParser()
    group = parser.register_group('server')
    group.add_argument("--action", type=str,
                       choices=['stop', 'start', 'status'],
                       help="Can be start stop or status",
                       default='status')

    params = parser.parseBDParameters(argv)
    base = BD.base.Base(**params)
    if params['action'] == 'stop':
        base.stopZdaemon()
    elif params['action'] == 'status':
        base.statusZdaemon()
    elif params['action'] == 'start':
        print('Server started')
        base.statusZdaemon()


if __name__ == "__main__":
    main()
