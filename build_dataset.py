import asyncio
import argparse


from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera

import time
from PIL import Image
import os
from viam.media.video import CameraMimeType


async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='adpcqgrzdhwa1q42bdeu4bsn6ee7vemx9fjuerl21ux75ydv')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('mac-server-main.wszwqu7wcv.viam.cloud', opts)
async def main(output_folder:str,
               dataset_size:int, 
               frequency:float, 
               prefix:str):
    robot = await connect()
    print(robot.resource_names)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    cam = Camera.from_robot(robot, "cam2")
    for i in range(dataset_size):
        print(f'Doing {i}')
        t1 = time.time()
        img = await cam.get_image(mime_type=CameraMimeType.JPEG)
        # img = await cam.get_image(mime_type="image/jpeg")
        img.save(output_folder+"/" + prefix +str(i)+".jpg")
        dt  = time.time()-t1
        print(f"time to sleep is {frequency-dt}")
        time.sleep(frequency-dt)
        print("finish to sleep")
    # img = await cam.get_image(mime_type=CameraMimeType.JPEG)
    # img.save(output_folder+"/" + prefix +"zebi.jpg")
    # print("zebi")
    # img = await cam.get_image(mime_type=CameraMimeType.JPEG)
    # img.save(output_folder+"/" + prefix +"webi.jpg")
    # print("webi")
    await robot.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build dataset of image to be used for reproducible experiments")
    parser.add_argument("--output_folder", type=str, default="./data", help="Path to the folder containing JPEG images and positions file.")
    parser.add_argument("--frequency", type=float, default=0.1, help="interval in seconds between each image")
    parser.add_argument("--dataset_size", type=int, default = 100, help="# of images")
    parser.add_argument("--prefix", type=str, default="image", )
    args = parser.parse_args()
    asyncio.run(main(output_folder=args.output_folder, 
                     dataset_size=args.dataset_size, 
                     frequency= args.frequency, 
                     prefix = args.prefix))
