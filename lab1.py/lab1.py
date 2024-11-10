import random

# Function to read student IDs from the file
def read_student_ids(file_name):
    try:
        with open(file_name, 'r') as file:
            # Read all lines from the file and strip any extra spaces or newlines
            student_ids = [line.strip() for line in file.readlines()]
        return student_ids
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to select students for viva
def conduct_viva(student_ids):
    # List to keep track of students who haven't been selected yet
    unselected_students = student_ids.copy()
    viva_counter = 1
    
    while unselected_students:
        # Randomly select a student
        selected_student = random.choice(unselected_students)
        print(f"Viva #{viva_counter}: {selected_student}")
        
        # Remove the selected student from the list
        unselected_students.remove(selected_student)
        
        # Increment the viva counter
        viva_counter += 1
        
    print("\nAll students have been selected for viva.")
    
    # Reset the list for the next round of viva
    return student_ids

# Main function to run the process
def main():
    # Define the file name where student IDs are stored
    file_name = 'student_id.txt'  # Corrected the file name here
    
    # Read the student IDs from the file
    student_ids = read_student_ids(file_name)
    
    if not student_ids:
        return  # Exit if no student IDs were read
    
    while True:
        # Conduct the viva selection process
        student_ids = conduct_viva(student_ids)
        
        # Ask if the user wants to run the process again
        restart = input("Do you want to conduct another round of viva? (yes/no): ").lower()
        if restart != 'yes':
            print("Exiting the program.")
            break

# Run the program
if __name__ == "__main__":
    main()