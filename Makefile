# Define directories
SNIPPET_GEN = snippet_gen
SPECTRE = spectre
SNIPPETS = $(SNIPPET_GEN)/snippets
BINARIES = $(SNIPPET_GEN)/binaries
BIN_OUTPUT = $(SPECTRE)/bin

# Default target
all:

clean_bin:
	@if [ -d "m5out" ]; then rm -rf m5out; fi
	@if [ -d "snippet_gen/binaries" ]; then rm -rf snippet_gen/binaries; fi
	@if [ -d "snippet_gen/snippets" ]; then rm -rf snippet_gen/snippets; fi
	@make -C spectre clean
	@if [ -f "stats_data.csv" ]; then rm stats_data.csv; fi
	@if [ -f "simul_output.txt" ]; then rm simul_output.txt; fi
	@if [ -f "terminal_output.txt" ]; then rm terminal_output.txt; fi
	@sleep 1
	@clear


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
		cd $(SNIPPET_GEN) && python3 opcode_replacement.py 1; \
		python3 opcode_replacement.py 2; \
		python3 opcode_replacement.py 3; \
		python3 opcode_replacement.py 4; \
		python3 opcode_replacement.py 5; \
		python3 opcode_replacement.py 6; \
		python3 opcode_replacement.py 7; \
		python3 opcode_replacement.py 8; \
		python3 opcode_replacement.py 9; \
		echo "done !"; \
	else \
		cd $(SNIPPET_GEN) && python3 opcode_replacement.py $(line); \
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
	@if [ -f simul_output.txt ]; then \
		echo "Found simul_output.txt. Deleting it..."; \
		rm simul_output.txt; \
	fi
	@if [ -f simul_output.txt ]; then \
		echo "Found stats_data.csv. Deleting it..."; \
		rm stats_data.csv; \
	fi
	@for binary in $(wildcard $(BINARIES)/*); do \
		echo "==============="; \
		echo "Running simulation for $$binary..."; \
		timeout 30s ../gem5/build/RISCV/gem5.opt ../gem5/configs/example/riscv/fs_linux.py --kernel $$binary --bare --cpu-type=O3CPU --caches --l2cache 2>&1; \
		if [ $$? -eq 124 ]; then \
			echo "Timeout occurred for $$binary"; \
		fi; \
		python3 ./snippet_gen/stats_reader.py $$(basename $$binary); \
		sleep 1; \
		rm -f ./m5out/stats.txt; \
		echo "***************"; \
	done | tee -a simul_output.txt


connect:
	@if [ -f terminal_output.txt ]; then \
		echo "Found terminal_output.txt. Deleting it..."; \
		rm terminal_output.txt; \
	fi
	@echo "Starting infinite loop. Use Ctrl+C to stop."
	@while true; do \
		echo "Running the command..."; \
		./../gem5/util/term/m5term localhost 3456; \
		sleep 0.001; \
	done | tee -a terminal_output.txt


start:
	@echo "Starting infinite loop. Use Ctrl+C to stop."
	file=$(find $(riscv)/riscv_fuzz/snippet_gen/binaries/ -type f | shuf -n 1) && filename=$(basename "$(file)") && ../gem5/build/RISCV/gem5.opt ../gem5/configs/example/riscv/fs_linux.py --kernel $(file) --bare --cpu-type=O3CPU --caches --l2cache; \
	@while true; do \
		echo "Running the Simulation..."; \
		timeout 30s python3 ./snippet_gen/stats_reader.py $(filename) && rm $(file) && file=$(find $(riscv)/riscv_fuzz/snippet_gen/binaries/ -type f | shuf -n 1) && filename=$(basename "$(file)") && ../gem5/build/RISCV/gem5.opt ../gem5/configs/example/riscv/fs_linux.py --kernel $(file) --bare --cpu-type=O3CPU --caches --l2cache; \
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
