# Define directories
SNIPPET_GEN = snippet_gen
SPECTRE = spectre
SNIPPETS = $(SNIPPET_GEN)/snippets
BINARIES = $(SNIPPET_GEN)/binaries
BIN_OUTPUT = $(SPECTRE)/bin

# Default target
all:

clean_bin:
	@rm -rf m5out
	@rm -rf snippet_gen/binaries
	@rm -rf snippet_gen/snippets
	@make -C spectre clean

# Rule to check and create directories
check_dirs:
	@for dir in $(BINARIES) $(SNIPPETS); do \
		if [ ! -d $$dir ]; then \
			echo "Directory $$dir does not exist. Creating..."; \
			mkdir -p $$dir; \
		else \
			echo "Directory $$dir already exists."; \
		fi \
	done

# ASM target to run the Python script
asm: check_dirs
	@if [ -z "$(line)" ]; then \
		cd $(SNIPPET_GEN) && python3 opcode_fuzz.py 1; \
		python3 opcode_fuzz.py 2; \
		python3 opcode_fuzz.py 3; \
		python3 opcode_fuzz.py 4; \
		python3 opcode_fuzz.py 5; \
		python3 opcode_fuzz.py 6; \
		python3 opcode_fuzz.py 7; \
		python3 opcode_fuzz.py 8; \
		python3 opcode_fuzz.py 9; \
		echo "done !"; \
	else \
		cd $(SNIPPET_GEN) && python3 opcode_fuzz.py $(line); \
	fi

# Compile target
compile: check_dirs
	@for snippet in $(SNIPPETS)/*; do \
		filename=$$(basename $$snippet); \
		modified_name=$$(echo $$filename | sed 's/\./_/g'); \
		echo "Processing $$filename..."; \
		cp $$snippet $(SPECTRE)/snippet.s; \
		rm -f $$snippet; \
		sleep1; \
		make -C $(SPECTRE) clean; \
		make -C $(SPECTRE) all RETPOLINE=1; \
		binary_file=$$(ls $(BIN_OUTPUT)/* 2>/dev/null | head -n 1); \
		if [ -z "$$binary_file" ]; then \
			echo "No .s file found in $(BIN_OUTPUT). Skipping..."; \
		else \
			new_file_name="$${modified_name}"; \
			cp $$binary_file $(BINARIES)/$$new_file_name; \
			echo "Copied $$binary_file to $(BINARIES)/$$new_file_name"; \
		fi; \
		rm -f $(SPECTRE)/snippet.s; \
	done

print:
	@echo "Processing and renaming files:"
	@for file in $(SNIPPETS)/*; do \
		echo "Processing: $$file"; \
		cp $$file $(SPECTRE)/snippet.s; \
		rm $(SPECTRE)/snippet.s; \
		rm $$file; \
	done

sim:
	@for binary in $(wildcard $(BINARIES)/*); do \
		echo "Running simulation for $$binary..."; \
		timeout 150s ../gem5/build/RISCV/gem5.opt ../gem5/configs/example/riscv/fs_linux.py --kernel $$binary --bare --cpu-type=O3CPU --caches --l2cache; \
		if [ $$? -eq 124 ]; then \
			echo "Timeout occurred for $$binary"; \
		fi; \
		python3 ./snippet_gen/stats_reader.py $$(basename $$binary); \
		sleep 1; \
		rm -f ./m5out/stats.txt; \
	done

connect:
	@echo "Starting infinite loop. Use Ctrl+C to stop."
	@while true; do \
		echo "Running the command..."; \
		./../gem5/util/term/m5term localhost 3456; \
		sleep 1; \
	done

git:
	@if [ -z "$(commit)" ]; then \
		echo "Error: You must specify a commit message. Use 'make git commit=<message>'."; \
		exit 1; \
	fi
	@git add .
	@git commit -m "$(commit)"
	git push
