# heatflux-fw

A python automation script for reading serial data output from CalSol battery's heat flux and pressure drop sensor board.

It currently dumps garbage data for testing. It will connect to actual board when hardware is designed and validated.

One line per sample, 115200 baud: 

    <ms>,<heat_flux_W_m2>,<pressure_Pa>

Example: `3200,58.3,-12.0`