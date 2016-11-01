# Sinusoidal signal generator prototype

# How to run it?
Open comand prompt and type: python3 simulator.py

# Where is results?
After a simulation execution the two html files will created (dds_output.html and dds_output_low_magnitude.html). You can open them by your browser(Chrome is preferable).

# How to add a custom function?
Open simulator.py into the your favorite text editor and add changes to script. Here is default script:
> s1 = Simulator(magnitude = 1.0, frequency = 110)

> s1.run(0.003)

> s1.frequency = 500

> s1.run(0.003)

> s1.frequency = 20

> s1.run(0.003)
