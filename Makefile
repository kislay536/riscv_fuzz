# Define directories
SNIPPET_GEN = snippet_gen
SPECTRE = spectre
SNIPPETS = $(SNIPPET_GEN)/snippets
BINARIES = $(SNIPPET_GEN)/binaries
BIN_OUTPUT = $(SPECTRE)/bin

# Default target
all: check_dirs

clean:
	@rm -rf snippet_gen/binaries

# Rule to check and create directories
check_dirs: clean
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
	@for snippet in $(SNIPPETS)/*.s; do \
		filename=$$(basename $$snippet); \
		modified_name=$$(echo $$filename | sed 's/\./_/g'); \
		echo "Processing $$filename..."; \
		cp $$snippet $(SPECTRE)/snippet.s; \
		make -C $(SPECTRE) all RETPOLINE=1; \
		binary_file=$$(ls $(BIN_OUTPUT)/* 2>/dev/null | head -n 1); \
		if [ -z "$$binary_file" ]; then \
			echo "No binary file found in $(BIN_OUTPUT). Skipping..."; \
		else \
			new_binary_name="spectre_$${modified_name}"; \
			cp $$binary_file $(BINARIES)/$$new_binary_name; \
			echo "Copied $$binary_file to $(BINARIES)/$$new_binary_name"; \
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


