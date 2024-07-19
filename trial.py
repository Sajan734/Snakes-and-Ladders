# def generate_snakes_ladders_board(scalex, scaley, xwidth, ywidth):
#     board = {}
#     x, y = scalex, scaley
#     direction = 1  # 1 for left-to-right, -1 for right-to-left

#     for number in range(100, 0, -1):
#         board[number] = (x, y)
#         x += direction * xwidth

#         if number % 10 == 1 and number != 1:  # At the end of each row
#             direction *= -1
#             x += direction * xwidth  # Adjust x for the next row's direction
#             y += ywidth

#     return board
# # x-axis: 50, 150, 200, 250, 300, 350, 400, 450, 500, 550
# # y-axis: 50, 150, 200, 250, 300, 350, 400, 450, 500, 550

x_vals = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
y_vals = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

numbers_list = []

counter = 100

for y_counter in range(0,10):
    for i in x_vals:
        # print(f"You are on: ", str(counter) + " - " + str({y_vals[y_counter]}))
        numbers_list.append({counter : (i, y_vals[y_counter])})
        counter -= 1


# print(numbers_list)


target = int(input('which number do you want to go to: '))
print(numbers_list[100-target])

with open("data.txt", 'w') as file:
    # for num, coord in sorted(coordinates.items()):
        file.write(f"{num}: {coord}\n")

