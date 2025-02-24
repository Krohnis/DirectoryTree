# Directory Tree: Pseudo File Manager

This is a simple **Directory Tree** program implemented in Python that functions as a pseudo file manager.  It allows users to create, move, list, and delete directories in a hierarchical structure.

## Features:
- **CREATE directories**: You can create directories in a specified path.
- **MOVE directories**: You can move directories from one location to another. Directories with the same name will be merged without overwriting.
- **LIST directories**: Lists the current directory structure, including subdirectories.
- **DELETE directories**: Delete a specified directory and its contents.
- **Prevents circular movements**: Prevents moving a directory into itself or into a subdirectory of itself.

## Setup

### Prerequisites:
- Python 3.x

### Running the Program:
1. Clone or download the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the Python program:

   ```bash
   python3 directory_tree.py
   ```
4. The program will enter a command prompt where you can type commands.

### Available Commands:
- **CREATE <path>**: Create a directory at the specified path.
  Example:
  ```bash
  CREATE foods/fruits/apples/fuji/
  CREATE foods/fruits/apples/red
  CREATE foods/fruits/apples/_super_special_apple_
  ```
- **MOVE <source_path> <destination_path>**: Move a directory from the source path to the destination path. If the directory with the same name exists at the destination, the contents of both directories will be merged.
  Example:
  ```bash
  MOVE foods/fruits ~
  MOVE fruits foods
  MOVE vegetables foods # Error
  ```
- **DELETE <path>**: Delete a directory at the specified path.
  Example:
  ```bash
  DELETE fruits/apples
  DELETE foods
  DELETE ~ # Error
  ```
- **LIST**: List the entire directory structure from the root.
  Example:
  ```bash
  LIST
  ```
- **EXIT**: Exit the program gracefully.

### Example Usage:
Sample Input:
```bash
> CREATE fruits/apples
> CREATE foods/fruits/banana
> MOVE fruits foods
> LIST
```
Sample Output:
```bash
foods
  fruits
    apples
    banana
```
### How It Works:
- Directories are stored as a tree structure, with each directory pointing to its subdirectories. Each can be considered a node linked to many child nodes.
- Magic. :)


