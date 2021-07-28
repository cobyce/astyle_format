
pluma astyle code format plugin

- install

	- copy or link project to the following dir:
	
		ln -s '/path/to/astyle_format' /home/<user>/.local/share/pluma/plugins/

- customize

	- to pass new params to astyle edit astyle_format.py on the line that contains:
	
		cmd = ["astyle 

- to format your code go to Tools - AStyle Format 
	
- tested with pluma 1.24.0

