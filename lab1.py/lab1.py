import random


def read_student_ids(file_name):
    try:
        with open(file_name, 'r') as file:
            
            student_ids = [line.strip() for line in file.readlines()]
        return student_ids
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def conduct_viva(student_ids):
  
    unselected_students = student_ids.copy()
    viva_counter = 1
    
    while unselected_students:
       
        selected_student = random.choice(unselected_students)
        print(f"Viva #{viva_counter}: {selected_student}")
        
      
        unselected_students.remove(selected_student)
        
      
        viva_counter += 1
        
    print("\nAll students have been selected for viva.")
    
    
    return student_ids


def main():
    
    file_name = 'student_id.txt'  
  
    student_ids = read_student_ids(file_name)
    
    if not student_ids:
        return  
    
    while True:
        
        student_ids = conduct_viva(student_ids)
        
      
        restart = input("Do you want to conduct another round of viva? (yes/no): ").lower()
        if restart != 'yes':
            print("Exiting the program.")
            break


if __name__ == "__main__":
    main()