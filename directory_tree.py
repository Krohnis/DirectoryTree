class Directory:
    def __init__(self, name):
        self.name = name.lower()
        self.subdirectories = {}
        self.parent = None  # Set the parent to the passed parent directory

    def add_subdirectory(self, subdirectory_name):
        subdirectory_name = subdirectory_name.lower()
        if subdirectory_name not in self.subdirectories:
            new_dir = Directory(subdirectory_name)
            new_dir.parent = self  # Set the parent to the current directory
            self.subdirectories[subdirectory_name] = new_dir
            return new_dir
        return self.subdirectories[subdirectory_name]

    def get_subdirectory(self, subdirectory_name):
        return self.subdirectories.get(subdirectory_name.lower())

    def delete_subdirectory(self, subdirectory_name):
        subdirectory_name = subdirectory_name.lower()
        if subdirectory_name in self.subdirectories:
            del self.subdirectories[subdirectory_name]
            return True
        return False

    def __lt__(self, other):
        # Less than comparison based on directory name for sorting.
        return self.name < other.name

    def __str__(self, level=0):
        result = "  " * level + self.name + "\n"
        for subdir in sorted(self.subdirectories.values(), key=lambda d: d.name):
            result += subdir.__str__(level + 1)
        return result

class DirectoryTree:
    def __init__(self):
        self.root = Directory('')

    def create(self, path):
        if path == '~':
            print("Cannont create a directory named ~")
            return

        parts = path.split('/')
        # Remove any empty parts (like trailing slashes or multiple slashes that create empty strings)
        parts = [part for part in parts if part]
        current_dir = self.root
        for part in parts:
            if part not in current_dir.subdirectories:
                current_dir.add_subdirectory(part)
            current_dir = current_dir.get_subdirectory(part)

    def move(self, src_path, dest_path):
        # Split paths to navigate the directories
        src_parts = src_path.split('/')
        dest_parts = dest_path.split('/')

        # Get the destination directory
        if dest_parts[0] == '~':  # Special case for root
            dest_dir = self.root
            dest_parts = dest_parts[1:]  # Remove the ~ part
        else:
            dest_dir = self.root
            for part in dest_parts:
                dest_dir = dest_dir.get_subdirectory(part)
                if not dest_dir:
                    print(f"Cannot move {src_path} - {dest_path} does not exist")
                    return

        # Get the source directory
        src_dir = self.root
        for part in src_parts[:-1]:
            src_dir = src_dir.get_subdirectory(part)
            if not src_dir:
                print(f"Cannot move {src_path} - Parent directory does not exist")
                return

        src_subdir = src_dir.get_subdirectory(src_parts[-1])
        if not src_subdir:
            print(f"Cannot move {src_path} - {src_parts[-1]} does not exist")
            return

        # Prevent moving a directory into its own subdirectory or parent (circular structure)
        if self.is_ancestor(src_subdir, dest_dir) or src_subdir == dest_dir:
            print(f"Cannot move {src_path} - it cannot be moved into itself or its subdirectories")
            return

        # If the destination already contains a subdirectory with the same name as the source
        if src_parts[-1] in dest_dir.subdirectories:
            dest_subdir = dest_dir.get_subdirectory(src_parts[-1])

            # Merge the subdirectories: copy all subdirectories from source into the destination subdirectory
            for subdir_name, subdir in src_subdir.subdirectories.items():
                # If the subdirectory doesn't already exist in the destination, add it
                if subdir_name not in dest_subdir.subdirectories:
                    dest_subdir.add_subdirectory(subdir_name)
                # Ensure the subdirectory's content is merged (not overwritten)
                dest_subdir.get_subdirectory(subdir_name).subdirectories.update(subdir.subdirectories)
        else:
            # Otherwise, simply move the directory by adding it to the destination
            dest_dir.add_subdirectory(src_parts[-1])
            dest_subdir = dest_dir.get_subdirectory(src_parts[-1])
            dest_subdir.subdirectories = src_subdir.subdirectories

        # After moving, remove the directory from the original location
        src_dir.delete_subdirectory(src_parts[-1])

    def delete(self, path):
        if path == '~':
            print("Cannont delete root directory ~")
            return
        
        parts = path.split('/')
        current_dir = self.root
        for part in parts[:-1]:
            current_dir = current_dir.get_subdirectory(part)
            if not current_dir:
                print(f"Cannont delete {path} - {parts[-2]} does not exist")
                return

        if not current_dir.delete_subdirectory(parts[-1]):
            if len(parts) == 1:
                print(f"Cannot delete {path} - {path} does not exist")
            else:
                print(f"Cannot delete {path} - {parts[-2]} does not exist")

    def list(self):
        print(self.root)

    def is_ancestor(self, potential_ancestor, dir_to_check):
        # Helper function to check if 'potential_ancestor' is an ancestor of 'dir_to_check'.
        # We check by traversing up from the dir_to_check to see if we reach the potential_ancestor.
        current = dir_to_check
        while current:
            if current == potential_ancestor:
                return True
            current = current.parent  # Traverse upwards to check if the potential_ancestor is an ancestor
        return False

def process_commands():
    directory_tree = DirectoryTree()
    
    print("Directory Tree is ready. Enter your commands (type 'EXIT' to quit):")
    
    while True:
        command = input("> ").strip()
        if command.upper() == 'EXIT':
            break
        
        parts = command.split()
        if len(parts) == 0:
            print("Invalid command. Please try again.")
            continue

        action = parts[0].upper()
        if action == 'CREATE' and len(parts) == 2:
            directory_tree.create(parts[1])
        elif action == 'MOVE' and len(parts) == 3:
            directory_tree.move(parts[1], parts[2])
        elif action == 'DELETE' and len(parts) == 2:
            directory_tree.delete(parts[1])
        elif action == 'LIST' and len(parts) == 1:
            directory_tree.list()
        else:
            print("Invalid command. Please try again.")

if __name__ == '__main__':
    process_commands()
