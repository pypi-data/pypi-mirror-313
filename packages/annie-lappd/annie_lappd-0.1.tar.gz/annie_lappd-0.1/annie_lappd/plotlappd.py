from .lappd import LAPPD
import matplotlib.pyplot as plt

class plotLAPPD(LAPPD):

    def __init__(self, data, pedestals):
        super().__init__(data, pedestals)
    
    def show2DEvent(self, event_id, side, spare_channels):
        plt.imshow(self.getEvent(event_id, side, spare_channels).astype(float).T,cmap='viridis', aspect='auto')
        plt.colorbar(label='Amplitude [mV]')  # Add colorbar for reference
        plt.gca().invert_yaxis()
        plt.title("Event {}, side {}".format(event_id, side))
        plt.xlabel('Time [ns]')
        if spare_channels == 0:
            plt.ylabel('Strip #')
        else:
            plt.ylabel('Strip # + spare channels')
        plt.show()

    def show1DEvent(self, event_id, side, spare_channels):
        plt.plot(self.getEvent(event_id, side, spare_channels))
        if spare_channels == 0:
            plt.title('Projetion Event {}, side {}'.format(event_id, side))
        else:
            plt.title('Projetion Event {}, side {}, + spare channels'.format(event_id, side))
        plt.xlabel('Time [ns]')
        plt.ylabel('Amplitude [mV]')
        plt.show()

    def show2DEventAx(self, event_id, side, spare_channels, ax):
        im = ax.imshow(self.getEvent(event_id, side, spare_channels).astype(float).T,cmap='viridis', aspect='auto')
        plt.colorbar(im, ax=ax).set_label('Amplitude [mV]')  # Add colorbar for reference
        ax.invert_yaxis()
        ax.set_title("Side {}".format(side))
        ax.set_xlabel('Time [ns]')
        if spare_channels == 0:
            ax.set_ylabel('Strip #')
        else:
            ax.set_ylabel('Strip # + spare channels')

    def show1DEventAx(self, event_id, side, spare_channels, ax):
        ax.plot(self.getEvent(event_id, side, spare_channels))
        if spare_channels == 0:
            ax.set_title('Projetion , side {}'.format(side))
        else:
            ax.set_title('Projetion, side {}, + spare channels'.format(side))
        ax.set_xlabel('Time [ns]')
        ax.set_ylabel('Amplitude [mV]')

    def displayEvent(self, event_id, spare_channels, show_display):
        plt.style.use(['dark_background'])
        if show_display == 0:
            plt.switch_backend('Agg')

        # Create a figure and subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 9))
        
        # Plot data on each subplot
        self.show2DEventAx(event_id, 0, spare_channels, ax1)
        self.show2DEventAx(event_id, 1, spare_channels, ax2)
        self.show1DEventAx(event_id, 0, spare_channels, ax3)
        self.show1DEventAx(event_id, 1, spare_channels, ax4)

        # Add a general title to the canvas
        fig.suptitle("Event {}".format(event_id), fontsize=16)

        # Adjust layout
        plt.tight_layout()

        # Show the plot
        if show_display == 1:
            plt.show()
        
        plt.close()
        return fig

    def displayEventsPDF(self, spare_chn, nevent, output_name):
        print("[+] Plotting the events....")
        # Create a PDF file to save the plots
        plt.switch_backend('Agg')
        with PdfPages(output_name+".pdf") as pdf:
            # Initialize the progress bar
            progress_bar = tqdm(total=nevent, desc="Progress", unit="iteration")
            for i in range(nevent):
                fig = self.displayEvent(i, spare_chn, 0)
                pdf.savefig(fig)
                progress_bar.update(1)
            progress_bar.close()
            print("[+] Plotting done....")

