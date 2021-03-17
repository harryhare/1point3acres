from PIL import Image
import pytesseract

if __name__ == "__main__":
	img_path = 'shard(30, 18).png'
	text = pytesseract.image_to_string(Image.open(img_path), lang="eng", config="--psm 10")
	print(text)
