from PIL import Image
from process_image import get_code_from_image


def split_png(f):
	n = f.n_frames
	for i in range(n):
		f.seek(i)
		f.save("misc3_%d.png" % (i))


def print_infos(f):
	n = f.n_frames
	for i in range(n):
		f.seek(i)
		print(f"frame:{i}\t duration:{f.info}")


def get_longest_frame_number(f):
	frame = 0
	max_duration = 0
	n = f.n_frames
	for i in range(n):
		f.seek(i)
		d = f.info["duration"]
		if d > max_duration:
			frame = i
			max_duration = d
	return frame


def get_longest_frame(f):
	n = get_longest_frame_number(f)
	f.seek(n)
	return f


# this is the function
def get_code_from_gif(f):
	f = get_longest_frame(f)
	# f.show()
	code = get_code_from_image(f)
	return code


if __name__ == "__main__":
	file_path = "../example/misc1.gif"
	# file_path = "H:/git/1point3acres/example/misc1.gif"
	f = Image.open(file_path)
	# split_png(f)
	# print_infos(f)
	frame = get_longest_frame_number(f)
	print("the frame:", frame)
	code = get_code_from_gif(f)
	print(code)
	f.close()
