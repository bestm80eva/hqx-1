import cairo, sys

DOTSIZE  = 10
DOTSPACE = 5
TBLSPACE = 15
MARGINX = MARGINY = 10
WPOS = [(0,0), (1,0), (2,0),
        (0,1), (1,1), (2,1),
        (0,2), (1,2), (2,2)]

tbl_x = lambda i: i*(DOTSIZE + DOTSPACE)
tbl_y = lambda j: j*(DOTSIZE + DOTSPACE)

def draw_tbl(x, y, sz, interp=None):
    for j in range(sz):
        for i in range(sz):
            if interp and (i, j) in interp:
                cr.set_source_rgb(1, 1, 1)
            else:
                cr.set_source_rgb(0.4, 0.4, 0.4)
            cr.rectangle(x + tbl_x(i), y + tbl_y(j), DOTSIZE, DOTSIZE)
            cr.fill()

    if interp:
        cr.set_line_width(2)
        cr.set_source_rgb(1, 0, 0)

        i, j = interp[0]
        cr.move_to(x + tbl_x(i) + DOTSIZE/2,
                   y + tbl_y(j) + DOTSIZE/2)
        for i, j in interp[1:]:
            cr.line_to(x + tbl_x(i) + DOTSIZE/2,
                       y + tbl_y(j) + DOTSIZE/2)
        cr.close_path()
        if len(interp) > 2:
            cr.fill()
        else:
            cr.stroke()

def draw_tbl2(x, y, sz, required_dots, conditionnal_diff):
    for j in range(sz):
        for i in range(sz):
            if (i, j) in required_dots:
                cr.set_source_rgb(1, 0, 0)
            else:
                cr.set_source_rgb(0.4, 0.4, 0.4)
            cr.rectangle(x + tbl_x(i), y + tbl_y(j), DOTSIZE, DOTSIZE)
            cr.fill()

    if conditionnal_diff:
        cr.set_line_width(2)
        cr.set_source_rgb(0, 1, 0)

        pt0, pt1 = conditionnal_diff
        cr.move_to(x + tbl_x(pt0 % 3) + DOTSIZE/2,
                   y + tbl_y(pt0 / 3) + DOTSIZE/2)
        cr.line_to(x + tbl_x(pt1 % 3) + DOTSIZE/2,
                   y + tbl_y(pt1 / 3) + DOTSIZE/2)
        cr.close_path()
        cr.stroke()

if __name__ == '__main__':

    dim = int(sys.argv[1])
    SZ = 3
    STEP = SZ*DOTSIZE + (SZ-1)*DOTSPACE + TBLSPACE

    if len(sys.argv) > 2:
        import rules

        interpid = sys.argv[2]

        max_nb_w = 15

        total = 0
        for cond, permuts in rules.data[dim][interpid].items():
            total += len(permuts)
        nb_w = min(total, max_nb_w)
        nb_h = total / nb_w + (1 if total % nb_w else 0)
        w = 2*MARGINX + nb_w*SZ*DOTSIZE + nb_w*(SZ-1)*DOTSPACE + (nb_w-1)*TBLSPACE
        h = 2*MARGINY + nb_h*SZ*DOTSIZE + nb_h*(SZ-1)*DOTSPACE + (nb_h-1)*TBLSPACE

        s = cairo.SVGSurface(None, w, h)
        cr = cairo.Context(s)
        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        n = 0
        x, y = MARGINX, MARGINY
        for cond, permuts in rules.data[dim][interpid].items():
            for dots in permuts:
                draw_tbl2(x, y, SZ, dots, cond)
                n += 1
                if n == max_nb_w:
                    x = MARGINX
                    y += STEP
                    n = 0
                else:
                    x += STEP

        s.write_to_png('hqx%d-%s.png' % (dim, interpid))

    else:
        import data

        nb_w, nb_h = 0, 0
        for pack_id, interp_pack in data.interp_def[dim - 2]:
            nb_w = max(nb_w, len(interp_pack))
            nb_h += 1
        w = 2*MARGINX + nb_w*SZ*DOTSIZE + nb_w*(SZ-1)*DOTSPACE + (nb_w-1)*TBLSPACE
        h = 2*MARGINY + nb_h*SZ*DOTSIZE + nb_h*(SZ-1)*DOTSPACE + (nb_h-1)*TBLSPACE

        s = cairo.SVGSurface(None, w, h)
        cr = cairo.Context(s)
        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        y = MARGINY
        for pack_id, interp_pack in data.interp_def[dim - 2]:
            x = MARGINX
            for idx, pos in interp_pack:
                interp = [WPOS[p] for p in pos]
                draw_tbl(x, y, SZ, interp)
                x += STEP
            y += STEP

        s.write_to_png('hqx%d.png' % dim)