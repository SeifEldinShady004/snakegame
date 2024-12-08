import random
import curses
import time
time.sleep(1) 

def main(screen):
    curses.curs_set(0)  
    screen_height, screen_width = screen.getmaxyx()  


    window = curses.newwin(screen_height, screen_width, 0, 0)
    window.keypad(1) 
    window.timeout(100) 


    snk_x = screen_width // 4
    snk_y = screen_height // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]


    food = [screen_height // 2, screen_width // 2]
    window.addch(food[0], food[1], curses.ACS_PI) 


    key = curses.KEY_RIGHT
    previous_key = key

    score = 0
    pause = False


    window.border(0)


    while True:

        window.addstr(0, 2, f'Score: {score} ')


        next_key = window.getch()


        if next_key == ord('q') or next_key == ord('Q'):
            break


        if next_key == ord('p') or next_key == ord('P'):
            pause = not pause

        if pause:
            window.addstr(screen_height // 2, screen_width // 2 - 5, "PAUSED")
            window.refresh()
            continue


        if next_key != -1 and next_key != ord('p') and next_key != ord('q'):
            if (key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT) or \
               (key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or \
               (key == curses.KEY_UP and next_key != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and next_key != curses.KEY_UP):
                key = next_key

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1

        if (new_head[0] in [0, screen_height - 1] or
            new_head[1] in [0, screen_width - 1] or
            new_head in snake):
            curses.endwin()
            quit()

        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            window.timeout(100 - (len(snake) // 5 + len(snake) // 10) % 100) 


            food = None
            while food is None:
                new_food = [
                    random.randint(1, screen_height - 2),
                    random.randint(1, screen_width - 2)
                ]
                food = new_food if new_food not in snake else None
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)


curses.wrapper(main)