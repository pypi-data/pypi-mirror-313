import os


###line counts based on given file extension --  MM

def countlines(start,lines=0, header=False, begin_start=None,extentsion='.py'):
    # if header:
    #     print('{:>10} |{:>10} | {:<20}'.format('Added', 'Total', 'filename'))
    #     print('{:->11}|{:->11}|{:->20}'.format('', '', ''))

    # lang_extensions = {
    # #     'nodejs':'.js',
    # #     'python':'.py',
    # #     'php':'.php',
    # #     'ruby':'.rb',
    # #     'go':'.go',
    # #     'java':'.java',
    # #     'python-snyk':'.py',
    # #     'node-snyk':'.js',
    # #     'ruby-snyk':'.rb',
    # #     'csharp':'.cs'
    # # }

    # # #print(lang_extensions['js'])





    if extentsion is None:
        print(extentsion)
        return 0

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isfile(thing):
            if thing.endswith(extentsion):
                with open(thing, 'r') as f:
                    newlines = f.readlines()
                    newlines = len(newlines)
                    lines += newlines

                    if begin_start is not None:
                        reldir_of_thing = '.' + thing.replace(begin_start, '')
                    else:
                        reldir_of_thing = '.' + thing.replace(start, '')

                    # print('{:>10} |{:>10} | {:<20}'.format(
                    #         newlines, lines, reldir_of_thing))


    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isdir(thing):
            lines = countlines(thing, lines, header=False, begin_start=start)

    return lines




#print(countlines('/home/boxuser/box/Vuln-code/',extentsion='.rb'))