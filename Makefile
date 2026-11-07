.PHONY: setup test download train report clean tree

setup:
	@echo "Creating conda environment from environment.yml..."
	conda env create -f environment.yml || echo "Environment exists."

test:
	pytest tests/ -v

download:
	python scripts/download_data.py

train:
	python scripts/run_experiment.py --config configs/v1_baseline.yaml

report:
	python scripts/generate_report.py --config configs/v1_baseline.yaml

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

tree:
	find . -type d -not -path './.git*' -not -path './.venv*' \
		-not -path '*/__pycache__*' -not -path './.vscode*' \
		| sort | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
