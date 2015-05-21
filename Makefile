CURVER=$(shell dpkg-parsechangelog -S Version)


all:
	@echo "Nada"

change_version:
	@sed -i 's/^VERSION_TXT.*/VERSION_TXT = """Versión: $(CURVER)"""/g' src/lib/about.py
