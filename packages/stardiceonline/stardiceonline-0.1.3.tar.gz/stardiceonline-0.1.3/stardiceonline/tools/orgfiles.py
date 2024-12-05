import numpy as np
import re


def convert(value):
    ''' Attemps to convert values to numerical types
    '''
    value = value.strip()
    if not value:
        value = "nan"
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    return value

def fromorg(filename):
    ''' Read a table in emacs org-mode format
    '''
    with open(filename, "r") as fh:
        lines = fh.readlines()

    d_key = {}
    names = []
    records = []
    first = True        
    header_expr = re.compile(':\s*(.+)\s*:\s*(.+)\s*')
        
    for i, line in enumerate(lines):
        if line.startswith(':'):
            try:
                key, val = header_expr.match(line).groups()
            except:
                raise ValueError('Line not understood : ' + line)
       
            val = convert(val)
       
            d_key[key] = val
        if line.startswith('|-'):
            continue
        if line.startswith('|'):
            vals = line.split('|')[1:-1]
            if first:
                names = [v.strip() for v in vals]
                first = False
            else:
                records.append([convert(v) for v in vals])

    nt = np.rec.fromrecords(records, names=names)
    return nt, d_key

def toorg(nt, filename='', keys={}):
    """
    Write the tuple to a .org file. 

    Parameters
    ----------
      - filename [str]: output file name 
                        if None, write to stdout instead

    """
    if filename is None:
        import sys
        fh = sys.stdout
    else:
        fh = open(filename, 'w')
        
    # global keys 
    for key, value in keys.items():
        print(":%s: %s" % (key, str(value)), file=fh)
    
    # header 
    ncols = len(nt.dtype.names)
    line_sep = "|" + "-+"*(ncols-1) + "-|"
    print(line_sep, file=fh) 
    s = "| "
    for key in nt.dtype.names:
        s += key ; s += " | "
    print(s, file=fh)
    print(line_sep, file=fh)
    
    # data 
    tmp_line = ""
    for t_line in nt:
        for name in nt.dtype.names:
            tmp_line += '| %-s ' % (str(t_line[name]))
        tmp_line += '\n'
    print(tmp_line[:-1], file=fh)
    print(line_sep, file=fh) 
