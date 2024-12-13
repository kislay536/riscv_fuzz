# Define directories
SNIPPET_GEN = snippet_gen
SPECTRE = spectre
SNIPPETS = $(SNIPPET_GEN)/snippets
BINARIES = $(SNIPPET_GEN)/binaries
BIN_OUTPUT = $(SPECTRE)/bin

# Default target
all: check_dirs

clean_bin:
	@rm -rf snippet_gen/binaries

# Rule to check and create directories
check_dirs: clean_bin
	@for dir in $(BINARIES) $(SNIPPETS); do \
		if [ ! -d $$dir ]; then \
			echo "Directory $$dir does not exist. Creating..."; \
			mkdir -p $$dir; \
		else \
			echo "Directory $$dir already exists."; \
		fi \
	done

# Compile target
compile: check_dirs
	@for snippet in $(SNIPPETS); do \
		filename=$$(basename $$snippet); \
		modified_name=$$(echo $$filename | sed 's/\./_/g'); \
		echo "Processing $$filename..."; \
		mv $$snippet $(SPECTRE)/snippet.s; \
		make -C $(SPECTRE) clean; \
		echo "make -C $(SPECTRE) all RETPOLINE=1"; \
		mkdir $(SPECTRE)/bin; \
		riscv64-unknown-elf-gcc -S -o $(SPECTRE)/bin/hello.s $(SPECTRE)/src/indirectBranchFunction.c; \
		binary_file=$$(ls $(BIN_OUTPUT)/* 2>/dev/null | head -n 1); \
		if [ -z "$$binary_file" ]; then \
			echo "No .s file found in $(BIN_OUTPUT). Skipping..."; \
		else \
			new_file_name="$${modified_name}"; \
			cp $$binary_file $(BINARIES)/$$new_file_name.s; \
			echo "Copied $$binary_file to $(BINARIES)/$$new_file_name.s"; \
		fi; \
		rm -f $(SPECTRE)/snippet.s; \
	done

# ASM target to run the Python script
asm: check_dirs
	@if [ -z "$(line)" ]; then \
		echo "Error: You must specify a line number. Use 'make asm line=<integer>'."; \
		exit 1; \
	fi; \
	cd $(SNIPPET_GEN) && python3 opcode_fuzz.py $(line)

sim:
	@for binary in $(wildcard $(BINARIES)/*); do \
		echo "Running simulation for $$binary..."; \
		../gem5/build/RISCV/gem5.opt ../gem5/configs/example/riscv/fs_linux.py --kernel $$binary --bare --cpu-type=O3CPU --caches --l2cache; \
		python3 ./snippet_gen/stats_reader.py $$(basename $$binary); \
		sleep 1; \
		rm -f ./m5out/stats.txt; \
	done


git:
	@if [ -z "$(commit)" ]; then \
		echo "Error: You must specify a commit message. Use 'make git commit=<message>'."; \
		exit 1; \
	fi
	@git add .
	@git commit -m "$(commit)"
	git push