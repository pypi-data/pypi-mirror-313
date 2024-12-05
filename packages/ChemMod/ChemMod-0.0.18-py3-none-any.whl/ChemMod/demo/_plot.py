import matplotlib.pyplot as plt
import numpy as np

class plot:

    
    def __init__(self, theme='dark_background'):
        import matplotlib.pyplot as plt
        import numpy as np
        self.theme = theme

        if self.theme == 'dark_background':
          self.border_color = 'mediumspringgreen'
          self.border_width = 1
          self.text_color = 'orange'
          self.data_color = 'mediumspringgreen'
          self.marker_color = 'orange'
          self.markeredge_color = 'orange'
          self.label_color = 'orange'
          self.face_color = 'black'
        elif self.theme == 'Solarize_Light2':
          self.border_color = 'mediumspringgreen'
          self.border_width = 1
          self.text_color = 'deeppink'
          self.data_color = 'mediumspringgreen'
          self.marker_color = 'deeppink'
          self.markeredge_color = 'deeppink'
          self.label_color = 'black'
          self.face_color = 'antiquewhite'
        elif self.theme == 'grayscale':
          self.border_color = 'black'
          self.border_width = 1
          self.text_color = 'red'
          self.data_color = 'black'
          self.marker_color = 'red'
          self.markeredge_color = 'black'
          self.label_color = 'black'
        elif self.theme == 'ggplot':
          self.border_color = 'black'
          self.border_width = 1
          self.text_color = 'black'
          self.data_color = 'black'
          self.marker_color = 'aliceblue'
          self.markeredge_color = 'black'
          self.label_color = 'black'

    def plot(self, x, y, title='', xlabel='', ylabel='', legends=None):
        plt.style.use(self.theme)
        fig, ax = plt.subplots()
        ax.plot(x, y, color=self.data_color, linewidth=2, marker='o', markersize=8, markerfacecolor=self.marker_color, markeredgewidth=2, markeredgecolor=self.markeredge_color, label='Data')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
        ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
        ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

        # Add grid
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Add legends if provided
        if legends:
            ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

        # Add thicker border
        for spine in ax.spines.values():
            spine.set_color(self.border_color)
            spine.set_linewidth(self.border_width)

        plt.show()

    def lineplot(self, x, y, title='', xlabel='', ylabel='', legends=None):
        plt.style.use(self.theme)  # Use dark background style for a futuristic theme
        fig, ax = plt.subplots()
        ax.plot(x, y, color=self.data_color, linewidth=2, label='Data')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
        ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
        ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

        # Add grid
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Add legends if provided
        if legends:
            ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

        # Add thicker border
        for spine in ax.spines.values():
            spine.set_color(self.border_color)
            spine.set_linewidth(self.border_width)

        plt.show()

    def scatterplot(self, x, y, title='', xlabel='', ylabel='', legends=None):
        plt.style.use(self.theme)  # Use dark background style for a futuristic theme
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=30, color=self.marker_color, edgecolors=self.markeredge_color, linewidths=1, label='Data')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
        ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
        ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

        # Add grid
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Add legends if provided
        if legends:
            ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

        # Add thicker border
        for spine in ax.spines.values():
            spine.set_color(self.border_color)
            spine.set_linewidth(self.border_width)

        plt.show()

    def histogram(self, x, y, title='', xlabel='', ylabel='', legends=None):
        plt.style.use(self.theme)  # Use dark background style for a futuristic theme
        fig, ax = plt.subplots()
        ax.hist(x, y, color=self.data_color, label='Data')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
        ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
        ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

        # Add grid
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Add legends if provided
        if legends:
            ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

        # Add thicker border
        for spine in ax.spines.values():
            spine.set_color(self.border_color)
            spine.set_linewidth(self.border_width)

        plt.show()

    def norm_plot(self, x, y, title='', xlabel='', ylabel='', legends=None):
      x = np.array(x)/np.max(x)
      y = np.array(y)/np.max(y)

      plt.style.use(self.theme)
      fig, ax = plt.subplots()
      ax.plot(x, y, color=self.data_color, linewidth=2, marker='o', markersize=8, markerfacecolor=self.marker_color, markeredgewidth=2, markeredgecolor=self.markeredge_color, label='Data')
      ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
      ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
      ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

      # Add grid
      ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

      # Add legends if provided
      if legends:
        ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

      # Add thicker border
      for spine in ax.spines.values():
          spine.set_color(self.border_color)
          spine.set_linewidth(self.border_width)

      plt.show()

    def norm_lineplot(self, x, y, title='', xlabel='', ylabel='', legends=None):
        x = np.array(x)/np.max(x)
        y = np.array(y)/np.max(y)

        plt.style.use(self.theme)  # Use dark background style for a futuristic theme
        fig, ax = plt.subplots()
        ax.plot(x, y, color=self.data_color, linewidth=2, label='Data')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
        ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
        ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

        # Add grid
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Add legends if provided
        if legends:
            ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

        # Add thicker border
        for spine in ax.spines.values():
            spine.set_color(self.border_color)
            spine.set_linewidth(self.border_width)

        plt.show()


    def norm_scatterplot(self, x, y, title='', xlabel='', ylabel='', legends=None):
        x = np.array(x)/np.max(x)
        y = np.array(y)/np.max(y)


        plt.style.use(self.theme)  # Use dark background style for a futuristic theme
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=30, color=self.marker_color, edgecolors=self.markeredge_color, linewidths=1, label='Data')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.text_color)
        ax.set_xlabel(xlabel, fontsize=14, fontstyle='italic', color=self.text_color)
        ax.set_ylabel(ylabel, fontsize=14, fontstyle='italic', color=self.text_color)

        # Add grid
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Add legends if provided
        if legends:
            ax.legend(legends, loc='upper left', fontsize=12, labelcolor=self.label_color)

        # Add thicker border
        for spine in ax.spines.values():
            spine.set_color(self.border_color)
            spine.set_linewidth(self.border_width)