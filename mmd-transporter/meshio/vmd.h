/**
 * VMD�`��
 * MMD�̃��[�V�����f�[�^�B
 * �o�C�i���`���Ń{�[�����[�V�����A�\��[�t�B���O�A�����A�e�̃L�[�t���[����
 * �L�^�����B
 *
 * �Q�l�T�C�g
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
    //! ���[�V����
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
    //! �\��
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
    //! �J����
    ////////////////////////////////////////////////////////////
    struct CameraKey
    {
      //! ���̋����H
      float length;
      //! �ʒu
      Vector3 pos;
      //! �I�C���[�p
      Vector3 euler;
      //! ���
      char interpolation[24];
      //! ����p
      unsigned short viewAngle;
      //! ���ߊ� 0��on
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
    //! ����
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
    //! �Z���t�V���h�E
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

        //! �t���[���ԍ�
        unsigned int frame;
        //! �L�[
        T key;

        //! �t���[���ԍ��ŃL�[���\�[�g����
        bool operator<(const KeyFrame &rhs)const{ return frame<rhs.frame; }
      };

    ////////////////////////////////////////////////////////////
    //! 1�`�����l�����̃L�[�t���[���̃��X�g�B
    //! �ǂݍ��񂾌�Ńt���[���ԍ��Ń\�[�g����B
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

      //! ���[�V����
      typedef std::map<std::wstring, BoneKeyFrameList*> BoneMap;
      BoneMap boneMap;
      std::vector<std::wstring> boneKeys;

      //! �\��
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
