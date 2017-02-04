from bling import Bling

bling = Bling()

print bling.menu()

done = False
while not done:
    try:
        input = raw_input('Enter your selection: ')
        if input == '?':
            print bling.menu()
        elif input == '':
            bling.stop_animation()
        elif input.lower() == 'q':
            done = True
        else:
            try:
                result = bling.menu_select(int(input))
                print result
            except ValueError:
                print 'Invalid input choose a number: %s' % input

    except KeyboardInterrupt:
        done = True

print '\nDone!'
