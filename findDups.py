import re
from xml.etree import ElementTree as ET
from gooey import Gooey, GooeyParser
import argparse

@Gooey(program_name="Find Duplicates in SVG", 
       default_size=(1024, 800), 
      )

def main():
    # Main function to accept an SVG file
    if __name__ == "__main__":
        parser = GooeyParser(description="Select a file to process")
        parser.add_argument(
            'input_file',
            metavar='Input File',
            help='Select the file to be processed',
            widget='FileChooser'
        )
        file_path = parser.parse_args()

        # Identify duplicates
        results = parse_svg_file_for_duplicates(file_path.input_file)

        # Output the results
        if results:
            print("=============================================================")
            print("Duplicate points found:")
            for result in results:
                print(f"Path ID: {result['id']}")
        else:
            print("No duplicate points found.")

def parse_svg_file_for_duplicates(file_path):
    """
    Parse an SVG file, extract paths, and identify duplicate consecutive points.
    """
    try:
        # Parse the SVG file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Namespace handling (optional, depending on SVG)
        namespaces = {'svg': 'http://www.w3.org/2000/svg'}

        # Find all <path> elements
        paths = root.findall('.//svg:path', namespaces)
        results = []

        for path in paths:
            d_attribute = path.get('d')
            path_id = path.get('id', 'No ID')  # Get the ID or "No ID" if missing

            if d_attribute:
                duplicates = find_duplicates_in_d(d_attribute)
                if duplicates:
                    results.append({'id': path_id, 'duplicates': duplicates})
        
        return results
    except Exception as e:
        print(f"Error parsing SVG file: {e}")
        return []

def find_duplicates_in_d(d_attribute):
    """
    Identify duplicate consecutive points in a `d` attribute.
    """
    # Split the path commands and numbers
    path_commands = re.findall(r'[a-zA-Z]|[-\d.]+(?:,[-\d.]+)?', d_attribute)

    points = []
    duplicates = []

    for command in path_commands:
        if re.match(r'[-\d.]+,[-\d.]+', command):  # Match coordinates
            # Convert to tuple (float, float)
            point = tuple(map(float, command.split(',')))
            # Check for duplicates
            if points and point == points[-1]:
                duplicates.append(point)
            points.append(point)

    return duplicates

if __name__ == "__main__":
    main()
