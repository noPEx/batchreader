from multiprocessing import Process, Pipe


def f(conn):
	for i in range(10):
		conn.send('hello:%s'%(i))
	conn.close()


if __name__ == "__main__":
	p_c, ch_c = Pipe()

	pr = Process(target=f, args=(ch_c,))
	pr.start()
	for i in range(10):
		print p_c.recv()

	pr.join()
