import os
import tempfile
import subprocess
import atexit
import pkg_resources

pkg_resources.resource_filename('DijkstraPathfinder', r'DataStructures\Graph\graph.c')

class Binder:

    def __init__(self):

        self.input_file_path = None
        self.output_file_path = None
        self.executable_path = None
        self.compile_command = [

            'gcc',
            pkg_resources.resource_filename('DijkstraPathfinder', r'DataStructures\Graph\graph.c'),
            pkg_resources.resource_filename('DijkstraPathfinder', r'DataStructures\Heap\heap.c'),
            pkg_resources.resource_filename('DijkstraPathfinder', r'Algorithms\Dijkstra\Implementation\dijkstra.c'),
            pkg_resources.resource_filename('DijkstraPathfinder', r'Algorithms\Dijkstra\Bindings\dijkstra_bindings.c'),
            '-o'
        ]

    # Create a temporary file with the given data
    def __create_temp_file(self, data:str, suffix:str='.txt') -> str:

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tempFile:
            tempFile.write(data.encode('utf-8'))
            return tempFile.name

    # Create a temporary executable file
    def __create_temp_executable(self) -> str:

        with tempfile.NamedTemporaryFile(delete=False, suffix='.exe') as tempFile:
            return tempFile.name

    # Compile C files to create the executable
    def __compile_c_files(self, temp_executable_path:str) -> None:

        compile_command = self.compile_command + [temp_executable_path]

        try:
            subprocess.run(compile_command, check=True)

        except subprocess.CalledProcessError as e:
            print("Compilation failed:", e)
            raise

    # Run the compiled executable
    def __run_executable(self) -> None:

        run_command = [self.executable_path, self.input_file_path, self.output_file_path]

        try:
            subprocess.run(run_command, check=True)

        except subprocess.CalledProcessError as e:
            print("Execution Error:", e)
            raise

    # Read the output file into a list of lists
    def _get_output_file(self) -> list[list[str]]:

        data = []

        with open(self.output_file_path, 'r') as file:

            for line in file:
                values = line.split()
                data.append(values)

        return data

    # Main method to run the program
    def run_program(self, input_data:list[list[str]]) -> list[list[str]]:

        # Prepare input data as a string for the input file
        input_data_str = ""

        numNodes, start = input_data[0]
        input_data_str += f"{numNodes} {start}\n"

        nodes = input_data[1]
        input_data_str += " ".join(nodes) + "\n"

        for edge in input_data[2:]:
            input_data_str += " ".join(map(str, edge)) + "\n"

        # Create temporary files for input, output, and executable
        self.input_file_path = self.__create_temp_file(input_data_str)
        self.output_file_path = self.__create_temp_file("")
        self.executable_path = self.__create_temp_executable()

        # Register file cleanup at exit
        atexit.register(lambda: os.remove(self.input_file_path))
        atexit.register(lambda: os.remove(self.output_file_path))
        atexit.register(lambda: os.remove(self.executable_path))

        # Compile and run the executable
        self.__compile_c_files(self.executable_path)
        self.__run_executable()
        data = self._get_output_file()

        return data

# Main function to run the binder program
def run(input_data:list[list[str]]) -> list[list[str]]:

    binder = Binder()
    data = binder.run_program(input_data)

    return data

# Function to retrieve the shortest path to a destination
def get_path(shortestPathTable:list[list[str]], destination:str) -> list[str]:

    path = []
    node = destination

    while node != '-':

        path.append(node)
        for row in shortestPathTable:
            if row[0] == node:
                node = row[-1]
                break

    path.reverse()
    return path
