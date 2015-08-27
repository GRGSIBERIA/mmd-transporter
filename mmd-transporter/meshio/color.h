/**
 * Color
 */
#ifndef MESH_IO_COLOR_H_INCLUDED
#define MESH_IO_COLOR_H_INCLUDED

namespace meshio {

  struct bRGBA
  {
    int r;
    int g;
    int b;
    int a;

    bRGBA()
    {}

    bRGBA(int _r, int _g, int _b, int _a)
      : r(_r), g(_g), b(_b), a(_a)
    {}

    static bRGBA createFromUInt(unsigned int uint)
    {
      return bRGBA(
          uint & 0x000000FF,
          uint & 0x0000FF00 >> 8,
          uint & 0x00FF0000 >> 16,
          uint & 0xFF000000 >> 24
          );
    }
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const bRGBA &rhs)
  {
    return os
      << '[' << rhs.r << ',' << rhs.g << ',' << rhs.b << ',' << rhs.a << ']';
  }
#endif


  //! Float RGBA
  struct fRGBA
  {
    float r;
    float g;
    float b;
    float a;

    fRGBA()
    {}

    fRGBA(float _r, float _g, float _b, float _a)
      : r(_r), g(_g), b(_b), a(_a)
    {}

    static fRGBA createFromUInt(unsigned int uint)
    {
      return fRGBA(
          (uint & 0x000000FF) / 255.0f,
          (uint & 0x0000FF00 >> 8) / 255.0f,
          (uint & 0x00FF0000 >> 16) / 255.0f,
          (uint & 0xFF000000 >> 24) / 255.0f
          );
    }
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const fRGBA &rhs)
  {
    return os
      << '[' << rhs.r << ',' << rhs.g << ',' << rhs.b << ',' << rhs.a << ']';
  }
#endif


  //! Float RGB
  struct fRGB
  {
    float r;
    float g;
    float b;
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const fRGB &rhs)
  {
    return os
      << '[' << rhs.r << ',' << rhs.g << ',' << rhs.b << ',' << ']';
  }
#endif


} // namespace meshio

#endif // MESH_IO_COLOR_H_INCLUDED
