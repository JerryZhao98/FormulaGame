from formula_game_functions import *
import gc, time


# of course you could make your code suited to these specific OR trees but
# then you'd be lying to yourself
SIMPLE_TREE = build_tree('(a+(b+c))')
MEDIUM_TREE = build_tree('(a+(b+(c+(d+(e+(f+(g+(h+(i+(j+(k+(l+(m+(n+o)' +
                         ')))))))))))))')
HARD_TREE = build_tree('(a+(b+(c+(d+(e+(f+(g+(h+(i+(j+(k+(l+(m+(n+' +
                       '(o+(p+(q+(r+(s+(t+(u+(v+(w+(x+(y+z)))))))))' +
                       '))))))))))))))))')


if __name__ == '__main__':
    # play2win is not supposed to be linear
    gc.disable()
    total_time = time.time()
    play2win(SIMPLE_TREE, 'EEE', 'abc', '')
    play2win(SIMPLE_TREE, 'EEE', 'abc', '11')
    play2win(SIMPLE_TREE, 'EEE', 'abc', '00')
    play2win(SIMPLE_TREE, 'EEA', 'abc', '')
    play2win(SIMPLE_TREE, 'AEE', 'abc', '')
    print('1/3 Completed, EASY_TREE, Time: ' + str(time.time()-total_time) +
          ' seconds')
    temp_time = time.time()
    play2win(MEDIUM_TREE, 'AEAEAEAEAEAEAEA', 'abcdefghijklmno', '000000')
    play2win(MEDIUM_TREE, 'EEEEEEEEEEEEEEE', 'abcdefghijklmno', '')
    play2win(MEDIUM_TREE, 'AEAAAAAAAAAAAAE', 'abcdefghijklmno', '')
    play2win(MEDIUM_TREE, 'AAAAAAAAAAAAAAE', 'abcdefghijklmno', '')
    play2win(MEDIUM_TREE, 'AAAAAAAAAAAAAAA', 'abcdefghijklmno', '1')
    play2win(MEDIUM_TREE, 'AEAEAEAEAEAEAEA', 'abcdefghijklmno', '')
    print('2/3 Completed, MEDIUM_TREE, Time: ' + str(time.time()-temp_time) +
          ' seconds')
    temp_time = time.time()
    play2win(HARD_TREE, 'EEEEEEEEEEEEEEEEEEEEEEEEEE',
             'abcdefghijklmnopqrstuvwxyz', '')
    play2win(HARD_TREE, 'AEEEEEEAAAAEEEEEAAAEEEEEEE',
             'abcdefghijklmnopqrstuvwxyz', '')
    play2win(HARD_TREE, 'AAAAAAAAAAAAAAAAAAAAAAAAAA',
             'abcdefghijklmnopqrstuvwxyz', '')
    play2win(HARD_TREE, 'EAEAEAEAEAEAEAEAEAEAEAEAEA',
             'abcdefghijklmnopqrstuvwxyz', '')
    play2win(HARD_TREE, 'AAAAAAAAAAAAAAAAAAAAAAAAAA',
             'abcdefghijklmnopqrstuvwxyz', '000000001')
    play2win(HARD_TREE, 'AAAAAAAAAAAAAAAAAAAAAAAAAE',
             'abcdefghijklmnopqrstuvwxyz', '000000000')
    print('3/3 Completed, HARD_TREE, Time: ' + str(time.time()-temp_time) +
          ' seconds')
    total_time = time.time() - total_time
    print('Total Time used: ' + str(total_time) + ' seconds')
    # if you're wondering, EASY should be done in less than a second,
    # MEDIUM should be done in a reasonable time less than 5 seconds
    # HARD if completed at all means you're on the right track, those who
    # did "try all permutations" will probably take forever, doing 67,108,864
    # permutations 6 times. But even so you could wait for half a minute before
    # calling it quites
    # you must get 1/3 done in less then a second
    # you should get 2/3 done in less than 5 seconds
    # you should try to get 3/3 done in less than 15 seconds