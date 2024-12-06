### `__init__.py`

Create an `__init__.py` file in the `coordinate_system/` directory to mark it as a package. You can add the following content to the `__init__.py` file:

```python
from .coord import coord3

# Coordinate System Package

This package provides a mathematical framework for defining and manipulating three-dimensional coordinate systems in Python. It includes the `vec3`, `quaternion`, and `coord3` classes, allowing users to work with vectors, rotations, and coordinate transformations efficiently.

## Installation

You can install the package using pip:

```bash
pip install coordinate-system
```

## Overview

The `Coord` system is based on group theory and defines a coordinate system in three-dimensional space. It includes an origin, three directional axes, and scaling components that correspond to transformations like translation, rotation, and scaling. This package provides methods to construct coordinate systems from various parameters and perform operations to convert between different coordinate systems.

## Classes

### vec3

Represents a three-dimensional vector.

- **Constructors:**
  - `vec3()` - Initializes a zero vector.
  - `vec3(float x, float y, float z)` - Initializes with specified components.

- **Properties:**
  - `x`: Component along the x-axis.
  - `y`: Component along the y-axis.
  - `z`: Component along the z-axis.

- **Methods:**
  - `__repr__()`: Returns a string representation of the vector.
  - `__add__(vec3 other)`: Computes the sum of two vectors.
  - `__sub__(vec3 other)`: Computes the difference between two vectors.
  - `__mul__(float scalar)`: Multiplies the vector by a scalar.
  - `__truediv__(float scalar)`: Divides the vector by a scalar.
  - `dot(vec3 other)`: Computes the dot product with another vector.
  - `cross(vec3 other)`: Computes the cross product with another vector.
  - `length()`: Returns the length (magnitude) of the vector.
  - `normalize()`: Normalizes the vector to unit length.
  - `isINF()`: Checks if any component is infinite.
  - `flipX()`, `flipY()`, `flipZ()`: Flips the respective component.
  - `serialise()`: Serializes the vector.
  - `len()`, `lenxy()`, `sqrlen()`, `abslen()`: Various length-related calculations.
  - `norm()`, `normcopy()`, `normalized()`: Normalization methods.
  - `min3(vec3 a, vec3 b, vec3 c)`: Returns the minimum of three vectors.
  - `max3(vec3 a, vec3 b, vec3 c)`: Returns the maximum of three vectors.
  - `rnd()`: Generates a random vector.
  - `lerp(vec3 a, vec3 b, float t)`: Performs linear interpolation between two vectors.
  - `angle(vec3 a, vec3 b)`: Computes the angle between two vectors.

### quat

Represents a quaternion for 3D rotations.

- **Constructors:**
  - `quat()` - Initializes to identity quaternion.
  - `quat(float w, float x, float y, float z)` - Initializes with specified components.
  - `quat(float angle, const vec3& axis)` - Creates a quaternion from an angle and an axis.
  - `quat(const vec3& v1, const vec3& v2)` - Creates a quaternion from two vectors.

- **Properties:**
  - `w`: Scalar component of the quaternion.
  - `x`, `y`, `z`: Vector components of the quaternion.

- **Methods:**
  - `__repr__()`: Returns a string representation of the quaternion.
  - `__add__(quaternion other)`: Computes the sum of two quaternions.
  - `__mul__(quaternion other)`: Multiplies two quaternions.
  - `__mul__(vec3 vector)`: Rotates a vector using the quaternion.
  - `__truediv__(quaternion other)`: Divides one quaternion by another.
  - `normalize()`: Normalizes the quaternion.
  - `normalized()`: Returns a normalized copy of the quaternion.
  - `conj()`: Returns the conjugate of the quaternion.
  - `conjcopy()`: Returns a copy of the conjugate quaternion.
  - `length()`: Returns the length of the quaternion.
  - `dot(quaternion other)`: Computes the dot product with another quaternion.
  - `angle_to(quaternion other)`: Computes the angle to another quaternion.
  - `from_eulers(float pitch, float yaw, float roll)`: Creates a quaternion from Euler angles.
  - `fromvectors(vec3 v1, vec3 v2)`: Creates a quaternion from two vectors.
  - `ang_axis(float angle, vec3 axis)`: Creates a quaternion from an angle and axis.
  - `exp()`: Computes the exponential of the quaternion.
  - `log()`: Computes the logarithm of the quaternion.
  - `spherical_cubic_interpolate()`: Performs spherical cubic interpolation.

### coord3

Represents a 3D coordinate system.

- **Constructors:**
  - `coord3()` - Default constructor.
  - `coord3(real x, real y, real z)` - Initializes with specified coordinates.
  - `coord3(real x, real y, real z, real sx, real sy, real sz)` - Initializes with position and scaling.
  - `coord3(const vec3& position)` - Initializes from a position vector.
  - `coord3(const vec3& ux, const vec3& uy, const vec3& uz)` - Initializes from three axis vectors.
  - `coord3(real angle, const vec3& axis)` - Initializes from an angle and axis.
  - `coord3(const quaternion& q)` - Initializes from a quaternion.
  - `coord3(const vec3& position, const quaternion& q, const vec3& scale)` - Initializes from position, quaternion, and scale.

- **Properties:**
  - `o`: Origin vector.
  - `ux`, `uy`, `uz`: Directional axes.
  - `s`: Scale vector.

- **Methods:**
  - `__add__(coord3 other)`: Computes the sum of two coordinate systems.
  - `__sub__(coord3 other)`: Computes the difference between two coordinate systems.
  - `__mul__(coord3 other)`: Multiplies two coordinate systems.
  - `__mul__(vec3 vector)`: Transforms a vector using the coordinate system.
  - `__truediv__(coord3 other)`: Divides one coordinate system by another.
  - `__eq__(coord3 other)`: Checks for equality between two coordinate systems.
  - `__ne__(coord3 other)`: Checks for inequality between two coordinate systems.
  - `pos()`: Returns the position vector.
  - `tovec()`: Converts the coordinate system to a vector.
  - `pose()`: Returns the pose of the coordinate system.
  - `rot(real angle, const vec3& axis)`: Rotates the coordinate system by an angle around an axis.
  - `rot(const quaternion& q)`: Rotates the coordinate system by a quaternion.
  - `rotated(real angle, const vec3& axis)`: Returns a new rotated coordinate system.
  - `rotated(const quaternion& q)`: Returns a new coordinate system rotated by a quaternion.
  - `equal_dirs(coord3 other)`: Checks if the directional axes are equal.
  - `hash()`: Returns a hash of the coordinate system.
  - `serialise()`: Serializes the coordinate system.
  - `dump()`: Dumps information about the coordinate system.
  - `lie_cross(coord3 other)`: Computes the Lie cross product.
  - `grad()`: Computes the gradient.
  - `reverse()`: Reverses the coordinate system.
  - `reversed()`: Returns a new reversed coordinate system.
  - `cross(coord3 other)`: Computes the cross product with another coordinate system.
  - `cross(vec3 vector)`: Computes the cross product with a vector.

## Usage

### Creating a Coordinate System

You can create a coordinate system using various constructors:

```python
from coordinate_system import coord3, vec3

# Create a coordinate system from three axes
C = coord3.from_axes(vec3(1, 0, 0), vec3(0, 1, 0), vec3(0, 0, 1))

# Create a coordinate system from an angle and axis
C_angle = coord3.from_angle(90, vec3(0, 0, 1))
```

### Transforming Vectors

You can transform vectors between different coordinate systems:

```python
V1 = vec3(1, 2, 3)
C1 = coord3(...)  # Some coordinate system
C0 = coord3(...)  # Another coordinate system

# Transforming from local to parent coordinate system
V0 = V1 * C1

# Projecting from parent to local coordinate system
V1 = V0 / C1
```

## Common Scenarios

### Converting Between Coordinate Systems

```python
# Convert a vector from world to local coordinates
VL = Vw / C
Vw = VL * C
```

### Using in Multi-Node Hierarchies

```python
V1 = V4 * C4 * C3 * C2 
V4 = V1 / C2 / C3 / C4
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.