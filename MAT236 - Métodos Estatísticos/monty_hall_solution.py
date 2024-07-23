import random


def monty_hall(n_doors = 3):
    # Set the doors.
    n_doors = max(n_doors, 3)
    
    doors = [0,] * n_doors
    doors[random.randint(0, len(doors) - 1)] = 1
    
    # Participant chooses a random door.
    choice = random.randint(0, len(doors) - 1)
    choice = doors.pop(choice)

    # Host opens a door.
    open_door = random.randint(0, len(doors) - 1)

    if doors[open_door] == 1:
        open_door += (-1 if open_door > 0 else 1)

    open_door = doors.pop(open_door)

    # Participant changes the choice.
    new_choice = random.randint(0, len(doors) - 1)
    new_choice = doors.pop(new_choice)

    # Final result.
    return [choice == 1, new_choice == 1]


n_doors = input("Number of doors [default=3]: ")
n_doors = max(int(n_doors) if n_doors else 3, 3)

n_samples = 10 ** 5

n_success_not_changing = 0
n_success_changing = 0

print(f"\nTesting for {n_doors} doors using {n_samples} samples...\n")

for i in range(n_samples):
    not_changing, changing = monty_hall(n_doors)
    
    n_success_not_changing += int(not_changing)
    n_success_changing += int(changing)

print("Result (keeping the first choice):", n_success_not_changing / n_samples)
print("Result (changing the door):", n_success_changing / n_samples)

