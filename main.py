from gameboard import GameBoard
from gameboard_post_construction import GameBoard2

def main():
    time = 0
    hour = 3600
    board = GameBoard(1.25 * hour)
    sum = 0
    num_cars = 0
    while time < 1.5*hour:
        commutes = board.time_seg(time)
        if time > 0.25 * hour:
            if(len(commutes)>0):
                for i in range(len(commutes)):
                    sum += time - commutes[i].get_spawn_time()
                    num_cars += 1
        if time%599 == 0:
            board.print_all()
        time += 1
    average_commute = sum/num_cars
    print(f"The average commute time is {(average_commute/60):.2f} min\n")
    print(num_cars)

main()