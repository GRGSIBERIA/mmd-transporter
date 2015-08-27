/**
 * Linear Algebra 
 */
#ifndef MESH_IO_LA_H_INCLUDED
#define MESH_IO_LA_H_INCLUDED

#include <ostream>

namespace meshio {
  struct Vector2
  {
    float x;
    float y;

    Vector2()
    {}

    Vector2(float _x, float _y)
      : x(_x), y(_y)
    {}
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const Vector2 &rhs)
  {
    return os
      << '[' << rhs.x << ',' << rhs.y << ']';
  }
#endif

  struct Vector3
  {
    float x;
    float y;
    float z;

    Vector3()
    {}

    Vector3(float _x, float _y, float _z)
      : x(_x), y(_y), z(_z)
    {}

    bool operator==(const Vector3 &rhs)const
    {
      return x==rhs.x && y==rhs.y && z==rhs.z;
    }

    Vector3 operator+(const Vector3 &rhs)
    {
      return Vector3(x+rhs.x, y+rhs.y, z+rhs.z);
    }

    Vector3 operator-(const Vector3 &rhs)
    {
      return Vector3(x-rhs.x, y-rhs.y, z-rhs.z);
    }
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const Vector3 &rhs)
  {
    return os
      << '[' << rhs.x << ',' << rhs.y << ',' << rhs.z << ']';
  }
#endif


  struct Vector4
  {
    float x;
    float y;
    float z;
    float w;

    Vector4()
    {}

    Vector4(float _x, float _y, float _z, float _w)
      : x(_x), y(_y), z(_z), w(_w)
    {}
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const Vector4 &rhs)
  {
    return os
      << '[' << rhs.x << ',' << rhs.y << ',' << rhs.z << ',' << rhs.w << ']';
  }
#endif


  struct Quaternion
  {
    float x;
    float y;
    float z;
    float w;

    Quaternion()
    {}

    Quaternion(float _x, float _y, float _z, float _w)
      : x(_x), y(_y), z(_z), w(_w)
    {}

    float dot(const Quaternion &rhs)
    {
      return x*rhs.x + y*rhs.y + z*rhs.z + w*rhs.w;
    }
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const Quaternion &rhs)
  {
    return os
      << '[' << rhs.x << ',' << rhs.y << ',' << rhs.z << ',' << rhs.w << ']';
  }
#endif

}

#endif // MESH_IO_LA_H_INCLUDED
