 # fit_plot

- Fit data with a straight line chosen by clicking points on a plot.

Requires: ipympl

To use:

      import fit_plot
      %matplotlib widget
      
      fit_plots.line(unique_name, xdata, ydata, yerr, chi2=False, input_boxes=True)

      or

      fit_plots.with_background(unique_name, xdata, ydata, yerr,chi2=False, input_boxes=True)

where xdata, ydata and yerr must be numpy arrays of at least two points.

Click in the data portion of the figure to set a point for the fit line.
Whichever point you click closer to will move to the new position.

For with_background(), a background value can be set: choose the
Floor radio button, then click at the desired level of background.

If chi2 == True, a chi-squared value will be calulated and displayed.

If input_boxes == True (default) boxes are displayed so that the slope,
intercept, and "floor" values may be entered manually.

Caveats:

1) if you change the unique name, the fit parameters will be lost.

2) fit parameters are stored in hidden files and won't travel if the
   notebook is renamed or moved to another directory.

3) any plots made after using one of these functions should start with
   plt.figure()

