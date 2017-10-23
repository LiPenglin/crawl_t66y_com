

def test(a):
    try:
        a = a + 1
    except:
        print('error')
        return
    print('end')

if __name__ == '__main__':
    test('a')