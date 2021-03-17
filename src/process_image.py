from PIL import Image
import pytesseract


def print_color_statistic(f):
	width, height = f.size
	c_map = {}
	for x in range(width):
		for y in range(height):
			c = f.getpixel((x, y))
			if c in c_map.keys():
				c_map[c] = c_map[c] + 1
			else:
				c_map[c] = 1
	print(c_map)
	for k in c_map:
		if c_map[k] > 200:
			print(k, c_map[k])


visit = []


def dfs(f, x, y, c, range_x, range_y):
	global visit
	if x < 0 or x > f.size[0] - 1 or y < 0 or y > f.size[1] - 1:
		return 0
	if f.getpixel((x, y)) != c:
		return 0
	if visit[y][x] == 1:
		return 0
	count = 1
	visit[y][x] = 1
	range_x[0] = min(range_x[0], x)
	range_x[1] = max(range_x[1], x)
	range_y[0] = min(range_y[0], y)
	range_y[1] = max(range_y[1], y)
	count += dfs(f, x - 1, y, c, range_x, range_y)
	count += dfs(f, x + 1, y, c, range_x, range_y)
	count += dfs(f, x, y - 1, c, range_x, range_y)
	count += dfs(f, x, y + 1, c, range_x, range_y)
	return count


# def dfs_fill(fin,fout,c):


def get_shards(f) -> list:
	width, height = f.size
	global visit
	visit = [[0 for i in range(width)] for j in range(height)]
	shard_list = []
	for y in range(height):
		for x in range(width):
			if visit[y][x] == 0:
				range_x = [x, x]
				range_y = [y, y]
				count = dfs(f, x, y, f.getpixel((x, y)), range_x, range_y)
				if count > 80:
					shard_list.append({"key": (x, y), "count": count, "range_x": range_x, "range_y": range_y})
	shard_list.sort(reverse=True, key=lambda x: x["count"])
	return shard_list


def get_charaters(shard_list: list, f) -> map:
	characters = {}
	for shard in shard_list:
		c = f.getpixel(shard["key"])
		range_x = shard["range_x"]
		range_y = shard["range_y"]
		print(shard, f"{range_x[1] - range_x[0]}x{range_y[1] - range_y[0]}")

		padding = 5
		offset_x = range_x[0]
		offset_y = range_y[0]
		w = range_x[1] - range_x[0] + 1 + padding * 2
		h = range_y[1] - range_y[0] + 1 + padding * 2
		if range_x[1] - range_x[0] > 25 or range_y[1] - range_y[0] > 25:
			continue
		img = Image.new('RGB', (w, h), color=(255, 255, 255))
		# todo: use dfs_fill instead
		for x in range(range_x[1] - range_x[0] + 1):
			for y in range(range_y[1] - range_y[0] + 1):
				if f.getpixel((x + range_x[0], y + range_y[0])) == c:
					img.putpixel((x + padding, y + padding), (0, 0, 0))
		text = pytesseract.image_to_string(img, lang="eng", config="--psm 10")
		if len(text) == 0:
			continue
		if not text[0].isalnum():
			continue
		characters[range_x[0]] = text
		# img.save(f'shard{k}.png')
		# img.close()
		if len(characters) >= 4:
			break
	return characters


def get_code(characters):
	result = ""
	keys = sorted(characters.keys())
	for k in keys:
		result += characters[k][0]
	return result


# this is the function
def get_code_from_image(f):
	shard_list = get_shards(f)
	print(shard_list)
	characters = get_charaters(shard_list, f)
	print(characters)
	code = get_code(characters)
	print(code)
	return code


if __name__ == "__main__":
	file_path = "../example/example1.png"
	# file_path = "H:/git/1point3acres/example/example1.png"
	f = Image.open(file_path)
	# f.show()
	print(get_code_from_image(f))

# todo：
#  相似颜色合并
#  dfs_fill
