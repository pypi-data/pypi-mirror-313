"""


Poselib Operators
*****************

:func:`apply_pose_asset`

:func:`blend_pose_asset`

:func:`convert_old_object_poselib`

:func:`convert_old_poselib`

:func:`copy_as_asset`

:func:`create_pose_asset`

:func:`paste_asset`

:func:`pose_asset_select_bones`

:func:`restore_previous_action`

"""

import typing

def apply_pose_asset(*args, blend_factor: float = 1.0, flipped: bool = False) -> None:

  """

  Apply the given Pose Action to the rig

  """

  ...

def blend_pose_asset(*args, blend_factor: float = 0.0, flipped: bool = False, release_confirm: bool = False) -> None:

  """

  Blend the given Pose Action to the rig

  """

  ...

def convert_old_object_poselib() -> None:

  """

  Create a pose asset for each pose marker in this legacy pose library data-block

  """

  ...

def convert_old_poselib() -> None:

  """

  Create a pose asset for each pose marker in the current action

  """

  ...

def copy_as_asset() -> None:

  """

  Create a new pose asset on the clipboard, to be pasted into an Asset Browser

  """

  ...

def create_pose_asset(*args, pose_name: str = '', activate_new_action: bool = True) -> None:

  """

  Create a new Action that contains the pose of the selected bones, and mark it as Asset. The asset will be stored in the current blend file

  """

  ...

def paste_asset() -> None:

  """

  Paste the Asset that was previously copied using Copy As Asset

  """

  ...

def pose_asset_select_bones(*args, select: bool = True, flipped: bool = False) -> None:

  """

  Select those bones that are used in this pose

  """

  ...

def restore_previous_action() -> None:

  """

  Switch back to the previous Action, after creating a pose asset

  """

  ...
