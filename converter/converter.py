import imageio
import os
import winsound
import argparse
from datetime import datetime

def video_converter(vid_path,format):
    vid_filename=os.path.basename(str(vid_path))
    ndex=vid_filename.find('.')
    output_path=vid_filename[:ndex]+'.'+str(format)
    print(output_path)
    print(f'converting {vid_path} to {output_path}....')
    start=datetime.now()

    try:
        reader=imageio.get_reader(vid_path)
        fps=reader.get_meta_data()['fps']

        writer=imageio.get_writer(output_path,fps=fps,mode='I')

        for frame in reader:
            writer.append_data(frame)

        duration=1000 #milliseconds
        freq=440 #hz
        winsound.Beep(duration,freq)
        end=datetime.now()
        print(f"Conversion took {end-start} hours")
    except FileNotFoundError :
        print('File not found , check path')
    except ValueError:
        print('Unsupported format provided')


def image_converter(image,format):
    output_path=os.path.splitext(image)[0]+'.'+str(format)
    print(f'converting {image} to {output_path}....')
    start=datetime.now()

    try:
        reader = imageio.imread(image)
        imageio.imwrite(output_path, reader)
        duration=1000 #milliseconds
        freq=440 #hz
        winsound.Beep(duration,freq)
        end=datetime.now()
        print(f"Conversion took {end-start} hours")
    except FileNotFoundError:
        print ('File not found , check path')
    except ValueError:
        print('Unsupported format provided')

def parser():
    parser=argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i","--image",help="image converter",action="store_true")
    group.add_argument("-v","--video",help="video converter",action="store_true")
    parser.add_argument("-p","--path",help="input file path (full path)",action="store")
    parser.add_argument("-f","--format",help="target format",action="store")

    args=parser.parse_args()

    if args.image:
        path_missing=(args.path==None)
        format_missing=(args.format==None)
        if path_missing:
            print("specify full path with -p")
        if format_missing:
            print("specify targeted format with -f")
        if path_missing or format_missing:
            pass
        else:
            image_converter(args.path,args.format)
    elif args.video:
        path_missing=(args.path==None)
        format_missing=(args.format==None)
        if path_missing:
            print("specify full path with -p")
        if format_missing:
            print("specify targeted format with -f")
        if path_missing or format_missing:
            pass
        else:
            video_converter(args.path,args.format)
    else:
        print("specify -i(image conversion) or -v(video conversion) ")

if __name__=='__main__':
    parser()
