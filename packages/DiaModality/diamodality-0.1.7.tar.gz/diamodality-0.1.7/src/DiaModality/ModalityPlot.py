#!/usr/bin/env python
import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import numpy as np

# Only use for plot layout adjustment
DEBUG = False


class __Figure():
    '''
        Super class of all future plots
    '''

    def __init__(
        self,
        marker='',
        linestyle='-',
        linewidth=0.5,
        alpha=0.8,
        figsize=(10, 10),
        title='',
    ) -> None:

        self.marker = marker
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.alpha = alpha
        self.figsize = figsize
        self.title = title
        self.debug_flag = DEBUG

        # Prepare figure:
        self.fig = plt.figure(figsize=self.figsize)
        self._make_layout()

    def _make_layout(self) -> None:
        # Create figure
        plt.subplots_adjust(wspace=0.0, hspace=0.0)
        plt.tight_layout()
        plt.suptitle(self.title)


class __Output():
    '''
        Output options mixin
    '''

    def show(self):
        plt.show()

    def save(self,
             filename,
             type='png',
             transparent=False):
        plt.savefig('{}.{}'.format(filename, type), transparent=transparent)


class ModalityPlot(__Figure, __Output):
    '''
        Input fotmat:

        data: list of points, each point should be represented as a
              list or touple containing three floats, one per modality.

    '''

    def __init__(
        self,
        data: list,
        binarization: list,
        modalities=('Set A', 'Set B', 'Set C'),
        angles=[90, 210, 330],
        labels=True,
        scalecircle=1,             # Scale circle radius
        scalecircle_linestyle=':',
        scalecircle_linewidth=1,
        marker='',                 # vector endpoints marker
        linestyle='-',
        linewidth=0.5,
        alpha=0.8,
        same_scale=False,          # Draw all the subplots in the same scale
        # Draw all vectors in the central subplot, else draw trimodal vectors only
        full_center=True,
        whole_sum=True,            # Calculate all three modality vectors despite binarization
        figsize=(10, 10),
        title='',
        colors=(
            'tab:green',           # Set 1 color
            'navy',                # Set 2 color
            'tab:red',             # Set 3 color
            '#1E88E5',             # Sets 1 & 2 intersection color
            '#FF9933',             # Sets 1 & 3 intersection color
            '#9900FF',             # Sets 2 & 3 intersection color
            'black',               # All sets   intersection color
        ),
        normalization_func='sigmoid',
    ) -> None:

        self.data, self.binarization = self.__format_input(data, binarization)
        self.modalities = modalities
        self.angles = np.deg2rad(angles)
        self.labels = labels
        self.scalecircle = scalecircle
        self.scalecircle_linestyle = scalecircle_linestyle
        self.scalecircle_linewidth = scalecircle_linewidth
        self.same_scale = same_scale
        self.full_center = full_center
        self.whole_sum = whole_sum
        self.colors = colors
        self.normalization_func = normalization_func
        self.modality_patterns = (
            (True, False, False),
            (False, True, False),
            (False, False, True),
            (True, True, False),
            (True, False, True),
            (False, True, True),
            (True, True, True),
        )
        self.modalities_array = (
            (self.modalities[0], None, None),
            (None, self.modalities[1], None),
            (None, None, self.modalities[2]),
            (self.modalities[0], self.modalities[1], None),
            (self.modalities[0], None, self.modalities[2]),
            (None, self.modalities[1], self.modalities[2]),
            (None, None, None),
        )

        super().__init__(
            marker,
            linestyle,
            linewidth,
            alpha,
            figsize,
            title,
        )

        # check input:
        assert self.data.any(), 'data array must not be empty'
        assert self.binarization.any(), 'binarization array must not be empty'
        assert len(self.data) == len(
            self.binarization), 'data and binarization arrays must have exact length'
        assert len(self.data[0]) == len(self.binarization[0]
                                        ) == 3, 'data and binarization arrays must have three columns each'

    def __format_input(self, input_data, input_bin) -> list:
        '''
            Data formatting:
            Each column represents one modality. Empty cells are counted as 0.
            Each row containing at least one value that will be represented as a point.
        '''

        output_data = np.array(input_data, dtype=object)
        # Replace empty cells with zeros
        output_data[output_data is None] = 0
        output_data = output_data.astype(np.float32)

        # Replace zeros with False and other numbers with True
        output_bin = np.array(input_bin, dtype=np.bool_)

        return output_data, output_bin

    def __normalization(self, input) -> list:
        '''
            Define function to normalize coordinates
            to values in range of 0 to 1 for HSV color model.
            input: np.array
        '''

        match self.normalization_func:

            case 'linear':
                def func(x): return (x - np.min(input)) / \
                    (np.max(input) - np.min(input))

            case 'sigmoid':
                def func(x): return 1 / (1 + np.exp(-x))

            # case 'log':
            #     log_input = np.log1p(input)
            #     func = lambda x: (x - np.min(log_input)) / (np.max(log_input) - np.min(log_input))

        return [func(x) for x in input]

    def __vector_addition(self, data, binarization) -> list:

        resultants = np.array((), dtype=np.float32)

        for points, bins in zip(data, binarization):

            # ignore empty lines
            if not all(x == 0 for x in points):

                # Calculate resultant vector
                resultants = np.append(
                    resultants,
                    np.sum(
                        [points[i] * np.exp(1j * self.angles[i])
                            if bins[i] or self.whole_sum
                            else 0
                            for i in range(len(points))
                         ]
                    )
                )
            else:
                resultants = np.append(resultants, (0))

        return resultants

    def __find_match_modality(self, sample, list) -> int:
        for i, item in enumerate(list):
            if np.array_equal(item, sample):
                return i
        return 0

    def __draw_scalecircle(self, ax) -> None:

        # Plot the single-unit circle
        r = self.scalecircle
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(theta, [r]*len(theta), color='black',
                linestyle=self.scalecircle_linestyle, linewidth=self.scalecircle_linewidth, zorder=10)

    def __initiate_subplot(self, ax) -> None:

        # Set custom design
        ax.set_yticklabels([])
        ax.set_xticks(self.angles if self.labels else [])
        ax.grid(False)
        ax.spines['polar'].set_visible(
            False) if not self.debug_flag else ax.spines['polar'].set_visible(True)
        ax.patch.set_facecolor('none')

    # Draw coordinate grid on the top of figure
    # to make easier subplots alignment on devtime

    def __debug_grid(self, fig, y, x) -> None:

        for i in range(1, y*x+1):

            ax = fig.add_subplot(y, x, i)

            # Set the facecolor of the axes
            ax.patch.set_facecolor('none')
            ax.set_xticks([])
            ax.set_yticks([])

            for spine in ax.spines.values():
                spine.set_edgecolor('black')

    def __draw_subplot(self, ax, resultants, modality_pattern, modalities) -> None:

        # for future sets calculation
        sets_counter = [0] * 8

        # Color measurement in HSV format (temporarry abandoned future)
        # hue_array = self.__normalization(np.angle(resultants))
        # sat_array = np.ones_like(hue_array)
        # val_array = self.__normalization(np.abs(resultants))
        # color = mcolors.hsv_to_rgb((hue, sat, val))

        for resultant, data_row, bin_row in zip(resultants, self.data, self.binarization):

            if (resultant
                and np.array_equal(bin_row, modality_pattern)
                or (self.full_center
                            and modality_pattern == (True, True, True)
                            and (tuple(bin_row) not in self.modality_patterns[:3]
                                 or self.whole_sum
                                 )
                            )
                ):

                # defining the modality of responce to apply color and z-order
                modality_pattern_number = self.__find_match_modality(
                    bin_row, self.modality_patterns)
                sets_counter[modality_pattern_number] += 1
                color = self.colors[modality_pattern_number]
                zorder = modality_pattern_number

                ax.plot(
                    [0, np.angle(resultant)],
                    [0, np.abs(resultant)],
                    zorder=zorder,
                    marker=self.marker,
                    linestyle=self.linestyle,
                    linewidth=self.linewidth,
                    color=color,
                    alpha=self.alpha
                )
                if self.labels:
                    ax.set_xticklabels(modalities)

        if self.scalecircle:
            self.__draw_scalecircle(ax)

        if not self.whole_sum and sum(modality_pattern) == 1:
            ax.set_visible(False)

    def _make_layout(self) -> None:
        '''
            Make figure layout,
            starting point of plotting
        '''

        # Defining layout
        gs = gridspec.GridSpec(20, 20, figure=self.fig)
        ax1 = self.fig.add_subplot(gs[7:17, 1:11], polar=True)
        ax2 = self.fig.add_subplot(gs[1:11, 5:15], polar=True)
        ax3 = self.fig.add_subplot(gs[7:17, 9:19], polar=True)
        ax12 = self.fig.add_subplot(gs[4:14, 3:13], polar=True)
        ax13 = self.fig.add_subplot(gs[7:17, 5:15], polar=True)
        ax23 = self.fig.add_subplot(gs[4:14, 7:17], polar=True)
        ax0 = self.fig.add_subplot(gs[5:15, 5:15], polar=True)
        subplots = (ax1, ax2, ax3, ax12, ax13, ax23, ax0)

        # calculate resultants
        resultants = self.__vector_addition(self.data, self.binarization)

        # plot each subplot
        for ax, modality_pattern, modalities in zip(subplots, self.modality_patterns, self.modalities_array):
            self.__initiate_subplot(ax)
            self.__draw_subplot(ax, resultants, modality_pattern, modalities)

        if self.same_scale:
            rlim = ax0.get_xlim()
            for ax in subplots:
                ax.set_rlim(rlim)

        # Draw coordinate grid on the top of figure
        # to make easier subplots alignment on devtime
        if self.debug_flag:
            self.__debug_grid(self.fig, 20, 20)

        plt.subplots_adjust(wspace=0.0, hspace=0.0)
        plt.tight_layout()
        plt.suptitle(self.title)


if __name__ == '__main__':
    print('\nThis script can be used as an imported module only\n')
