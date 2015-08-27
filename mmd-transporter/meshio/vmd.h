/**
 * VMD形式
 * MMDのモーションデータ。
 * バイナリ形式でボーンモーション、表情モーフィング、光源、影のキーフレームが
 * 記録される。
 *
 * 参考サイト
 * http://blog.goo.ne.jp/torisu_tetosuki/e/bc9f1c4d597341b394bd02b64597499d
 * http://atupdate.web.fc2.com/vmd_format.htm
 */
#ifndef MESH_IO_VMD_H_INCLUDED
#define MESH_IO_VMD_H_INCLUDED 

#include <ostream>
#include <vector>
#include <map>
#include "la.h"
#include "color.h"
#include "binary.h"
#include <algorithm>

namespace meshio {
  namespace vmd {

    ////////////////////////////////////////////////////////////
    //! モーション
    ////////////////////////////////////////////////////////////
    struct BoneKey
    {
      Vector3 pos;
      Quaternion q;
      char interpolationX[16];
      char interpolationY[16];
      char interpolationZ[16];
      char interpolationRot[16];
    };
    inline std::ostream& operator<<(std::ostream &os, const BoneKey &rhs)
    {
      return os
        << "<BoneKey: " << rhs.pos << rhs.q << ">" 
        ;
    }

    ////////////////////////////////////////////////////////////
    //! 表情
    ////////////////////////////////////////////////////////////
    struct MorphKey
    {
      float weight;
    };
    inline std::ostream& operator<<(std::ostream &os, const MorphKey &rhs)
    {
      return os
        << "<MorphKey: " << rhs.weight << ">" 
        ;
    }


    ////////////////////////////////////////////////////////////
    //! カメラ
    ////////////////////////////////////////////////////////////
    struct CameraKey
    {
      //! 何の距離？
      float length;
      //! 位置
      Vector3 pos;
      //! オイラー角
      Vector3 euler;
      //! 補間
      char interpolation[24];
      //! 視野角
      unsigned short viewAngle;
      //! 遠近感 0がon
      unsigned char perspective;
    };
    inline std::ostream& operator<<(std::ostream &os, const CameraKey &rhs)
    {
      return os
        << "<CameraKey: " << rhs.length 
        << rhs.pos << rhs.euler << ">" 
        ;
    }


    ////////////////////////////////////////////////////////////
    //! 光源
    ////////////////////////////////////////////////////////////
    struct LightKey
    {
      fRGB color;
      Vector3 pos;
    };
    inline std::ostream& operator<<(std::ostream &os, const LightKey &rhs)
    {
      return os
        << "<LightKey: " << rhs.color << rhs.pos << ">" 
        ;
    }


    ////////////////////////////////////////////////////////////
    //! セルフシャドウ
    ////////////////////////////////////////////////////////////
    struct SelfShadowKey
    {
    };

    ////////////////////////////////////////////////////////////
    //! KeyFrame
    ////////////////////////////////////////////////////////////
    template<typename T>
      struct KeyFrame
      {
        typedef T VALUE_TYPE;

        //! フレーム番号
        unsigned int frame;
        //! キー
        T key;

        //! フレーム番号でキーをソートする
        bool operator<(const KeyFrame &rhs)const{ return frame<rhs.frame; }
      };

    ////////////////////////////////////////////////////////////
    //! 1チャンネル分のキーフレームのリスト。
    //! 読み込んだ後でフレーム番号でソートする。
    ////////////////////////////////////////////////////////////
    template<typename T>
      struct KeyFrameList
      {
        typedef T KEYFRAME_TYPE;

        std::vector<KEYFRAME_TYPE> list;
        void sort(){ std::sort(list.begin(), list.end()); }
        KEYFRAME_TYPE& push(unsigned int frame)
        {
          list.push_back(KEYFRAME_TYPE());
          KEYFRAME_TYPE &keyFrame=list.back();
          keyFrame.frame=frame;
          return keyFrame;
        }
      };

    ////////////////////////////////////////////////////////////
    //! IO
    ////////////////////////////////////////////////////////////
    typedef KeyFrame<BoneKey> BoneKeyFrame;
    typedef KeyFrameList<BoneKeyFrame> BoneKeyFrameList;

    typedef KeyFrame<MorphKey> MorphKeyFrame;
    typedef KeyFrameList<MorphKeyFrame> MorphKeyFrameList;

    struct IO
    {
      std::string version;
      char name[20];

      //! モーション
      typedef std::map<std::wstring, BoneKeyFrameList*> BoneMap;
      BoneMap boneMap;
      std::vector<std::wstring> boneKeys;

      //! 表情
      typedef std::map<std::wstring, MorphKeyFrameList*> MorphMap;
      MorphMap morphMap;
      std::vector<std::wstring> morphKeys;

      IO();
      ~IO();
      bool read(binary::IReader &reader);
      bool read(const char *path);
      bool write(std::ostream &os);
    };
    inline std::ostream& operator<<(std::ostream &os, const IO &rhs)
    {
      os
        << "<VMD " << rhs.name << std::endl
        << "[bones] " << rhs.boneMap.size() << std::endl
        << "[morphs] " << rhs.morphMap.size() << std::endl
        << ">"
        ;
      return os;
    }

  } // namespace vmd
} // namespace meshio

#endif // MESH_IO_VMD_H_INCLUDED
