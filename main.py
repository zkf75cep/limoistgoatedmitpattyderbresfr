from Website_Klicker_Funktion import main
import time, random, os

#pfad_des_ordners = "C:/Users/Noah/Downloads/Website_Klicker"
pfad_des_ordners = os.path.dirname(os.path.abspath(__file__))

sleeping_time = random.choice([10,20,30,40,50,60])


print("\nWEBSITE OPENER © NOAH \n")
user_input = input("Wie oft?\n")
print("\n Starting...")

times = 0
while times < (int(user_input)):
    times += 1

    try:
        main(pfad_des_ordners)
        print(f"Website {times} finished!")
    except(TimeoutError, AttributeError, OSError):
        print(f"Error occured after {times} Runs :(")
    time.sleep(sleeping_time)

print(f"Finished with {times} Runs!\n")
print("© NOAH")

time.sleep(100)