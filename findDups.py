import re
from xml.etree import ElementTree as ET

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

# Main function to accept an SVG file
if __name__ == "__main__":
    # Prompt user for the file path
    file_path = input("Enter the path to the SVG file: ").strip()

    # Identify duplicates
    results = parse_svg_file_for_duplicates(file_path)

    # Output the results
    if results:
        print("Duplicate points found:")
        for result in results:
            print(f"Path ID: {result['id']}")
            for duplicate in result['duplicates']:
                print(f"  Duplicate Point: {duplicate}")
    else:
        print("No duplicate points found.")

