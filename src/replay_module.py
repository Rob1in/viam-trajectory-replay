from typing import ClassVar, Optional, Dict, Sequence, Any, Mapping, Tuple, Union

from typing_extensions import Self

from viam.components.camera import Camera,  DistortionParameters, IntrinsicParameters, RawImage
from PIL import Image
from viam.resource.base import ResourceBase
from viam.proto.app.robot import ComponentConfig

from viam.gen.common.v1.common_pb2 import Orientation, Vector3, GeoPoint
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.module.types import Reconfigurable
from viam.resource.types import Model, ModelFamily
import queue
import os
import src.utils as utils

from viam.logging import getLogger
LOGGER = getLogger(__name__)

class Replay(Camera, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viam", "replay"), "camera_replay")
    
    
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        LOGGER.info(f"made it here 1")
        camera = cls(config.name)
        camera.reconfigure(config, dependencies)
        return camera

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        '''
        Returns the dependency
        '''
        path = config.attributes.fields["path"].string_value
        if path == "":
            LOGGER.error("A 'path' attribute is required for replay camera module")
        



    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.Properties(supports_pcd=False, intrinsic_parameters=None, distortion_parameters=None)
        height = config.attributes.fields["height"].number_value
        width = config.attributes.fields["width"].number_value
        path = config.attributes.fields["path"].string_value
        prefix_filter = config.attributes.fields["prefix"].string_value
        jpeg_files = [file for file in os.listdir(path) if ((file.lower().endswith('.jpg') or file.lower().endswith('.jpeg')) and file.lower().startswith(prefix_filter))]
        if not jpeg_files:
            raise ValueError(f"No JPEG files found in the specified folder with names starting with '{prefix_filter}'.")
        jpeg_files = utils.sort_jpeg_names(jpeg_files=jpeg_files)
        # self.images=queue()s
        self.images = []
        self.count =0 
        for file in jpeg_files:
            file_path = os.path.join(path, file)
            try:
                image = Image.open(file_path)
            except:
                continue
            # LOGGER.error(f"TYPE OF IMAGE IS {type(image)}")
            # resized_image = image.resize(width, height, Image.LANCZOS)
            # self.images.put(resized_image)
            # self.images.put(image)
            self.images.append(image)
        LOGGER.info(f"Number of images in the queue is {len(self.images)}")
            
        

    async def get_image(self, mime_type: str = "", *, timeout: Optional[float] = None, **kwargs):
        """Get the next image from the camera as an Image or RawImage.
        Be sure to close the image when finished.

        NOTE: If the mime type is ``image/vnd.viam.dep`` you can use :func:`viam.media.video.RawImage.bytes_to_depth_array`
        to convert the data to a standard representation.

        Args:
            mime_type (str): The desired mime type of the image. This does not guarantee output type

        Returns:
            Image | RawImage: The frame
        """
        img = self.images[self.count]
        self.count +=1
        return img

    async def get_images(self, *, timeout: Optional[float] = None, **kwargs):
        raise NotImplementedError

    async def get_point_cloud(self, *, timeout: Optional[float] = None, **kwargs) -> Tuple[bytes, str]:
        raise NotImplementedError
    
    async def get_properties(self, *, timeout: Optional[float] = None, **kwargs) -> Camera.Properties:
        """
        Get the camera intrinsic parameters and camera distortion parameters

        Returns:
            Properties: The properties of the camera
        """
        ...
        return self.Properties





