
"""
Yandex Source Explorer
======================

A lightweight terminal tool for exploring large collections
of source-code file lists.

Features:
    - Automatically discovers *_file_list.txt files
    - Lists available modules
    - Searches paths
    - Searches filenames
    - Searches file extensions
    - Searches inside a specific module
    - Displays repository statistics
    - Processes files line-by-line to reduce memory usage

Author:
    Fouad Azahaf

Contact:
    Email: fouadazahf@gmail.com
    Website: https://fouadazahaf.com
    GitHub: https://github.com/foux9

License:
    MIT

Disclaimer:
    This is an independent utility for navigating and analyzing
    file-list data. It is not affiliated with or endorsed by Yandex.

    Users are responsible for ensuring that the data they analyze
    is obtained and used lawfully and in accordance with applicable
    licenses and terms of use.
"""

from pathlib import Path
import argparse
import sys


                                                               
                                          
                                                               

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        ██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗  ██╗          ║
║        ╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝╚██╗██╔╝          ║
║         ╚████╔╝ ███████║██╔██╗ ██║█████╗   ╚███╔╝           ║
║          ╚██╔╝  ██╔══██║██║╚██╗██║██╔══╝   ██╔██╗           ║
║           ██║   ██║  ██║██║ ╚████║███████╗██╔╝ ██╗          ║
║           ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝          ║
║                                                              ║
║                 SOURCE CODE EXPLORER                         ║
║                                                              ║
║              [ RECON • SEARCH • ANALYSIS ]                   ║
║                                                              ║
║       Terminal toolkit for large source-code datasets        ║
║                                                              ║
║       ───────────────────────────────────────────────        ║
║                                                              ║
║       Author  : Fouad Azahaf                                 ║
║       GitHub  : github.com/foux9                               ║
║       Web     : fouadazahaf.com                               ║
║                                                              ║
║       Status  : READY                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


class YandexExplorer:

    def __init__(self, directory):

        self.directory = Path(directory).expanduser().resolve()

        self.file_lists = []

        self.discover_lists()

                                                               
                         
                                                               

    def discover_lists(self):

        if not self.directory.exists():

            print(
                f"\n[ERROR] Directory not found:\n"
                f"{self.directory}"
            )

            sys.exit(1)

        if not self.directory.is_dir():

            print(
                f"\n[ERROR] This is not a directory:\n"
                f"{self.directory}"
            )

            sys.exit(1)

        self.file_lists = sorted(
            self.directory.glob("*_file_list.txt")
        )

                                                               
                     
     
                            
        
              
                                                               

    def module_name(self, path):

        name = path.name

        suffix = "_file_list.txt"

        if name.endswith(suffix):

            return name[:-len(suffix)]

        return name

                                                               
                      
                                                               

    def show_modules(self):

        print("\n" + "=" * 70)
        print("AVAILABLE SOURCE CODE MODULES")
        print("=" * 70)

        if not self.file_lists:

            print("\nNo *_file_list.txt files found.")

            return

        print(
            f"\nFound {len(self.file_lists):,} modules:\n"
        )

        for number, file in enumerate(
            self.file_lists,
            1
        ):

            print(
                f"{number:3}. "
                f"{self.module_name(file):25} "
                f"{file.name}"
            )

                                                               
                 
     
                                                           
                                                               

    def count_lines(self, file):

        count = 0

        try:

            with open(
                file,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as f:

                for _ in f:

                    count += 1

        except OSError as error:

            print(
                f"\n[ERROR] Could not read {file}"
            )

            print(error)

        return count

                

    def statistics(self):

        print("\n" + "=" * 70)
        print("SCANNING FILE LISTS")
        print("=" * 70)

        if not self.file_lists:

            print("\nNo files found.")

            return

        total = 0

        for number, file in enumerate(
            self.file_lists,
            1
        ):

            print(
                f"\r[{number}/{len(self.file_lists)}] "
                f"Scanning {file.name}...",
                end="",
                flush=True
            )

            count = self.count_lines(file)

            total += count

        print("\n")

        print("=" * 70)
        print("STATISTICS")
        print("=" * 70)

        print(
            f"Modules       : "
            f"{len(self.file_lists):,}"
        )

        print(
            f"Total paths   : "
            f"{total:,}"
        )

                 

    def search_path(
        self,
        query,
        module=None
    ):

        query = query.lower()

        files = self.file_lists

                                       

        if module:

            files = [
                file
                for file in files
                if self.module_name(file).lower()
                == module.lower()
            ]

            if not files:

                print(
                    f"\n[ERROR] Module not found: "
                    f"{module}"
                )

                return

        print("\n" + "=" * 70)

        print(
            "PATH SEARCH"
        )

        print("=" * 70)

        print(
            f"\nQuery : {query}"
        )

        if module:

            print(
                f"Module: {module}"
            )

        print()

        found = 0

                             

        for list_file in files:

            try:

                with open(
                    list_file,
                    "r",
                    encoding="utf-8",
                    errors="replace"
                ) as f:

                    for line in f:

                        path = line.strip()

                        if not path:

                            continue

                        if query in path.lower():

                            print(
                                f"{self.module_name(list_file):20} "
                                f"{path}"
                            )

                            found += 1

            except OSError as error:

                print(
                    f"\n[ERROR] {list_file}"
                )

                print(error)

        print("\n" + "-" * 70)

        print(
            f"Matches: {found:,}"
        )

                     

    def search_filename(
        self,
        filename,
        module=None
    ):

        filename = filename.lower()

        files = self.file_lists

        if module:

            files = [
                file
                for file in files
                if self.module_name(file).lower()
                == module.lower()
            ]

            if not files:

                print(
                    f"\n[ERROR] Module not found: "
                    f"{module}"
                )

                return

        print("\n" + "=" * 70)

        print(
            "FILENAME SEARCH"
        )

        print("=" * 70)

        print(
            f"\nFilename: {filename}"
        )

        if module:

            print(
                f"Module  : {module}"
            )

        print()

        found = 0

        for list_file in files:

            try:

                with open(
                    list_file,
                    "r",
                    encoding="utf-8",
                    errors="replace"
                ) as f:

                    for line in f:

                        path = line.strip()

                        if not path:

                            continue

                        basename = Path(path).name.lower()

                        if filename in basename:

                            print(
                                f"{self.module_name(list_file):20} "
                                f"{path}"
                            )

                            found += 1

            except OSError as error:

                print(
                    f"\n[ERROR] {list_file}"
                )

                print(error)

        print("\n" + "-" * 70)

        print(
            f"Matches: {found:,}"
        )

                      

    def search_extension(
        self,
        extension,
        module=None
    ):

        extension = extension.lower()

        if not extension.startswith("."):

            extension = "." + extension

        files = self.file_lists

        if module:

            files = [
                file
                for file in files
                if self.module_name(file).lower()
                == module.lower()
            ]

            if not files:

                print(
                    f"\n[ERROR] Module not found: "
                    f"{module}"
                )

                return

        print("\n" + "=" * 70)

        print(
            "EXTENSION SEARCH"
        )

        print("=" * 70)

        print(
            f"\nExtension: {extension}"
        )

        if module:

            print(
                f"Module   : {module}"
            )

        print()

        found = 0

        for list_file in files:

            try:

                with open(
                    list_file,
                    "r",
                    encoding="utf-8",
                    errors="replace"
                ) as f:

                    for line in f:

                        path = line.strip()

                        if not path:

                            continue

                        if (
                            Path(path).suffix.lower()
                            == extension
                        ):

                            print(
                                f"{self.module_name(list_file):20} "
                                f"{path}"
                            )

                            found += 1

            except OSError as error:

                print(
                    f"\n[ERROR] {list_file}"
                )

                print(error)

        print("\n" + "-" * 70)

        print(
            f"Matches: {found:,}"
        )

                      

    def menu(self):

        while True:

            print("\n")

            print(
                "╔══════════════════════════════════════════════════════════╗"
            )

            print(
                "║                 YANDEX SOURCE EXPLORER                  ║"
            )

            print(
                "╠══════════════════════════════════════════════════════════╣"
            )

            print(
                "║ [1] List all modules                                    ║"
            )

            print(
                "║ [2] Search path                                         ║"
            )

            print(
                "║ [3] Search filename                                     ║"
            )

            print(
                "║ [4] Search extension                                    ║"
            )

            print(
                "║ [5] Search path inside one module                       ║"
            )

            print(
                "║ [6] Statistics                                          ║"
            )

            print(
                "║ [7] Exit                                                ║"
            )

            print(
                "╚══════════════════════════════════════════════════════════╝"
            )

            choice = input(
                "\nSelect option: "
            ).strip()

                          

            if choice == "1":

                self.show_modules()

                         

            elif choice == "2":

                query = input(
                    "\nPath to search: "
                ).strip()

                if query:

                    self.search_path(query)

                             

            elif choice == "3":

                filename = input(
                    "\nFilename to search: "
                ).strip()

                if filename:

                    self.search_filename(
                        filename
                    )

                                                               
                              
                                                               

            elif choice == "4":

                extension = input(
                    "\nExtension "
                    "(.go, .py, .cpp...): "
                ).strip()

                if extension:

                    self.search_extension(
                        extension
                    )

                                                               
                           
                                                               

            elif choice == "5":

                module = input(
                    "\nModule name "
                    "(example: security): "
                ).strip()

                query = input(
                    "Path to search: "
                ).strip()

                if module and query:

                    self.search_path(
                        query,
                        module
                    )

                                                               
                        
                                                               

            elif choice == "6":

                self.statistics()

                                                               
                  
                                                               

            elif choice == "7":

                print(
                    "\nThank you for using "
                    "Yandex Source Explorer."
                )

                print(
                    "Goodbye."
                )

                break

                                                               
                            
                                                               

            else:

                print(
                    "\n[ERROR] Invalid option."
                )




def main():

    print(BANNER)

    parser = argparse.ArgumentParser(
        description=(
            "Explore large collections of "
            "source-code file lists."
        )
    )

    parser.add_argument(
        "directory",
        help=(
            "Directory containing "
            "*_file_list.txt files"
        )
    )

    args = parser.parse_args()

    explorer = YandexExplorer(
        args.directory
    )

    explorer.show_modules()

    explorer.menu()


if __name__ == "__main__":

    main()
