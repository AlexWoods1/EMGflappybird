.PHONY: install run notebook check setup dirs

install:
	@echo "Installing requirements"
	pip install -r requirements.txt --break-system-packages

dirs:
	@echo "Installing directories"
	mkdir -p Trial_files

run:
	@echo "Running Code"
	python EMGFlappyBird/main.py

notebook:
	@echo "Running Jupyter Notebook"
	jupyter notebook Signal_Analysis/post_processing.ipynb

check:
	@echo "Checking Connection"
	python EMGFlappyBird/check_connection.py

setup: install dirs run
	@echo "Complete!"