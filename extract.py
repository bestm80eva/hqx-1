import pprint, re

hqx_path = 'hqx-read-only/src'

k_to_pos = [(0,0), (1,0), (2,0),
            (0,1),        (2,1),
            (0,2), (1,2), (2,2)]

common_h = hqx_path + '/common.h'
interps_values = []
for line in open(common_h).readlines():
    if 'pc = Interp' in line:
        nums = [int(x) for x in re.findall('[^c_](\d+)', line)]
        coeffs, nbits = nums[:-1], nums[-1]
        interps_values.append((coeffs, nbits))

interp_def = {}
data = {}
for i in [2, 3, 4]:

    hqx_c = hqx_path + '/hq%dx.c' % i
    interp_defx = {}
    reset_cases = True
    rules = {}

    for line in open(hqx_c).readlines():
        line = line.strip()

        # Interpolations
        if line.startswith('#define PIXEL') and 'Interp' in line:
            m = re.match(r'.*PIXEL(\d+)_([^ ]+) +Interp(\d+)', line)
            dim, idx, interp = m.group(1, 2, 3)
            pos = [int(x) - 1 for x in re.findall('\[(\d+)\]', line)]
            interp_defx['%s_%s' % (dim, idx)] = (pos, int(interp) - 1)

        # Combinations
        elif line.startswith('case '):
            if reset_cases:
                cases = []
            mask = int(line[5:-1])
            cases.append(sorted([pos for k, pos in enumerate(k_to_pos) if mask & 1<<k]))
            reset_cases = False
            current_condition = None
        else:
            reset_cases = True
            if 'Diff(' in line:
                current_condition = tuple(int(x) - 1 for x in re.findall('\[(\d+)\]', line))
            elif 'else' in line:
                current_condition = None
            elif line.startswith('PIXEL'):
                pxid = line[5:] #.split('_', 1)
                pxrules = rules.get(pxid, {})
                condrules = pxrules.get(current_condition, [])
                condrules += cases
                pxrules[current_condition] = sorted(condrules)
                rules[pxid] = pxrules

    interp_def[i] = interp_defx
    data[i] = rules

open('data.py', 'w').write('''
interp_values = \\
%s

interp_def = \\
%s

combinations = \\
%s
''' % (
    pprint.pformat(interps_values),
    pprint.pformat(interp_def, width=200),
    pprint.pformat(data, width=200),
))
