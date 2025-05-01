from gameboard import GameBoard

def main():
    time = 0
    hour = 3600
    board = GameBoard(hour)
    sum = 0
    num_cars = 0
    while time < hour:
        commutes = board.time_seg(time)
        if(len(commutes)>0):
            for i in range(len(commutes)):
                sum += commutes[i]
                num_cars += 1
        if time%100 == 0:
            board.print_all()
        time += 1
    average_commute = sum/num_cars
    print("The average commute time is " + average_commute + "\n")

main()