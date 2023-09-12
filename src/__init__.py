"""
"""

from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.components.camera import Camera
from .replay_module import Replay

Registry.register_resource_creator(Camera.SUBTYPE, Replay.MODEL, ResourceCreatorRegistration(Replay.new, Replay.validate_config))