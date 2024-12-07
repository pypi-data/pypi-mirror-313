"""
This module contains migration functions that can be used to refactor code in a backwards compatible way.
"""

import functools
import sys
import re
from pathlib import Path
import itertools
from abc import ABC, abstractmethod
from openplx.Core import RefactorReplaceOp, RefactorToolkit


def migration(from_version: str, to_version: str, order: int = 0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        wrapper.openplx_from_version = from_version
        wrapper.openplx_to_version = to_version
        wrapper.openplx_order = order
        return wrapper

    return decorator

@migration("0.9.3", "0.10.0")
def snakecaseify_methods_093(documents): # pylint: disable=too-many-statements
    ops = []
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Vec3.fromXYZ", "from_xyz"))
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Vec3.angleBetweenVectors", "angle_between_vectors"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Vec3.getOrthogonalUnitVector", "get_orthogonal_unit_vector"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(documents, "Math.Quat.angleAxis", "angle_axis")
    )
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Quat.fromTo", "from_to"))
    ops.extend(
        RefactorToolkit.renameMethod(documents, "Math.Quat.fromXYZW", "from_xyzw")
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.AffineTransform.fromAxes", "from_axes"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.AffineTransform.inverseOf", "inverse_of"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.AffineTransform.transformVec3Point", "transform_vec3_point"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Math.AffineTransform.transformVec3Vector",
            "transform_vec3_vector",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix3x3.fromRowMajor", "from_row_major"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(documents, "Math.Matrix3x3.fromRows", "from_rows")
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix3x3.fromColumns", "from_columns"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix4x4.fromRowMajor", "from_row_major"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.fromRows", "from_rows")
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix4x4.fromColumns", "from_columns"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix4x4.fromVec3Quat", "from_vec3_quat"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix4x4.getAffineTranslation", "get_affine_translation"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Math.Matrix4x4.getAffineRotation", "get_affine_rotation"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Functions.harmonicMean", "harmonic_mean"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(documents, "Math.Line.fromPoints", "from_points")
    )
    # ValueOutputSignal
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.fromAngle", "from_angle"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromAngularVelocity1D",
            "from_angular_velocity_1d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.fromDistance", "from_distance"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.fromForce1D", "from_force_1d"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromVelocity1D",
            "from_velocity_1d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromTorque1D",
            "from_torque_1d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromAcceleration3D",
            "from_acceleration_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromAngularAcceleration3D",
            "from_angular_acceleration_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromAngularVelocity3D",
            "from_angular_velocity_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.fromForce3D", "from_force_3d"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromTorque3D",
            "from_torque_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromVelocity3D",
            "from_velocity_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.fromPosition3D",
            "from_position_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.fromRPY", "from_rpy"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.isReal", "is_real"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asReal", "as_real"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asVec3", "as_vec3"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asAngle", "as_angle"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asAngularVelocity1D",
            "as_angular_velocity_1d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asDistance", "as_distance"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asForce1D", "as_force_1d"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asVelocity1D",
            "as_velocity_1d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asTorque1D", "as_torque_1d"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asAcceleration3D",
            "as_acceleration_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asAngularAcceleration3D",
            "as_angular_acceleration_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asAngularVelocity3D",
            "as_angular_velocity_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asForce3D", "as_force_3d"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Physics.Signals.ValueOutputSignal.asTorque3D", "as_torque_3d"
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asVelocity3D",
            "as_velocity_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents,
            "Physics.Signals.ValueOutputSignal.asPosition3D",
            "as_position_3d",
        )
    )
    ops.extend(
        RefactorToolkit.renameMethod(
            documents, "Robotics.Signals.RobotInputSignal.fromValues", "from_values"
        )
    )

    # DriveTrain.Signals
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "DriveTrain.Signals.CombustionEngineThrottleInput",
            "Physics.Signals",
            "FractionInput",
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "DriveTrain.Signals.CombustionEngineTorqueOutput",
            "Physics.Signals",
            "Torque1DOutput",
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "DriveTrain.Signals.GearTorqueOutput",
            "Physics.Signals",
            "Torque1DOutput",
        )
    )

    return [ReplaceOp(op) for op in ops]


@migration("0.10.3", "0.11.0")
def migrations_for_0_10_3(documents):
    ops = []
    # Physics3D.Transform -> Math.AffineTransform
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents, "Physics3D.Transform", "Math", "AffineTransform"
        )
    )
    # Robotics.Joints.FlexibleVelocityJoint -> Robotics.Joints.FlexibleAngularVelocityJoint
    ops.extend(
        RefactorToolkit.renameModel(
            documents,
            "Robotics.Joints.FlexibleVelocityJoint",
            "FlexibleAngularVelocityJoint",
        )
    )
    ops.extend(
        RefactorToolkit.renameModel(
            documents,
            "Physics3D.Signals.MateConnector.Velocity3DOutput",
            "LinearVelocity3DOutput",
        )
    )
    return [ReplaceOp(op) for op in ops]


@migration("0.11.0", "0.11.1")
def migrations_for_0_11_0(documents):
    ops = []
    ops.extend(
        RefactorToolkit.renameModel(
            documents,
            "Physics3D.Signals.RigidBodyVelocityOutput",
            "LinearVelocity3DOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.RigidBodyVelocityOutput.rigid_body", "source"
        )
    )
    return [ReplaceOp(op) for op in ops]


@migration("0.12.1", "0.12.2")
def migrations_for_0_12_1(documents):
    ops = []
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.PrismaticVelocityOutput",
            "Physics.Signals",
            "LinearVelocity1DOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.PrismaticVelocityOutput.prismatic", "source"
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents,
            "DriveTrain.ManualClutch.initial_opening_fraction",
            "initial_engagement_fraction",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents,
            "DriveTrain.ManualClutch.opening_fraction_input",
            "engagement_fraction_input",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents,
            "DriveTrain.ManualClutch.opening_fraction_output",
            "engagement_fraction_output",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents,
            "DriveTrain.AutomaticClutch.engage_time",
            "engagement_time",
        )
    )

    return [ReplaceOp(op) for op in ops]


@migration("0.13.1", "0.13.2")
def migrations_for_0_13_1(documents):
    ops = []
    # DriveTrain.Gear -> DriveTrain.FlexibleGear
    ops.extend(
        RefactorToolkit.renameModel(
            documents,
            "DriveTrain.Gear",
            "FlexibleGear",
        )
    )

    return [ReplaceOp(op) for op in ops]

@migration("0.14.0", "0.15.0")
def rename_from_brick_to_openplx(document_path):

    return ChangeExtensionOp(Path(document_path), ".openplx")


@migration("0.15.1", "0.15.2")
def migrations_for_0_15_1(documents):
    ops = []
    ops.extend(
        RefactorToolkit.renameModel(
            documents,
            "Robotics.Joints.TorqueDriveTrain",
            "FlexibleJointDriveTrain",
        )
    )
    ops.extend(
        RefactorToolkit.renameModel(
            documents,
            "Robotics.Joints.AngularVelocityDriveTrain",
            "FlexibleJointDriveTrain",
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.HingeAngularVelocityOutput",
            "Physics.Signals",
            "AngularVelocity1DOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.HingeAngularVelocityOutput.hinge", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "DriveTrain.Signals.TorqueMotorInput",
            "Physics.Signals",
            "Torque1DInput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "DriveTrain.Signals.TorqueMotorInput.motor", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.LinearSpringPositionInput",
            "Physics.Signals",
            "Position1DInput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.LinearSpringPositionInput.spring", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.TorsionSpringAngleInput",
            "Physics.Signals",
            "AngleInput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.TorsionSpringAngleInput.spring", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.RigidBodyRPYOutput",
            "Physics3D.Signals",
            "RPYOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.RigidBodyRPYOutput.rigid_body", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.RigidBodyPositionOutput",
            "Physics3D.Signals",
            "Position3DOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.RigidBodyPositionOutput.rigid_body", "source"
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Interactions.VelocityMotor.desired_speed", "target_speed"
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics1D.Interactions.VelocityMotor.desired_speed", "target_speed"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.RotationalVelocityMotorVelocityInput",
            "Physics.Signals",
            "AngularVelocity1DInput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.RotationalVelocityMotorVelocityInput.motor", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics1D.Signals.RotationalVelocityMotor1DVelocityInput",
            "Physics.Signals",
            "AngularVelocity1DInput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics1D.Signals.RotationalVelocityMotor1DVelocityInput.motor", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics3D.Signals.LinearVelocityMotorVelocityInput",
            "Physics.Signals",
            "LinearVelocity1DInput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics3D.Signals.LinearVelocityMotorVelocityInput.motor", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics1D.Signals.RotationalBodyAngularVelocityOutput",
            "Physics.Signals",
            "AngularVelocity1DOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics1D.Signals.RotationalBodyAngularVelocityOutput.body", "source"
        )
    )
    ops.extend(
        RefactorToolkit.moveAndRenameModel(
            documents,
            "Physics1D.Signals.RotationalBodyAngleOutput",
            "Physics.Signals",
            "AngleOutput",
        )
    )
    ops.extend(
        RefactorToolkit.renameAttribute(
            documents, "Physics1D.Signals.RotationalBodyAngleOutput.body", "source"
        )
    )

    return [ReplaceOp(op) for op in ops]


def split_version(v):
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", v)

    if not match:
        raise ValueError("Invalid version format")

    return tuple(int(part) for part in match.groups())


def collect_migrations(from_version, to_version):
    migrations = filter(
        lambda obj: (
            callable(obj)
            and hasattr(obj, "openplx_from_version")
            and hasattr(obj, "openplx_to_version")
            and hasattr(obj, "openplx_order")
            and split_version(from_version) <= split_version(obj.openplx_from_version)
            and split_version(obj.openplx_from_version) < split_version(to_version)
        ),
        [obj for _, obj in globals().items()],
    )

    return sorted(list(migrations), key=lambda m: split_version(m.openplx_from_version))


class MigrateOp(ABC):  # pylint: disable=R0903 # Too few public methods
    @abstractmethod
    def apply_to(self, lines, offset):
        pass


class ChangeExtensionOp(MigrateOp):
    def __init__(self, path: Path, new_extension: str):
        self.path = path
        self.new_extension = new_extension

    def __str__(self):
        return f"{{ {self.path}, {self.new_extension} }}"

    def apply_to(self, _lines, _offset):
        self.path.rename(self.path.with_suffix(self.new_extension))

class ReplaceOp(MigrateOp):
    def __init__(self, op: RefactorReplaceOp):
        self.path = Path(op.source_id)
        self.from_line = op.from_line
        self.from_column = op.from_column
        self.end_line = op.end_line
        self.end_column = op.end_column
        self.new_content = op.new_content

    def __str__(self):
        return f"{{{self.path}, {self.from_line}, {self.from_column}, {self.end_line}, {self.end_column}, {self.new_content} }}"

    @staticmethod
    def apply_many(ops, lines):
        # There can be multiple ops per line, we need to run them in order sorted by column
        for _, line_group in itertools.groupby(ops, lambda op: op.from_line):
            offset = 0
            for op in sorted(line_group, key=lambda op: op.from_column):
                lines = op.apply_to(lines, offset)
                offset += len(op.new_content) - op.end_column + op.from_column
        return lines

    def apply_to(self, lines, offset):

        if self.end_line != self.from_line:
            print("Multiple line replace ops are not supported", file=sys.stderr)
            return []

        target_line = lines[self.from_line - 1]

        lines[self.from_line - 1] = (
            target_line[: (self.from_column + offset - 1)]
            + self.new_content
            + target_line[(self.end_column + offset - 1) :]
        )

        return lines
