import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

from azureml.core.run import Run, _OfflineRun

FONT_SIZE_S = 15
FONT_SIZE_M = 25
FONT_SIZE_L = 35
CM_TITLE = 'Confusion Matrix'
CM_XLABEL = 'Predicted Class'
CM_YLABEL = 'Actual Class'
MAX_DISPLAY_LABEL_LENGTH = 10


def format_display_label(display_labels):
    final_display_labels = []
    for label in display_labels:
        final_display_labels.append(
            label if len(label) <= MAX_DISPLAY_LABEL_LENGTH else
            f'{label[0: MAX_DISPLAY_LABEL_LENGTH]}...')

    return final_display_labels


def plot_confusion_matrix(confusion_matrix,
                          display_labels,
                          plot_name,
                          cmap='Blues',
                          format='%.2g'):
    # To avoid large size plot figure, limit display label name max length to 10,
    # will add '...' as postfix if length exceeds.
    display_labels = format_display_label(display_labels)
    n_classes = confusion_matrix.shape[0]
    # set 10 as size lower bound to get pretty plot if n_classes is small.
    size = max(10, n_classes)
    figsize = [size, size]
    fig, ax = get_new_fig(plot_name, figsize)
    cm = pd.DataFrame(confusion_matrix,
                      index=display_labels,
                      columns=display_labels)
    # thanks for seaborn
    ax = sn.heatmap(cm,
                    annot=True,
                    annot_kws={"size": FONT_SIZE_S},
                    linewidths=0.5,
                    ax=ax,
                    cbar=False,
                    cmap=cmap,
                    linecolor='w',
                    fmt='.1%')
    # set ticklabels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=FONT_SIZE_M)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=FONT_SIZE_M)
    # set colorbar
    im_ = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    # set colorbar size to match graph by these fraction and pad value
    cbar = fig.colorbar(im_,
                        ax=ax,
                        fraction=0.012,
                        pad=0.02,
                        aspect=80,
                        format=format)
    cbar.ax.tick_params(labelsize=FONT_SIZE_S)
    # set title
    ax.set_title(CM_TITLE, fontsize=FONT_SIZE_L)
    # set axis label
    ax.set_xlabel(CM_XLABEL, fontsize=FONT_SIZE_M)
    ax.set_ylabel(CM_YLABEL, fontsize=FONT_SIZE_M)
    plt.tight_layout()
    # log plot in run record
    run = Run.get_context()
    run.log_image(plot_name, plot=plt)
    if type(run) == _OfflineRun:
        plt.savefig(f'{plot_name}.png')

    plt.close('all')


def get_new_fig(fn, figsize=[9, 9]):
    fig = plt.figure(fn, figsize, dpi=40)
    # get current axis
    ax = fig.gca()
    # clear existing plot
    ax.cla()
    return fig, ax
