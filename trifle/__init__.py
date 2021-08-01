import matplotlib.pyplot as plt


def _get_ax_ratio(ax):
    _, _, w, h = _get_ax_pos_inch_coords(ax)
    return w / h


def _get_fig_ratio(fig):
    figsizex, figsizey = fig.get_size_inches()
    return figsizex / figsizey


def _get_ax_pos_fig_coords(ax):
    pos = ax.get_position()
    return pos.xmin, pos.ymin, pos.width, pos.height


def _get_ax_pos_inch_coords(ax):
    pos = ax.get_position()
    figsizex, figsizey = ax.figure.get_size_inches()
    return pos.xmin * figsizex, pos.ymin * figsizey, pos.width * figsizex, pos.height * figsizey


def get_target_pos(source_ax, target_box, va="top"):
    source_fig = source_ax.figure
    target_fig = target_box.figure

    source_f_ratio = _get_fig_ratio(source_fig)
    target_f_ratio = _get_fig_ratio(target_fig)
    target_ratio = _get_ax_ratio(target_box)
    source_ratio = _get_ax_ratio(source_ax)

    ax_xoff, ax_yoff, ax_w, ax_h = _get_ax_pos_fig_coords(source_ax)
    box_xoff, box_yoff, box_w, box_h = _get_ax_pos_fig_coords(target_box)

    if target_ratio < source_ratio:
        panel_w = box_w
        panel_h = panel_w / (source_f_ratio / target_f_ratio)
    else:
        panel_h = box_h
        panel_w = panel_h * (source_f_ratio / target_f_ratio)

    if va == "top":
        ypos = box_yoff + box_h - (1 - ax_yoff) * panel_h
    else:
        ypos = box_yoff + panel_h * ax_yoff

    return box_xoff + panel_w * ax_xoff, ypos, panel_w * ax_w, panel_h * ax_h


def move_axes(ax, target_box_axes):
    """Transfer axes from one figure inside a bounding box defined by axes on another
    figure.
    """
    target_pos = get_target_pos(ax, target_box_axes)

    fig = target_box_axes.figure
    ax.remove()
    ax.figure = fig  # set reference to new fig
    fig.add_axes(ax)  # add axes to current axes

    # Change transformation of axes BBox to target figure transformation, otherwise
    # scaling will be done with respect to old image sizes
    ax.bbox._transform._mtx = target_box_axes.bbox._transform._mtx
    ax.set_position(target_pos)


def transfer_figure_in_box(fig, target_box_ax, remove_target_box=True):
    for ax in fig.get_axes():
        move_axes(ax, target_box_ax)
    plt.close(fig)

    if remove_target_box:
        target_box_ax.remove()


def compose_figure(flist, fig_width=8):
    # Calculate cumulative ratios for each row:
    cumulative_ratios = [sum([_get_fig_ratio(f) for f in frow]) for frow in flist]

    # Derive image height from individual widths:
    heights = [fig_width / cum_ratio for cum_ratio in cumulative_ratios]
    fig_height = sum(heights)

    # Create assembled figure axes looping over figures
    cum_fig = plt.figure(figsize=(fig_width, fig_height))
    yo = 1

    axes = []
    for frow, cumulative_ratio, height in zip(flist, cumulative_ratios, heights):
        xo = 0
        h = height / fig_height
        yo -= h
        axes_row = []
        for f in frow:
            print(f)
            w = _get_fig_ratio(f) / cumulative_ratio
            new_ax = cum_fig.add_axes((xo, yo, w, h))
            axes_row.append(new_ax)
            xo += w

        axes.append(axes_row)

    plt.gcf().canvas.draw()

    return cum_fig, axes


def transfer_fig_list(flist, axes, fig_width=8, remove_target_box=True):
    # cum_fig, axes = compose_figure(flist, fig_width=fig_width)

    for axrow, frow in zip(axes, flist):
        for ax, fig in zip(axrow, frow):
            transfer_figure_in_box(fig, ax, remove_target_box=remove_target_box)

    # return cum_fig


def compose_and_transfer(flist, fig_width=8, remove_target_box=True):
    cum_fig, axes = compose_figure(flist, fig_width=fig_width)

    for axrow, frow in zip(axes, flist):
        for ax, fig in zip(axrow, frow):
            transfer_figure_in_box(fig, ax, remove_target_box=remove_target_box)

    return cum_fig