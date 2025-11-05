.PHONY: install run test

install:
	@echo "Installing requirements..."
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

run:
	@echo "Running Othello (human plays black by default, AI time limit 30s):"
	python run.py --human black --time 30

test:
	@echo "Running quick syntax checks..."
	python -m py_compile run.py othello/board.py othello/ai.py othello/eval.py othello/cli.py
