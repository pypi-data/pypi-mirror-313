import glob
from PIL import Image

class GIFConverter:
    """
    Image to GIF converter
    """
    def __init__(self, path_in=None, path_out=None, resize=(320, 240)) :
        """
        :param path_in: 원본 여러 이미지 경로 (images/*.png)
        :param path_out: 결과 이미지 경로 (output/filename.gif)
        :param resize:  리사이크 크기((320,240))
        """
        self.path_in = path_in or './images/*.png'
        self.path_out = path_out or './output/filename.gif'
        self.resize = resize

    def convert(self):
        """
        GIF 이미지 변환 수행
        """
        print(self.path_in, self.path_out, self.resize)
        img, *images = [Image.open(f).resize(self.resize) for f in sorted(glob.glob(self.path_in))]
        try:
            img.save(
                fp=self.path_out,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=500,
                loop=0,
            )
        except IOError as e:
            print("Converter Error: ", e)
        except Exception as e:
            print(e)

        print("{} created successfully".format(self.path_out))

if __name__ == '__main__':
    c = GIFConverter('./project/images/*.png', './project/image_out/filename.gif', resize=(320, 240))
    c.convert()
    print(GIFConverter.__doc__)


