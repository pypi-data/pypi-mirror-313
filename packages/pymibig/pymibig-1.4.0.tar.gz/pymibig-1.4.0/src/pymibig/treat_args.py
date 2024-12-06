"""
Treat all arguments passed by the user.
"""

def treat_args(data, args) -> bool:
    '''
    Lower all user inputs an compare to lowered metadata. Evaluate the
    presence of an argument and include it in treatment

    Arguments:
    data -- MIBiG metadata from json files
    args -- object of class Args containing user inputs
    '''

    add: bool = True

    if args.organism:
        add &= (
            args.organism.lower() in data['taxonomy']['name'].lower()
            )
    if args.product:
        add &= args.product.lower() in [
            c.get('name').lower() for c in data['compounds']
            ]
    if args.biosynt:
        add &= args.biosynt.lower() in [
            b.get('class').lower() for b in data['biosynthesis']['classes']
            ]
    if args.completeness != 'all':
        add &= (
            data['completeness'].lower()
            == args.completeness.lower()
            )
    if args.quality != 'all':
        add &= (
            data['quality'].lower() == args.quality.lower()
            )

    return add
